from fastapi import APIRouter, HTTPException

from database_ai.db import supabase
from database_ai.schemas import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])
TABLE = "products"


@router.get("", response_model=list[ProductResponse], summary="상품 목록 조회")
def list_products():
    response = supabase.table(TABLE).select("*").order("id").execute()
    return response.data


@router.get("/{product_id}", response_model=ProductResponse, summary="상품 단건 조회")
def get_product(product_id: int):
    response = supabase.table(TABLE).select("*").eq("id", product_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
    return response.data[0]


@router.post("", response_model=ProductResponse, status_code=201, summary="상품 생성")
def create_product(payload: ProductCreate):
    response = supabase.table(TABLE).insert(payload.model_dump()).execute()
    return response.data[0]


@router.patch("/{product_id}", response_model=ProductResponse, summary="상품 수정")
def update_product(product_id: int, payload: ProductUpdate):
    data = payload.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="수정할 값이 없습니다")

    response = supabase.table(TABLE).update(data).eq("id", product_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
    return response.data[0]


@router.delete("/{product_id}", status_code=204, summary="상품 삭제")
def delete_product(product_id: int):
    response = supabase.table(TABLE).delete().eq("id", product_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
