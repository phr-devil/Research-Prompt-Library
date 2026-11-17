#!/usr/bin/env python3
"""Simple F11 example: one-row pipeline; pure Python standard library."""
import json
from pathlib import Path
from xml.etree import ElementTree as ET
HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
NS = "http://www.w3.org/2000/svg"
Q = lambda t: "{"+NS+"}"+t
ET.register_namespace("", NS)
def main():
    spec=json.loads((HERE/"figure_spec.example.json").read_text(encoding="utf-8"))
    assets={x["id"]: x for x in json.loads((ASSETS/"manifest.json").read_text(encoding="utf-8"))["assets"]}
    nodes=spec["nodes"]
    if len(nodes)<2 or len(nodes)>8: raise ValueError("Demo supports 2-8 nodes")
    w=40+len(nodes)*210
    doc=ET.Element(Q("svg"),viewBox="0 0 %s 290"%w,width=str(w),height="290")
    ET.SubElement(doc,Q("title")).text=spec["title"]
    ET.SubElement(doc,Q("rect"),x="0",y="0",width=str(w),height="290",fill="#fff")
    defs=ET.SubElement(doc,Q("defs"))
    mark=ET.SubElement(defs,Q("marker"),id="a",markerWidth="10",markerHeight="10",refX="8",refY="5",orient="auto")
    ET.SubElement(mark,Q("path"),d="M1 1 L8 5 L1 9",stroke="#445",fill="none")
    for i,n in enumerate(nodes):
        x=20+i*210
        if i:
            ET.SubElement(doc,Q("path"),d="M%d 147 H%d"%(x-30,x),stroke="#445",fill="none",
                          **{"marker-end":"url(#a)"})
        ET.SubElement(doc,Q("rect"),x=str(x),y="35",width="180",height="220",rx="8",
                      fill=n["fill"],stroke="#8a96a0")
        ET.SubElement(doc,Q("text"),x=str(x+90),y="66",fill="#273442",
                      style="bold 18px Arial,sans-serif",**{"text-anchor":"middle"}).text=n["label"]
        item=assets[n["icon"]]
        asset=(ASSETS/item["path"]).resolve()
        if not asset.is_relative_to(ASSETS.resolve()): raise ValueError("Unsafe asset path")
        pic=ET.parse(asset).getroot()
        if pic.tag!=Q("svg"): raise ValueError("Invalid SVG")
        for el in pic.iter():
            if el.tag.rsplit("}",1)[-1].lower() in ("script","image","foreignobject","iframe","use"):
                raise ValueError("Unsafe SVG element")
            if any(k.lower().startswith("on") or k.lower().endswith("}href") for k in el.attrib):
                raise ValueError("Unsafe SVG attr")
        # OpenMoji files reuse SVG ids; prefix them for safe inlining.
        for j, element in enumerate(pic.iter()):
            if "id" in element.attrib:
                element.set("id", f"f11-{i}-{j}-" + element.get("id"))
        pic.attrib.update(x=str(x+27),y="79",width="126",height="126")
        doc.append(pic)
    svg=ET.tostring(doc,encoding="unicode")
    out=HERE/"out";out.mkdir(exist_ok=True)
    (out/"figure.svg").write_text(svg,encoding="utf-8")
    html='<!doctype html><meta charset="utf-8"><style>svg{width:100%;height:auto}</style>'+svg
    (out/"figure.html").write_text(html,encoding="utf-8")
    print("OK:",out/"figure.svg",out/"figure.html")
if __name__=="__main__":main()
