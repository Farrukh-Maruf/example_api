# 18.00
from fastapi import FastAPI
from .import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient

models.Base.metadata.create_all(bind = engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint: register 
# this before routers so it isn't shadowed
@app.get("/")
def root():
    return {"message" :"welcome to my fucking  world"}

# this is how we include routers from different modules, wire them together
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)