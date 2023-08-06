import vecspace
import vecspace.config
from vecspace.server.fastapi import FastAPI

settings = vecspace.config.Settings()
server = FastAPI(settings)
app = server.app()
