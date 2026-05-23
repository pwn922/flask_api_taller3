from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
def login_v2():
    return {"id": 1, "name": "a", "email": "b", "version": "v2"}
