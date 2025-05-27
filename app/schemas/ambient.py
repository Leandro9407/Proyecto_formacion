from typing import Optional
from pydantic import BaseModel, Field


class AmbienteBase(BaseModel):
    nombre_ambiente: str = Field(min_length=3, max_length=80)
    num_max_aprendices: int = Field(le=30)
    municipio: str = Field(min_length=3, max_length=80)
    ubicacion: str = Field(min_length=3, max_length=80)
    cod_centro: int

class AmbienteCreate(AmbienteBase):
    estado: bool

class AmbienteUpdate(BaseModel):    
    nombre_ambiente: Optional[str] = Field(min_length=3, max_length=80)
    num_max_aprendices: Optional[int] = Field(le=30)
    municipio: Optional[str] = Field(min_length=3, max_length=80)
    ubicacion: Optional[str] = Field(min_length=3, max_length=80)
    cod_centro: Optional[int] 
    estado: Optional[bool]

class AmbienteOut(AmbienteBase):
    id_ambiente: int