from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions.business import BaseException
from web.router import auth_router, base_router

app = FastAPI()


@app.exception_handler(BaseException)
async def exception_handler(_: Request, exc: BaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "code": exc.code},
    )


app.include_router(auth_router)
app.include_router(base_router)
