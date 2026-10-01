from http.server import BaseHTTPRequestHandler,HTTPServer
import json,uuid
JOBS={}
class H(BaseHTTPRequestHandler):
 def sendj(self,c,o):
  b=json.dumps(o).encode();self.send_response(c);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if self.path=="/system_stats":return self.sendj(200,{"devices":[{"name":"MOCK-GPU","type":"cuda"}]})
  if self.path=="/object_info":return self.sendj(200,{x:{} for x in ["CLIPTextEncode","LoadImage","CreateVideo","SaveVideo"]})
  if self.path.startswith("/history/"):
   p=self.path.rsplit("/",1)[1];return self.sendj(200,{p:{"status":{"status_str":"success","completed":True},"outputs":{"58":{"videos":[{"filename":"mock.mp4","subfolder":"","type":"output"}]}}}} if p in JOBS else {})
  return self.sendj(404,{"error":"not found"})
 def do_POST(self):
  n=int(self.headers.get("Content-Length","0"));raw=self.rfile.read(n)
  if self.path=="/upload/image":return self.sendj(200,{"name":"mock_input.png","subfolder":"","type":"input"})
  if self.path=="/prompt":
   try:body=json.loads(raw);assert isinstance(body.get("prompt"),dict)
   except Exception:return self.sendj(400,{"error":"invalid prompt"})
   p=str(uuid.uuid4());JOBS[p]=1;return self.sendj(200,{"prompt_id":p})
  return self.sendj(404,{"error":"not found"})
 def log_message(self,*a):pass
if __name__=="__main__":HTTPServer(("127.0.0.1",8189),H).serve_forever()
