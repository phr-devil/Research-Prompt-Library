#!/usr/bin/env python3
"""Reproducible prompt A/B benchmark. Default is plan-only; --live may incur model charges."""
import argparse,csv,hashlib,json,os,random,re,subprocess,sys,urllib.request,urllib.parse
from pathlib import Path
BASE="e205a9a10d5c75641461205032a2aafb9f6b28cc"
CAND="be351d5cf925507fb84d545b6eb46857ae52a9df"
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def save(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def prompt(repo,sha,path,selector=""):
    if len(sha)!=40 or any(c not in "0123456789abcdef" for c in sha):
        raise ValueError("Require pinned 40-character Git commit")
    r=subprocess.run(["git","-C",str(repo),"show",sha+":"+path],capture_output=True,text=True,encoding="utf-8",timeout=15)
    if r.returncode:raise RuntimeError("Missing Git source/history: "+path)
    content=r.stdout
    if selector:
        if selector=="S01-B":
            heading=r"(?m)^### B ·[^\n]*$"
        elif selector=="09-ONECLICK":
            heading=r"(?m)^## 02｜一键总控 Prompt[^\n]*$"
        elif selector=="09-REFINE":
            heading=r"(?m)^### STEP 05-R：[^\n]*$"
        elif re.fullmatch(r"0[1-5]-[A-F]",selector):
            heading=r"(?m)^## "+re.escape(selector)+r"｜[^\n]*$"
        else:
            raise ValueError("Unknown prompt selector: "+selector)
        match=re.search(heading,content)
        if not match:raise ValueError("Missing selected prompt heading "+selector)
        section=content[match.end():]
        stop=re.search(r"(?m)^#{2,3} ",section)
        content=section[:stop.start()] if stop else section
    else:
        part=content.split("## 可直接复制的 Prompt")
        if len(part)!=2:raise ValueError("Missing prompt heading")
        content=part[1]
    m=re.search(r"(?:\x60{3}|~{3})text\s*\n([\s\S]*?)\n(?:\x60{3}|~{3})",content)
    if not m or len(m.group(1).strip())<100:raise ValueError("Missing selected prompt text")
    return m.group(1).strip()
def endpoint(base):
    u=urllib.parse.urlsplit(base)
    if u.username or u.password or u.query or u.fragment: raise ValueError("Unsafe API URL")
    if u.scheme=="https" and u.hostname: return base.rstrip("/")+"/chat/completions"
    if u.scheme=="http" and u.hostname in ("127.0.0.1","localhost","::1"):
        return base.rstrip("/")+"/chat/completions"
    raise ValueError("Require HTTPS or loopback HTTP")
class RejectRedirect(urllib.request.HTTPRedirectHandler):
    """Do not forward API credentials to a redirect target."""
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise ValueError("API redirect rejected; check the configured endpoint")

def invoke(url,key,model,sys_prompt,task,limit,token_field="max_completion_tokens",timeout=90,temperature=None):
    payload={"model":model,"messages":[{"role":"system","content":sys_prompt},{"role":"user","content":task}],
             token_field:limit}
    if temperature is not None: payload["temperature"]=temperature
    req=urllib.request.Request(url,data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
        headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
    with urllib.request.build_opener(RejectRedirect()).open(req,timeout=timeout) as r: obj=json.loads(r.read().decode("utf-8"))
    if not obj.get("choices"): raise ValueError("No completions returned")
    answer=obj["choices"][0].get("message",{}).get("content")
    if not isinstance(answer,str) or not answer.strip(): raise ValueError("Empty/non-textual model response")
    meta={"model":obj.get("model") or model,"finish_reason":obj["choices"][0].get("finish_reason")}
    if meta["finish_reason"]!="stop":
        raise ValueError("Model response did not finish normally: "+str(meta["finish_reason"]))
    return answer,obj.get("usage") or {},meta
def score(out,repo):
    m=read(out/"manifest.json")
    if m["status"]!="MODEL_OUTPUTS_UNSCORED": raise ValueError("No completed independent model run")
    fixture_name=m.get("fixture_file","EVAL_CASES.json")
    if fixture_name not in ("EVAL_CASES.json","EVAL_CASES_CURRENT.json"):
        raise ValueError("Unknown pinned evaluation fixture")
    fixture=read(repo/fixture_name)
    mapping=read(out/"private_mapping.json");cases={x["id"]:x for x in fixture["cases"]}
    with (out/"blind_review.csv").open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    if len(rows)!=len(mapping): raise ValueError("Review missing rows")
    ids=[r.get("blind_id","") for r in rows]
    if len(set(ids))!=len(ids) or set(ids)!=set(mapping):raise ValueError("Duplicate, missing or unknown review labels")
    if m.get("actual_calls")!=m.get("planned_calls") or m.get("actual_calls")!=len(mapping):
        raise ValueError("Manifest call count is inconsistent with model outputs")
    raw=[json.loads(x) for x in (out/"raw_responses.jsonl").read_text(encoding="utf-8").splitlines()]
    raw_by_id={x.get("blind_id"):x for x in raw}
    if len(raw)!=len(mapping) or len(raw_by_id)!=len(mapping) or set(raw_by_id)!=set(mapping):
        raise ValueError("Raw output IDs are missing or duplicated")
    plan=read(out/"plan.json")
    if len(plan)!=len(mapping):raise ValueError("Planned jobs do not match collected outputs")
    expected_cases={x["id"]:x for x in fixture["cases"]}
    fixture_hash=hashlib.sha256(json.dumps(
        [expected_cases[x] for x in m["selected_cases"]],ensure_ascii=False,sort_keys=True
        ).encode("utf-8")).hexdigest()
    if fixture_hash!=m.get("fixture_sha256"):
        raise ValueError("Evaluation rubric changed after inference")
    for i,p in enumerate(plan,1):
        label="R"+str(i).zfill(3)
        x=raw_by_id[label]
        if x.get("ref")!=p["ref"] or x.get("case_id")!=p["case_id"] or x.get("prompt_sha256")!=p["prompt_sha256"]:
            raise ValueError("Raw model output does not match the frozen plan")
        if x.get("repeat")!=p["repeat"] or x.get("model_meta",{}).get("finish_reason")!="stop":
            raise ValueError("Incomplete or incorrectly paired model result")
        if mapping[label]!={"version":p["version"],"case_id":p["case_id"],"repeat":p["repeat"]}:
            raise ValueError("Private blind mapping disagrees with planned job")
    for row in rows:
        x=raw_by_id[row["blind_id"]]
        if row.get("case_id")!=x["case_id"] or row.get("response")!=x["answer"]:
            raise ValueError("Review response text or case ID was altered")
    result={"baseline":{"n":0,"full_pass":0,"critical_errors":0},
            "candidate":{"n":0,"full_pass":0,"critical_errors":0}}
    for row in rows:
        data=mapping[row["blind_id"]];case=cases[data["case_id"]]
        correct=int(row["must_pass_count"]);severe=int(row["critical_error_0_or_1"])
        if correct<0 or correct>len(case["must"]) or severe not in (0,1):raise ValueError("Invalid review value")
        v=result[data["version"]];v["n"]+=1;v["full_pass"]+=int(correct==len(case["must"]) and severe==0)
        v["critical_errors"]+=severe
    observed_models={x.get("model_meta",{}).get("model") for x in raw}
    if len(observed_models)!=1 or not all(isinstance(name,str) and name.strip() for name in observed_models):
        raise ValueError("Model identity changed across A/B runs")
    result["observed_model"]=next(iter(observed_models))
    for name,ref in (("baseline",m["base_ref"]),("candidate",m["candidate_ref"])):
        usage=[x.get("usage") or {} for x in raw if x["ref"]==ref]
        for metric in ("prompt_tokens","completion_tokens","total_tokens"):
            result[name]["measured_"+metric]=(sum(u[metric] for u in usage)
                if len(usage)==result[name]["n"] and all(type(u.get(metric)) is int for u in usage) else None)
    # Preserve genuine case+repeat pairing: aggregate counts alone are insufficient.
    pairs={};totals={"candidate_only":0,"baseline_only":0,"both_pass":0,"both_fail":0}
    bypair={}
    for row in rows:
        entry=mapping[row["blind_id"]]
        key=(entry["case_id"],entry["repeat"])
        pair=bypair.setdefault(key,{})
        if entry["version"] in pair:
            raise ValueError("Repeated version within the same case/repeat pair")
        passed=(int(row["must_pass_count"])==len(cases[entry["case_id"]]["must"])
                and int(row["critical_error_0_or_1"])==0)
        pair[entry["version"]]=int(passed)
    for cid in m["selected_cases"]:
        stats={"candidate_only":0,"baseline_only":0,"both_pass":0,"both_fail":0}
        for repeat in range(1,m["repeat"]+1):
            pair=bypair.get((cid,repeat))
            if not pair or set(pair)!={"baseline","candidate"}:
                raise ValueError("Missing balanced comparison for "+cid+" repeat "+str(repeat))
            label=("both_pass" if pair["baseline"] and pair["candidate"] else
                   "candidate_only" if pair["candidate"] else
                   "baseline_only" if pair["baseline"] else "both_fail")
            stats[label]+=1;totals[label]+=1
        pairs[cid]={"n":m["repeat"],**stats}
    if sum(totals.values())!=result["baseline"]["n"] or result["baseline"]["n"]!=result["candidate"]["n"]:
        raise ValueError("Paired totals do not match model output counts")
    result["per_case"]=pairs
    result["paired_summary"]={"n_pairs":sum(totals.values()),**totals}
    result["measured_token_definition"]="Per version: observed service-reported prompt/completion/total tokens; null when incomplete"
    result["status"]="HUMAN_REVIEW_SCORED_NOT_INDEPENDENTLY_VERIFIED"
    result["limits"]="Descriptive pilot only; no inferential significance claim"
    save(out/"scores.json",result);print(json.dumps(result,ensure_ascii=False,indent=2))
def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--repo",type=Path,default=Path(__file__).resolve().parent)
    a.add_argument("--suite",choices=("historical","current"),default="historical",
                   help="Historical frozen v1.3/v1.5 benchmark or explicit current-version stress fixture")
    a.add_argument("--base-ref",default=None);a.add_argument("--candidate-ref",default=None)
    a.add_argument("--cases",default=None);a.add_argument("--all",action="store_true")
    a.add_argument("--repeat",type=int,default=1);a.add_argument("--seed",type=int,default=20261026)
    a.add_argument("--max-calls",type=int,default=8);a.add_argument("--output-dir",type=Path,default=Path(".eval_runs/pilot"))
    a.add_argument("--model",default="");a.add_argument("--live",action="store_true");a.add_argument("--score",action="store_true")
    a.add_argument("--api-base",default=os.getenv("OPENAI_BASE_URL","https://api.openai.com/v1"))
    a.add_argument("--token-limit",type=int,default=650)
    a.add_argument("--allow-unchanged-controls",action="store_true",help="Explicitly allow cases whose compared prompt text is identical")
    a.add_argument("--token-field",choices=("max_completion_tokens","max_tokens"),default="max_completion_tokens")
    a.add_argument("--timeout",type=int,default=90)
    a.add_argument("--temperature",type=float,default=None,help="Explicit generation temperature; omit if unsupported")
    arg=a.parse_args();repo=arg.repo.resolve();out=arg.output_dir.resolve()
    if arg.score: return score(out,repo)
    if arg.suite=="current" and (arg.base_ref is None or arg.candidate_ref is None):
        raise ValueError("--suite current requires explicit pinned --base-ref and --candidate-ref")
    arg.base_ref=arg.base_ref or BASE
    arg.candidate_ref=arg.candidate_ref or CAND
    fixture_file=("EVAL_CASES_CURRENT.json" if arg.suite=="current" else "EVAL_CASES.json")
    fixture=read(repo/fixture_file)
    cases=fixture["cases"]
    if not isinstance(cases,list) or not cases or any(
        not isinstance(c,dict) or not isinstance(c.get("id"),str) or not c["id"]
        or not isinstance(c.get("prompt_id"),str) or not c["prompt_id"]
        or not isinstance(c.get("input"),str) or not c["input"].strip()
        or any(not isinstance(c.get(k),list) or not c[k] or any(
            not isinstance(v,str) or not v.strip() for v in c[k])
            for k in ("must","critical"))
        for c in cases):
        raise ValueError("Invalid cases fixture: IDs, inputs, and rubrics must be nonempty")
    byid={x["id"]:x for x in cases}
    index_items=read(repo/"LIBRARY_INDEX.json")
    index={x["id"]:x["file"] for x in index_items}
    if any(
        (not isinstance(c.get("prompt_selector",""),str) or
         (c.get("prompt_path") is not None and not isinstance(c["prompt_path"],str)))
        for c in cases):
        raise ValueError("Invalid prompt selector/path in fixture")
    if len(cases)!=len(byid) or len(index_items)!=len(index) or any(
        c["prompt_id"] not in index and not c.get("prompt_path") for c in cases):
        raise ValueError("Duplicate case/index ID or unknown prompt_id")
    if arg.all and arg.cases is not None:
        raise ValueError("Choose --all or --cases, not both")
    selection=(sorted(byid) if arg.all else
               fixture.get("pilot_ids") if arg.cases is None else
               [x.strip() for x in arg.cases.split(",")])
    if (not isinstance(selection,list) or not selection
        or any(not isinstance(x,str) or not x.strip() for x in selection)
        or len(selection)!=len(set(selection)) or any(x not in byid for x in selection)):
        raise ValueError("Duplicate, empty or unknown case in selection")
    if arg.temperature is not None and not 0<=arg.temperature<=2:raise ValueError("Temperature must be in [0,2]")
    if not 1<=arg.repeat<=10 or not 1<=arg.token_limit<=4096 or not 5<=arg.timeout<=600:
        raise ValueError("Invalid repeat/token/timeout limit")
    if arg.base_ref==arg.candidate_ref:raise ValueError("Baseline and candidate commits must differ")
    rng=random.Random(arg.seed);jobs=[];prompt_cache={}
    for test_id in selection:
        case=byid[test_id]
        for rep in range(arg.repeat):
            options=[("baseline",arg.base_ref),("candidate",arg.candidate_ref)]
            rng.shuffle(options)
            for name,ref in options:
                source=case.get("prompt_path") or index[case["prompt_id"]]
                if (not isinstance(source,str) or not source.endswith(".md") or
                    source.startswith("/") or "\\\\" in source or
                    any(p in ("",".","..") for p in source.split("/"))):
                    raise ValueError("Unsafe prompt_path: "+str(source))
                selector=case.get("prompt_selector","")
                if not isinstance(selector,str):raise ValueError("Invalid prompt selector")
                key=(ref,source,selector)
                if key not in prompt_cache:prompt_cache[key]=prompt(repo,*key)
                s=prompt_cache[key]
                jobs.append({"case_id":test_id,"repeat":rep+1,"version":name,"ref":ref,
                             "system":s,"task":case["input"],
                             "prompt_sha256":hashlib.sha256(s.encode()).hexdigest()})
    unchanged=[]
    for case_id in selection:
        paired=[j["prompt_sha256"] for j in jobs if j["case_id"]==case_id and j["repeat"]==1]
        if len(paired)!=2:
            raise ValueError("Unpaired comparison for "+case_id)
        if paired[0]==paired[1]:
            unchanged.append(case_id)
    if unchanged and not arg.allow_unchanged_controls:
        raise ValueError("Compared Prompt texts are identical for "+",".join(unchanged)+
                         "; choose changed scenarios or explicitly use --allow-unchanged-controls")
    rng.shuffle(jobs)
    if len(jobs)>arg.max_calls:raise ValueError("Call budget exceeded; raise --max-calls explicitly")
    # Validate the live endpoint and credentials BEFORE writing any output files.
    if arg.live:
        if not arg.model or not os.getenv("OPENAI_API_KEY",""):
            raise ValueError("Need --model and OPENAI_API_KEY for live inference")
        url=endpoint(arg.api_base)
    if out.exists() and any(out.iterdir()):
        raise ValueError("Output directory is not empty; use a fresh --output-dir")
    out.mkdir(parents=True,exist_ok=True)
    fixture_hash=hashlib.sha256(json.dumps(
        [byid[x] for x in selection],ensure_ascii=False,sort_keys=True
        ).encode("utf-8")).hexdigest()
    m={"suite":arg.suite,"fixture_file":fixture_file,"selected_cases":selection,
       "unchanged_control_cases":unchanged,"fixture_sha256":fixture_hash,
       "seed":arg.seed,"repeat":arg.repeat,"token_field":arg.token_field,"temperature":arg.temperature,
       "status":"PLAN_ONLY","base_ref":arg.base_ref,"candidate_ref":arg.candidate_ref,
       "model":arg.model if arg.live else None,"planned_calls":len(jobs),"actual_calls":0}
    save(out/"manifest.json",m)
    save(out/"plan.json",[{k:v for k,v in x.items() if k not in ("system","task")} for x in jobs])
    if not arg.live:
        print("PLAN_ONLY:",len(jobs),"calls planned; no model invoked");return
    key=os.getenv("OPENAI_API_KEY","")
    if not key:raise ValueError("OPENAI_API_KEY missing")
    blind=[];mapping={};m["status"]="RUNNING"
    try:
        with (out/"raw_responses.jsonl").open("w",encoding="utf-8") as f:
            for i,job in enumerate(jobs):
                response,usage,model_meta=invoke(url,key,arg.model,job["system"],job["task"],arg.token_limit,arg.token_field,arg.timeout,arg.temperature)
                label="R"+str(i+1).zfill(3)
                mapping[label]={"version":job["version"],"case_id":job["case_id"],"repeat":job["repeat"]}
                entry={"blind_id":label,"case_id":job["case_id"],"repeat":job["repeat"],"model_meta":model_meta,"ref":job["ref"],
                       "answer":response,"usage":usage,"prompt_sha256":job["prompt_sha256"]}
                f.write(json.dumps(entry,ensure_ascii=False)+"\n");f.flush()
                blind.append({"blind_id":label,"case_id":job["case_id"],"response":response,
                              "must_pass_count":"","critical_error_0_or_1":"","notes":""})
                m["actual_calls"]=i+1;save(out/"manifest.json",m)
                if model_meta.get("finish_reason")!="stop":
                    raise ValueError("Model response not normally completed: refusing to score incomplete run")
        m["status"]="MODEL_OUTPUTS_UNSCORED"
    finally:
        if m["status"]=="RUNNING":m["status"]="FAILED_OR_INCOMPLETE"
        save(out/"manifest.json",m);save(out/"private_mapping.json",mapping)
        if blind:
            with (out/"blind_review.csv").open("w",encoding="utf-8-sig",newline="") as f:
                w=csv.DictWriter(f,fieldnames=blind[0].keys());w.writeheader();w.writerows(blind)
    print("Real model outputs recorded. Blind human review required; no success rate yet.")
if __name__=="__main__":
    try:main()
    except Exception as e:print("EVAL_ABORTED:",str(e)[:250],file=sys.stderr);sys.exit(2)
