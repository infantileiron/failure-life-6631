from fastapi import APIRouter,Depends
from src.controllers import rule as controller
from src.schemas.entities import RuleInput
from src.services.auth import current,editor
router=APIRouter(prefix='/rules',tags=['rules'])
@router.get('')
def list_items(user=Depends(current)):return controller.list_items()
@router.post('',status_code=201)
def create(data:RuleInput,user=Depends(editor)):return controller.create(data)
