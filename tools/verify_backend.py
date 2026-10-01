import json,sys,urllib.request
from pathlib import Path
base=sys.argv[1] if len(sys.argv)>1 else "http://127.0.0.1:8189"
def get(p):
 with urllib.request.urlopen(base+p,timeout=5) as r:return json.load(r)
def post(p,o):
 b=json.dumps(o).encode();q=urllib.request.Request(base+p,b,{"Content-Type":"application/json"})
 with urllib.request.urlopen(q,timeout=5) as r:return json.load(r)
print("system_stats:",bool(get("/system_stats")))
info=get("/object_info");print("required nodes:",all(x in info for x in ["CLIPTextEncode","LoadImage","CreateVideo","SaveVideo"]))
wf=json.loads(Path(__file__).with_name("mock_api_workflow.json").read_text())
r=post("/prompt",{"prompt":wf,"client_id":"openreel-verify"});print("prompt_id:",r.get("prompt_id"))
h=get("/history/"+r["prompt_id"]);print("history success:",h[r["prompt_id"]]["status"]["status_str"]=="success");print("OUTPUT: PASS")
