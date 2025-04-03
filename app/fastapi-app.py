import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.rest.hosts_router import hosts_router
from app.rest.index_router import index_router

app = FastAPI()
app.include_router(hosts_router)
app.include_router(index_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":  # for debugging
    uvicorn.run(app, host="127.0.0.1", port=8000)
