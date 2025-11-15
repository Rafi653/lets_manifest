"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.schemas.common import APIResponse, HealthCheck

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RESTful API for Let's Manifest - A comprehensive personal development and manifestation tracking application",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=APIResponse[dict])
async def root():
    """Root endpoint."""
    return APIResponse(
        data={"message": "Welcome to Let's Manifest API"}, message="API is running"
    )


@app.get("/health", response_model=APIResponse[HealthCheck])
async def health_check():
    """Health check endpoint."""
    return APIResponse(
        data=HealthCheck(status="healthy", version=settings.APP_VERSION),
        message="Service is healthy",
    )


# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "data": None,
            "message": "Resource not found",
            "errors": None,
            "meta": {"timestamp": None, "request_id": None},
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "data": None,
            "message": "Internal server error",
            "errors": None,
            "meta": {"timestamp": None, "request_id": None},
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
