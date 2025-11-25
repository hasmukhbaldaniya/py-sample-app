import uvicorn
from fastapi import FastAPI

from app.db.client import DBClient
from app.routers import v1_router

app = FastAPI(title="sample app", version="0.0.1")

def initialize_application_resources(app: FastAPI):
    print("initialize_application_resources")
    DBClient.initialise(app)

"""Configure startup event"""
app.add_event_handler("startup", lambda: initialize_application_resources(app))

app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Hi")