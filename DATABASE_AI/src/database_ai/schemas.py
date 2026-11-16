"""요청·응답 모양을 정의하는 Pydantic 모델.

테이블마다 세 가지로 나눈다.
  Create   : POST 본문 — id·created_at 은 DB가 만드니 받지 않는다
  Update   : PATCH 본문 — 일부만 고칠 수 있어야 하므로 전부 None 허용
  Response : 응답 — DB가 채운 id·created_at 까지 포함
"""

from datetime import datetime

from pydantic import BaseModel


# ---------- 회원 ----------
class MemberCreate(BaseModel):
    email: str
    name: str


class MemberUpdate(BaseModel):
    email: str | None = None
    name: str | None = None


class MemberResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime


# ---------- 상품 ----------
class ProductCreate(BaseModel):
    name: str
    price: int
    stock: int = 0


class ProductUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    stock: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    created_at: datetime


# ---------- 주문 ----------
class OrderCreate(BaseModel):
    member_id: int
    product_id: int
    quantity: int = 1


class OrderUpdate(BaseModel):
    member_id: int | None = None
    product_id: int | None = None
    quantity: int | None = None


class OrderResponse(BaseModel):
    id: int
    member_id: int
    product_id: int
    quantity: int
    created_at: datetime
