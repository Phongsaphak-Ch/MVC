from fastapi import FastAPI
from App.routes.routes import router
from starlette.middleware.cors import CORSMiddleware
from App.services.generate_csv import check_and_generate_cow_data

app = FastAPI(title="MVC", version="1.0.0", timeout=300)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    check_and_generate_cow_data()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

