from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import get_current_user
from core.database import get_db
from app.schemas.ambient import AmbientCreate, AmbientUpdate, AmbientOut
from app.crud import ambient as crud_ambient
from app.schemas.users import UserCreate, UserOut
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.crud import users as crud_users

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_ambient(
    ambiente: AmbientCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        crud_ambient.create_ambient(db, ambiente)
        return {"message": "Ambiente creado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{id_ambiente}")
def update_ambient(
    id_ambiente: int,
    ambiente: AmbientUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        success = crud_ambient.update_ambient(db, id_ambiente, ambiente.model_dump(exclude_unset=True))
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el ambiente")
        return {"message": "Ambiente actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-by-id/{id_ambiente}", response_model=AmbientOut)
def get_ambient_by_id(
    id_ambiente: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        ambiente = crud_ambient.get_ambient_by_id(db, id_ambiente)
        if not ambiente:
            raise HTTPException(status_code=404, detail="Ambiente no encontrado")
        return ambiente
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status-activate-by-centro", response_model=List[AmbientOut])
def get_ambient_by_centro(
    cod_centro: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        ambientes = crud_ambient.get_ambient_by_centro(db, cod_centro)
        if not ambientes:
            raise HTTPException(status_code=404, detail="No se encontraron ambientes activos para este centro")
        return ambientes
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/modify-status/{id_ambiente}")
def modify_status_ambient(
    id_ambiente: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol not in [1, 2]:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        crud_ambient.modify_status_ambient(db, id_ambiente)
        return {"message": "Estado del ambiente modificado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
