import os
from gevent.pywsgi import WSGIServer
print("start load app!")
from ss14tts import app,WarmUp,model,example_text

print("init!")

http_server = WSGIServer(("0.0.0.0", int(os.environ.get("PORT","5000"))), app)
WarmUp(model,example_text)
print("run!")
http_server.serve_forever()