from fastapi import APIRouter, HTTPException

from database_ai.db import supabase
from database_ai.schemas import MemberCreate, MemberResponse, MemberUpdate

router = APIRouter(prefix="/members", tags=["members"])
TABLE = "members"

@router.get("", response_model=list[MemberResponse], summary="회원 목록 조회")
def list_members():
    response = supabase.table(TABLE).select("*").order("id").execute()
    return response.data


@router.get("/{member_id}", response_model=MemberResponse, summary="회원 단건 조회")
def get_member(member_id: int):
    response = supabase.table(TABLE).select("*").eq("id", member_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다")
    return response.data[0]


@router.post("", response_model=MemberResponse, status_code=201, summary="회원 생성")
def create_member(payload: MemberCreate):
    response = supabase.table(TABLE).insert(payload.model_dump()).execute()
    return response.data[0]


@router.patch("/{member_id}", response_model=MemberResponse, summary="회원 수정")
def update_member(member_id: int, payload: MemberUpdate):
    data = payload.model_dump(exclude_none=True)
    if not data:
        raise HTTPException(status_code=400, detail="수정할 값이 없습니다")

    response = supabase.table(TABLE).update(data).eq("id", member_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다")
    return response.data[0]


@router.delete("/{member_id}", status_code=204, summary="회원 삭제")
def delete_member(member_id: int):
    response = supabase.table(TABLE).delete().eq("id", member_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다")

    