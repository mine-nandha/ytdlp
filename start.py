import os
from uvicorn import Config, Server
from app.main import app

port = int(os.getenv("PORT", "8000"))
cfg = Config(app=app, host="0.0.0.0", port=port)
Server(cfg).run()