from fastapi import APIRouter, HTTPException
from postgrest.exceptions import APIError

from database_ai.db import supabase
from database_ai.schemas import OrderCreate, OrderResponse, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])
TABLE = "orders"

# FK 위반(없는 회원·상품 참조) 시 PostgreSQL 에러 코드
FK_VIOLATION = "23503"


def _handle_fk(error: APIError) -> None:
    """외래키 위반이면 400으로 바꿔 던진다. 그 밖의 오류는 그대로 올린다."""
    if error.code == FK_VIOLATION:
        raise HTTPException(
            status_code=400,
            detail="존재하지 않는 회원 또는 상품입니다 (외래키 제약 위반)",
        )
    raise HTTPException(status_code=400, detail=error.message)


@router.get("", response_model=list[OrderResponse], summary="주문 목록 조회")
def list_orders():
    response = supabase.table(TABLE).select("*").order("id").execute()
    return response.data


@router.get("/{order_id}", response_model=OrderResponse, summary="주문 단건 조회")
def get_order(order_id: int):
    response = supabase.table(TABLE).select("*").eq("id", order_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")
    return response.data[0]


@router.post("", response_model=OrderResponse, status_code=201, summary="주문 생성")
def create_order(payload: OrderCreate):
    try:
        response = supabase.table(TABLE).insert(payload.model_dump()).execute()
    except APIError as error:
        _handle_fk(error)
    return response.data[0]


@router.patch("/{order_id}", response_model=OrderResponse, summary="주문 수정")
def update_order(order_id: int, payload: OrderUpdate):
    data = payload.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="수정할 값이 없습니다")

    try:
        response = supabase.table(TABLE).update(data).eq("id", order_id).execute()
    except APIError as error:
        _handle_fk(error)
    if not response.data:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")
    return response.data[0]


@router.delete("/{order_id}", status_code=204, summary="주문 삭제")
def delete_order(order_id: int):
    response = supabase.table(TABLE).delete().eq("id", order_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")
