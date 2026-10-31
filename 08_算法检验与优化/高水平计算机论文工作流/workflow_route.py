#!/usr/bin/env python3
"""Read-only scientific prompt and event adviser; never executes model or grants permissions."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = [f"{s:02d}-{chr(65+i)}" for s,n in enumerate((4,5,6,4,5),1) for i in range(n)]
FENCE = re.compile(r"(?m)^(?P<mark>`{3}|~{3})text[ \t]*\r?\n(?P<body>[\s\S]*?)\r?\n(?P=mark)[ \t]*$")


def resolve_playbook(relative_path, root=ROOT):
    """Read-only resolver for explicitly allowlisted in-repository playbook links."""
    if (not isinstance(relative_path, str) or not relative_path
            or not (relative_path == "POST_SELECTION.md"
                    or relative_path.startswith("playbooks/"))
            or "\\" in relative_path or ".." in relative_path.split("/")):
        raise ValueError("Invalid playbook path")
    path = (root / relative_path).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file() or path.suffix != ".md":
        raise ValueError("Unsafe or absent playbook")
    return path


def load_routes(root=ROOT):
    catalog = json.loads((root/"ROUTES.json").read_text(encoding="utf-8"))
    if catalog.get("version") != "5.0.0":
        raise ValueError("Unknown route manifest")
    if len(catalog.get("stages", [])) != 5:
        raise ValueError("Expected exactly five research stages")
    found = {}
    for index, stage in enumerate(catalog["stages"], 1):
        if stage.get("id") != f"{index:02d}" or not isinstance(stage.get("file"), str):
            raise ValueError("Stage IDs must match the expected order")
        if not stage["file"].startswith(stage["id"]+"_"):
            raise ValueError("Stage file does not match stage ID")
        if index == 1 and stage.get("default_platform") != "ChatGPT":
            raise ValueError("Stage 01 must default to ChatGPT")
        path = (root/stage["file"]).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file() or path.suffix != ".md":
            raise ValueError("Unsafe or absent stage file")
        for item in stage["routes"]:
            key = item["id"]
            if key in found or not re.fullmatch(r"0[1-5]-[A-F]",key) or not key.startswith(stage["id"]+"-"):
                raise ValueError("Duplicate/invalid route ID")
            if item["kind"] not in ("as_needed","required_for_action","conditional") or not item["when"]:
                raise ValueError("Invalid route trigger")
            found[key] = (path,item)
    if list(found) != EXPECTED:
        raise ValueError("Expected 24 unique selectors in original order")
    if catalog.get("workflow_version") in ("6.0", "6.1"):
        default = catalog.get("default_path", {})
        if default.get("mandatory_scenes") != [] or default.get("mode") != "PROTOTYPE_FIRST":
            raise ValueError("Fast-path must not require legacy scenes")
        for event, advice in catalog.get("event_advice", {}).items():
            if not re.fullmatch(r"[A-Z_]{3,48}", event) or not isinstance(advice, dict):
                raise ValueError("Invalid research event")
            if advice.get("route") is not None and advice["route"] not in found:
                raise ValueError("Unknown advisory route")
            if not advice.get("action") or not advice.get("why"):
                raise ValueError("Incomplete event advice")
            if "playbook" in advice:
                resolve_playbook(advice["playbook"], root)
            for field in ("deliverable", "verify", "boundary"):
                if field in advice and (not isinstance(advice[field], str) or not advice[field].strip()):
                    raise ValueError("Invalid research event operation: " + field)
    return found


def extract(path,key):
    doc = path.read_text(encoding="utf-8")
    matches = list(re.finditer(r"(?m)^## "+re.escape(key)+r"｜[^\n]*$",doc))
    if len(matches)!=1:
        raise ValueError("Missing or duplicate route heading "+key)
    m = matches[0]
    tail = doc[m.end():]
    end = re.search(r"(?m)^## ",tail)
    section = tail[:end.start()] if end else tail
    blocks = list(FENCE.finditer(section))
    if len(blocks) != 1 or len(blocks[0].group("body").strip()) < 100:
        raise ValueError("Expected one correctly closed text Prompt for " + key)
    return blocks[0].group("body").strip()



def load_repairs(root=ROOT, routes=None):
    """Fail-closed, read-only catalog: all 24 scenes and valid return routes."""
    if routes is None:
        routes=load_routes(root)
    doc=json.loads((root/"REPAIR_ROUTES.json").read_text(encoding="utf-8"))
    if doc.get("version")!="1.0.0":
        raise ValueError("Unknown repair catalog")
    fam=doc.get("families")
    if not isinstance(fam,dict) or not fam:
        raise ValueError("Missing repair families")
    for name,item in fam.items():
        if not re.fullmatch("[A-Z_]+",name) or not isinstance(item,dict):
            raise ValueError("Bad failure family")
        for field in ("class","check","fix","verify"):
            if not isinstance(item.get(field),str) or not item[field].strip():
                raise ValueError("Incomplete failure family")
    scenes={}
    for entry in doc.get("scenes",[]):
        key=entry.get("route")
        if key not in routes or key in scenes:
            raise ValueError("Unknown or duplicate repair route")
        cases=entry.get("failures")
        if not isinstance(cases,list) or not cases:
            raise ValueError("Empty repair list")
        for failure in cases:
            if failure.get("family") not in fam or failure.get("recheck") not in routes:
                raise ValueError("Unknown failure family or return route")
            if not failure.get("signal") or not failure.get("local_fix"):
                raise ValueError("Incomplete repair case")
        scenes[key]=cases
    if list(scenes)!=list(routes):
        raise ValueError("Repair catalog does not exactly cover 24 routes")
    return fam,scenes


def render_repair(key):
    fam,scenes=load_repairs()
    if key not in scenes:
        raise ValueError("Unknown repair route: "+str(key))
    out=["REPAIR_DIAGNOSTICS: "+key+"; read-only, not an experiment approval"]
    for i,c in enumerate(scenes[key],1):
        rule=fam[c["family"]]
        out.extend([f"{i}. {c['family']}: {c['signal']}",
                    "CHECK: "+rule["check"],
                    "REPAIR: "+c["local_fix"],
                    "GUARD: "+rule["fix"],
                    "VERIFY: "+rule["verify"],
                    "RECHECK_ROUTE: "+c["recheck"]])
    out.append("GPU/paid/formal-experiment approval remains separate.")
    return "\n".join(out)



def load_triage(root=ROOT, routes=None):
    """Validate instructions only; never infer true defect severity from CLI arguments."""
    if routes is None:routes=load_routes(root)
    doc=json.loads((root/"TRIAGE_POLICY.json").read_text(encoding="utf-8"))
    if doc.get("version")!="1.0.0" or set(doc.get("levels",{}))!={"CRITICAL","REPAIRABLE","MINOR"}:
        raise ValueError("Unsupported triage policy")
    expected={"CRITICAL":"BLOCK_AFFECTED_ACTION","REPAIRABLE":"USER_CHOICE","MINOR":"LOG_AND_CONTINUE"}
    for level,action in expected.items():
        rule=doc["levels"][level]
        if rule.get("default")!=action or not rule.get("meaning"):
            raise ValueError("Invalid severity contract")
    if [e.get("id") for e in doc.get("route_focus",[])]!=list(routes):
        raise ValueError("Triage must cover exactly 24 ordered routes")
    if any(not e.get("focus") for e in doc["route_focus"]):
        raise ValueError("Empty route-specific guidance")
    if [e.get("id") for e in doc.get("stages",[])]!=["01","02","03","04","05"]:
        raise ValueError("Missing stage-specific rules")
    expected_intents={"READ_ONLY_RESEARCH","SCOPED_EXPLORATION","DRAFT_PREPARATION","FORMAL_RUN","CONFIRMED_CLAIM","SUBMISSION"}
    if set(doc.get("action_intents",{}))!=expected_intents:
        raise ValueError("Invalid or missing action intent mapping")
    if set(doc.get("allowed_limited_intents",[]))!={"READ_ONLY_RESEARCH","SCOPED_EXPLORATION","DRAFT_PREPARATION"}:
        raise ValueError("Limited continuation scope must exclude formal and publication operations")
    if set(doc.get("choice_codes",[]))!={"CONTINUE_LIMITED","REPAIR_FIRST","REFRAME","HOLD"}:
        raise ValueError("Invalid choice codes")
    for ex in doc.get("examples",[]):
        if ex.get("severity") not in expected or not ex.get("scope") or not ex.get("signal"):
            raise ValueError("Bad triage example")
    return doc


def show_triage(key):
    doc=load_triage()
    if key not in load_routes():
        raise ValueError("Unknown triage route: "+str(key))
    focus=next(e["focus"] for e in doc["route_focus"] if e["id"]==key)
    out=["TRIAGE: "+key+" — advisory only, severity depends on real evidence and target action",
         "SCENE: "+focus]
    for level in ("CRITICAL","REPAIRABLE","MINOR"):
        rule=doc["levels"][level]
        out.append(level+": "+rule["default"]+" — "+rule["meaning"])
        if rule["menu"]:out.append("OPTIONS: "+" / ".join(rule["menu"]))
    out.append("UNKNOWN -> NEEDS_MINIMAL_EVIDENCE_CHECK (not automatic CRITICAL).")
    out.append("Actual later user messages must be verified by the host; stored choices alone are not approval.")
    out.append("No GPU/formal/paid permission is conferred by this read-only tool.")
    return "\n".join(out)


def propose_transition(level, intent, choice=None, policy=None, *, scoped_work_verified=False, material_change=False):
    """Offline routing suggestion, NOT evidence validation or user authorization.

    scoped_work_verified is supplied ONLY by a caller with independently checked
    actual permissions and experiment scope; the function cannot verify it.
    Explicit HOLD/REPAIR/REFRAME requests have precedence over optional auto-continue.
    UNKNOWN calls for a narrow evidence check, never an automatic positive conclusion.
    """
    if policy is None:
        policy = load_triage()
    if level not in (*policy["levels"], "UNKNOWN") or intent not in policy["action_intents"]:
        raise ValueError("Unknown severity or action intent")
    if choice is not None and choice not in policy["choice_codes"]:
        raise ValueError("Unknown proposed user choice")
    if level == "CRITICAL":
        return "BLOCKED_CRITICAL"
    if choice == "HOLD":
        return "HOLD"
    if choice == "REPAIR_FIRST":
        return "TARGETED_REPAIR"
    if choice == "REFRAME":
        return "NEEDS_USER_RESEARCH_SCOPE_CONFIRMATION"
    if intent in ("FORMAL_RUN", "CONFIRMED_CLAIM", "SUBMISSION"):
        return "INDEPENDENT_EVIDENCE_OR_APPROVAL_GATE"
    if level == "UNKNOWN":
        return "NEEDS_MINIMAL_EVIDENCE_CHECK"
    if level == "MINOR":
        return "DEFERRED_MINOR_CONTINUE"
    if choice is None:
        if (level == "REPAIRABLE" and scoped_work_verified and not material_change
                and intent in policy["allowed_limited_intents"]):
            return "BOUNDED_DIAGNOSTIC_CONTINUE"
        return "WAITING_FOR_USER_DECISION"
    if choice == "CONTINUE_LIMITED":
        if intent not in policy["allowed_limited_intents"]:
            return "INDEPENDENT_EVIDENCE_OR_APPROVAL_GATE"
        return "PROPOSED_READY_WITH_LIMITATIONS"
    raise ValueError("Unrecognized choice state")


def can_reuse_risk_choice(saved, current, *, user_message_verified=False):
    """Advisory matching only. Caller must independently verify the *later* real
    user message, its origin, and its content; a state file is never approval.
    """
    if not user_message_verified or not isinstance(saved, dict) or not isinstance(current, dict):
        return False
    if saved.get("choice") != "CONTINUE_LIMITED":
        return False
    if saved.get("level") != "REPAIRABLE" or current.get("level") != "REPAIRABLE":
        return False
    if current.get("review_due") is not False or current.get("permission_revoked") is not False:
        return False
    if current.get("new_user_override") is not False:
        return False
    required = ("decision_id", "issue_id", "claim_id", "claim_fingerprint",
                "data_fingerprint", "protocol_fingerprint", "action_intent",
                "allowed_scope", "revisit_before", "source_commit")
    if any(not isinstance(saved.get(k), str) or not saved[k].strip()
           or saved[k] != current.get(k) for k in required):
        return False
    if saved["action_intent"] not in ("READ_ONLY_RESEARCH", "SCOPED_EXPLORATION",
                                     "DRAFT_PREPARATION"):
        return False
    menu = saved.get("menu_message_reference")
    reply = saved.get("user_message_reference")
    if not isinstance(menu, str) or not isinstance(reply, str):
        return False
    if not menu.strip() or not reply.strip() or menu == reply:
        return False
    return True



def advise_event(event, root=ROOT):
    """Choose ONE narrowly relevant legacy route and optional practical playbook; no execution."""
    routes = load_routes(root)
    catalog = json.loads((root / "ROUTES.json").read_text(encoding="utf-8"))
    advice = catalog.get("event_advice", {}).get(event)
    if not advice or advice.get("route") not in (None, *routes):
        raise ValueError("Unknown research event: " + str(event))
    result = dict(advice, event=event, permission="ADVISORY_ONLY_NO_EXECUTION")
    if result["route"] is not None:
        stage = next(s for s in catalog["stages"] if s["id"] == result["route"][:2])
        if stage.get("default_platform"):
            result["recommended_platform"] = stage["default_platform"]
    return result


def render_event(event):
    item = advise_event(event)
    lines = ["EVENT: " + event, "SUGGESTED_ACTION: " + item["action"],
             "REASON: " + item["why"]]
    if item["route"] is not None:
        lines.append("OPTIONAL_ROUTE: " + item["route"])
    if item.get("recommended_platform"):
        lines.append("RECOMMENDED_PLATFORM: " + item["recommended_platform"])
    if item.get("playbook"):
        lines.append("OPTIONAL_PLAYBOOK: " + item["playbook"] + " (read one on demand)")
    for field, label in (("deliverable", "DELIVERABLE"), ("verify", "VERIFY"), ("boundary", "BOUNDARY")):
        if item.get(field):
            lines.append(label + ": " + item[field])
    if item.get("lesson"):
        lines.append("OPTIONAL_LESSON: " + item["lesson"])
    lines.append("Advisory only; it cannot verify message authenticity, data, budgets or permissions.")
    return "\n".join(lines)


def main():
    p=argparse.ArgumentParser(description="Read-only v6 research event adviser and legacy scene extractor")
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--id")
    g.add_argument("--list",action="store_true")
    g.add_argument("--check",action="store_true")
    g.add_argument("--repair",help="print this route's two repair scenarios; never execute")
    g.add_argument("--triage",help="print severity guidance for one scene, read-only")
    g.add_argument("--event",help="show one v6 research event recommendation, without execution")
    args=p.parse_args()
    try:
        routes=load_routes()
        if args.check:
            for key,(path,_) in routes.items():extract(path,key)
            load_repairs(routes=routes)
            load_triage(routes=routes)
            print("ROUTES_CHECK_PASS: 24/24; no model, GPU or paid calls")
        elif args.list:
            for key,(_,x) in routes.items():print(key,x["kind"],x["name"],x["when"])
        elif args.repair:
            print(render_repair(args.repair))
        elif args.triage:
            print(show_triage(args.triage))
        elif args.event:
            print(render_event(args.event))
        else:
            if args.id not in routes:raise ValueError("Unknown route "+str(args.id))
            print(extract(routes[args.id][0],args.id))
        return 0
    except (OSError,ValueError,KeyError,json.JSONDecodeError) as e:
        print("ROUTE_ERROR:",str(e),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
