from contextlib import asynccontextmanager

from app import config

from fastapi import FastAPI

from app.health.presentation.health_controller import router as health_router
from app.middleware.http_logging import HTTPLoggingMiddleware
from app.sales.presentation.sales_controller import router as dashboard_router
from fastapi.middleware.cors import CORSMiddleware

api_prefix = f"/api"

def create_app() -> FastAPI:
    env = config.ENV
    app = FastAPI(
        title="API",
        debug=(env == "development"),
        docs_url=f"{api_prefix}/docs",
        redoc_url=f"{api_prefix}/redoc",
        root_path=api_prefix,
    )

    origins = [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    #app.add_middleware(HTTPLoggingMiddleware)

    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(dashboard_router, prefix="/sales", tags=["dashboard"])

    return app
