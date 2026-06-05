from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.route import router

app = FastAPI(title="README Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update this to rontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)