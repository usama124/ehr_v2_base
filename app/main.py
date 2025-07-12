from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import user
from app.core.responses import CustomException

app = FastAPI(
    title="EHR Backend",
    description="Electronic Health Records API with role-based access control",
    version="1.0.0"
)

# CORS middleware (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handling standard HTTP exceptions globally
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "error_code": exc.status_code, "message": exc.detail},
    )


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: Exception):
    status_code = int(exc.code)
    error_code = exc.error_code
    message = exc.message
    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )

app.include_router(user.router, prefix="/user", tags=["User"])
