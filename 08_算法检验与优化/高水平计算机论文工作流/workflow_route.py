#!/usr/bin/env python3
"""Read-only loader. Does not execute model, GPU, git or user approvals."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = [f"{s:02d}-{chr(65+i)}" for s,n in enumerate((4,5,6,4,5),1) for i in range(n)]
FENCE = re.compile(r"(?:\x60{3}|~{3})text\s*\n([\s\S]*?)\n(?:\x60{3}|~{3})")


def load_routes(root=ROOT):
    catalog = json.loads((root/"ROUTES.json").read_text(encoding="utf-8"))
    if catalog.get("version") != "5.0.0":
        raise ValueError("Unknown route manifest")
    found = {}
    for stage in catalog["stages"]:
        path = (root/stage["file"]).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file() or path.suffix != ".md":
            raise ValueError("Unsafe or absent stage file")
        for item in stage["routes"]:
            key = item["id"]
            if key in found or not re.fullmatch(r"0[1-5]-[A-F]",key) or not key.startswith(stage["id"]+"-"):
                raise ValueError("Duplicate/invalid route ID")
            if item["kind"] not in ("required","conditional") or not item["when"]:
                raise ValueError("Invalid route trigger")
            found[key] = (path,item)
    if list(found) != EXPECTED:
        raise ValueError("Expected 24 unique selectors in original order")
    return found


def extract(path,key):
    doc = path.read_text(encoding="utf-8")
    m = re.search(r"(?m)^## "+re.escape(key)+r"｜[^\n]*$",doc)
    if not m:
        raise ValueError("Missing route heading "+key)
    tail = doc[m.end():]
    end = re.search(r"(?m)^## ",tail)
    section = tail[:end.start()] if end else tail
    blocks = FENCE.findall(section)
    if len(blocks) != 1 or len(blocks[0].strip())<100:
        raise ValueError("Expected one full text Prompt for "+key)
    return blocks[0].strip()


def main():
    p=argparse.ArgumentParser(description="Load exactly one v5 scene Prompt; read-only")
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--id")
    g.add_argument("--list",action="store_true")
    g.add_argument("--check",action="store_true")
    args=p.parse_args()
    try:
        routes=load_routes()
        if args.check:
            for key,(path,_) in routes.items():extract(path,key)
            print("ROUTES_CHECK_PASS: 24/24; no model, GPU or paid calls")
        elif args.list:
            for key,(_,x) in routes.items():print(key,x["kind"],x["name"],x["when"])
        else:
            if args.id not in routes:raise ValueError("Unknown route "+str(args.id))
            print(extract(routes[args.id][0],args.id))
        return 0
    except (OSError,ValueError,KeyError,json.JSONDecodeError) as e:
        print("ROUTE_ERROR:",str(e),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
