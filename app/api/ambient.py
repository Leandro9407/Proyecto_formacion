from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user) #autorizacion (candadito)
):   
    if current_user.id_rol == 2:
        if user.id_rol == 1 or user.id_rol == 2:
             raise HTTPException(status_code=401, detail="Usuario no autorizado")

    if current_user.id_rol == 3:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")  
    try:
        user_validate = crud_users.get_user_by_email(db, user.correo)
        if user_validate:
            raise HTTPException(status_code=400, detail="Correo ya registrado")
        
        crud_users.create_user(db, user)
        return {"message": "Usuario creado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
