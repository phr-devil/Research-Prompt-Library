#!/usr/bin/env python3
"""Reproducible prompt A/B benchmark. Default is plan-only; --live may incur model charges."""
import argparse,csv,hashlib,json,os,random,re,subprocess,sys,urllib.request,urllib.parse
from pathlib import Path
BASE="e205a9a10d5c75641461205032a2aafb9f6b28cc"
CAND="be351d5cf925507fb84d545b6eb46857ae52a9df"
def read(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def save(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def prompt(repo,sha,path):
    if len(sha)!=40 or any(c not in "0123456789abcdef" for c in sha):
        raise ValueError("Require pinned 40-character Git commit")
    r=subprocess.run(["git","-C",str(repo),"show",sha+":"+path],capture_output=True,text=True,encoding="utf-8",timeout=15)
    if r.returncode: raise RuntimeError("Missing Git source/history: "+path)
    part=r.stdout.split("## 可直接复制的 Prompt")
    if len(part)!=2: raise ValueError("Missing prompt heading")
    m=re.search(r"\x60{3}text\s*\n([\s\S]*?)\n\x60{3}",part[1])
    if not m or len(m.group(1).strip())<100: raise ValueError("Missing prompt text")
    return m.group(1).strip()
def endpoint(base):
    u=urllib.parse.urlsplit(base)
    if u.username or u.password or u.query or u.fragment: raise ValueError("Unsafe API URL")
    if u.scheme=="https" and u.hostname: return base.rstrip("/")+"/chat/completions"
    if u.scheme=="http" and u.hostname in ("127.0.0.1","localhost","::1"):
        return base.rstrip("/")+"/chat/completions"
    raise ValueError("Require HTTPS or loopback HTTP")
def invoke(url,key,model,sys_prompt,task,limit):
    payload={"model":model,"messages":[{"role":"system","content":sys_prompt},{"role":"user","content":task}],
             "max_completion_tokens":limit}
    req=urllib.request.Request(url,data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
        headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=90) as r: obj=json.loads(r.read().decode("utf-8"))
    if not obj.get("choices"): raise ValueError("No completions returned")
    answer=obj["choices"][0].get("message",{}).get("content")
    if not isinstance(answer,str): raise ValueError("No textual response")
    return answer,obj.get("usage") or {}
def score(out,repo):
    m=read(out/"manifest.json")
    if m["status"]!="MODEL_OUTPUTS_UNSCORED": raise ValueError("No completed independent model run")
    mapping=read(out/"private_mapping.json");cases={x["id"]:x for x in read(repo/"EVAL_CASES.json")["cases"]}
    with (out/"blind_review.csv").open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    if len(rows)!=len(mapping): raise ValueError("Review missing rows")
    result={"baseline":{"n":0,"full_pass":0,"critical_errors":0},
            "candidate":{"n":0,"full_pass":0,"critical_errors":0}}
    for row in rows:
        data=mapping[row["blind_id"]];case=cases[data["case_id"]]
        correct=int(row["must_pass_count"]);severe=int(row["critical_error_0_or_1"])
        if correct<0 or correct>len(case["must"]) or severe not in (0,1):raise ValueError("Invalid review value")
        v=result[data["version"]];v["n"]+=1;v["full_pass"]+=int(correct==len(case["must"]) and severe==0)
        v["critical_errors"]+=severe
    raw=[json.loads(x) for x in (out/"raw_responses.jsonl").read_text(encoding="utf-8").splitlines()]
    for name,ref in (("baseline",m["base_ref"]),("candidate",m["candidate_ref"])):
        usage=[x.get("usage",{}) for x in raw if x["ref"]==ref]
        result[name]["measured_total_tokens"]=(sum(u["total_tokens"] for u in usage)
            if len(usage)==result[name]["n"] and all(type(u.get("total_tokens")) is int for u in usage) else None)
    save(out/"scores.json",result);print(json.dumps(result,ensure_ascii=False,indent=2))
def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--repo",type=Path,default=Path(__file__).resolve().parent)
    a.add_argument("--base-ref",default=BASE);a.add_argument("--candidate-ref",default=CAND)
    a.add_argument("--cases",default="T03,T04,T08,T11");a.add_argument("--all",action="store_true")
    a.add_argument("--repeat",type=int,default=1);a.add_argument("--seed",type=int,default=20261026)
    a.add_argument("--max-calls",type=int,default=8);a.add_argument("--output-dir",type=Path,default=Path(".eval_runs/pilot"))
    a.add_argument("--model",default="");a.add_argument("--live",action="store_true");a.add_argument("--score",action="store_true")
    a.add_argument("--api-base",default=os.getenv("OPENAI_BASE_URL","https://api.openai.com/v1"))
    a.add_argument("--token-limit",type=int,default=650)
    arg=a.parse_args();repo=arg.repo.resolve();out=arg.output_dir.resolve()
    if arg.score: return score(out,repo)
    cases=read(repo/"EVAL_CASES.json")["cases"];byid={x["id"]:x for x in cases}
    index={x["id"]:x["file"] for x in read(repo/"LIBRARY_INDEX.json")}
    selection=sorted(byid) if arg.all else [x.strip() for x in arg.cases.split(",")]
    if len(cases)!=len(byid) or len(selection)!=len(set(selection)) or any(x not in byid for x in selection):
        raise ValueError("Duplicate or unknown case")
    if not 1<=arg.repeat<=10 or not 1<=arg.token_limit<=4096:raise ValueError("Invalid repeat/token limit")
    rng=random.Random(arg.seed);jobs=[]
    for test_id in selection:
        case=byid[test_id]
        for rep in range(arg.repeat):
            options=[("baseline",arg.base_ref),("candidate",arg.candidate_ref)]
            rng.shuffle(options)
            for name,ref in options:
                s=prompt(repo,ref,index[case["prompt_id"]])
                jobs.append({"case_id":test_id,"repeat":rep+1,"version":name,"ref":ref,
                             "system":s,"task":case["input"],
                             "prompt_sha256":hashlib.sha256(s.encode()).hexdigest()})
    rng.shuffle(jobs)
    if len(jobs)>arg.max_calls:raise ValueError("Call budget exceeded; raise --max-calls explicitly")
    out.mkdir(parents=True,exist_ok=True)
    m={"status":"PLAN_ONLY","base_ref":arg.base_ref,"candidate_ref":arg.candidate_ref,
       "model":arg.model if arg.live else None,"planned_calls":len(jobs),"actual_calls":0}
    save(out/"manifest.json",m)
    save(out/"plan.json",[{k:v for k,v in x.items() if k not in ("system","task")} for x in jobs])
    if not arg.live:
        print("PLAN_ONLY:",len(jobs),"calls planned; no model invoked");return
    key=os.getenv("OPENAI_API_KEY","")
    if not arg.model or not key:raise ValueError("Need --model and OPENAI_API_KEY for live inference")
    url=endpoint(arg.api_base)
    if (out/"raw_responses.jsonl").exists():raise ValueError("Output directory already contains model outputs")
    blind=[];mapping={};m["status"]="RUNNING"
    try:
        with (out/"raw_responses.jsonl").open("w",encoding="utf-8") as f:
            for i,job in enumerate(jobs):
                response,usage=invoke(url,key,arg.model,job["system"],job["task"],arg.token_limit)
                label="R"+str(i+1).zfill(3)
                mapping[label]={"version":job["version"],"case_id":job["case_id"]}
                entry={"blind_id":label,"case_id":job["case_id"],"ref":job["ref"],
                       "answer":response,"usage":usage,"prompt_sha256":job["prompt_sha256"]}
                f.write(json.dumps(entry,ensure_ascii=False)+"\n");f.flush()
                blind.append({"blind_id":label,"case_id":job["case_id"],"response":response,
                              "must_pass_count":"","critical_error_0_or_1":"","notes":""})
                m["actual_calls"]=i+1;save(out/"manifest.json",m)
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
