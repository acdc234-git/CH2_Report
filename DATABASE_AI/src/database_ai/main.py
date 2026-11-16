"""FastAPI 앱 조립 지점.

실행: uv run uvicorn database_ai.main:app --reload
문서: http://localhost:8000/docs
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from postgrest.exceptions import APIError

from database_ai.routers import members, orders, products

app = FastAPI(
    title="쇼핑몰 CRUD",
    description="Supabase + FastAPI — 회원·상품·주문 3개 테이블 CRUD",
    version="0.1.0",
)

app.include_router(members.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.exception_handler(APIError)
def handle_supabase_error(request: Request, error: APIError) -> JSONResponse:
    """Supabase 오류를 빈 500 대신 읽을 수 있는 메시지로 돌려준다."""
    return JSONResponse(
        status_code=400,
        content={
            "detail": error.message,
            "code": error.code,
            "hint": error.hint,
            "details": error.details,
        },
    )


@app.get("/", tags=["health"], summary="헬스 체크")
def root():
    return {"status": "ok"}
