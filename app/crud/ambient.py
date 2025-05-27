import logging
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.ambient import AmbientCreate

logger = logging.getLogger(__name__)

def Create_ambient(db: Session, Ambient: AmbientCreate) -> Optional[bool]:
    try:
        query = text("""
            INSERT INTO ambiente_formacion (
                nombre_ambiente, num_max_aprendices, municipio,
                ubicacion, cod_centro, estado
            ) VALUES (
                :nombre_ambiente, :num_max_aprendices, :municipio,
                :ubicacion, :cod_centro, :estado
            )
        """)
        db.execute(query, Ambient.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear ambiente: {e}")
        raise Exception("Error de base de datos al crear el ambiente")

def update_ambient(db: Session, id_ambient: int, ambient_data: dict) -> Optional[bool]:
    try:
        query = text("""
            UPDATE ambiente_formacion
            SET nombre_ambiente = :nombre_ambiente,
                num_max_aprendices = :num_max_aprendices,
                municipio = :municipio,
                ubicacion = :ubicacion,
                cod_centro = :cod_centro,
                estado = :estado
            WHERE id_ambiente = :id_ambient
        """)
        ambient_data['id_ambient'] = id_ambient
        db.execute(query, ambient_data)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar ambiente: {e}")
        raise Exception("Error de base de datos al actualizar el ambiente")

def get_ambient_by_id(db: Session, id_ambient: int):
    try:
        query = text("""SELECT id_ambiente, nombre_ambiente, num_max_aprendices, municipio,
                        ubicacion, cod_centro, estado
                     FROM ambiente_formacion 
                     WHERE id_ambiente = :id""")
        result = db.execute(query, {"id": id_ambient}).mappings().first()
        if not result:
            return None
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener ambiente por ID: {e}")
        raise Exception("Error de base de datos al obtener el ambiente")

def get_ambientes_activos_por_centro(db: Session, cod_centro: int):
    try:
        query = text("""
            SELECT id_ambiente, nombre_ambiente, num_max_aprendices, municipio,
                   ubicacion, cod_centro, estado
            FROM ambiente_formacion
            WHERE cod_centro = :cod_centro AND estado = TRUE
        """)
        result = db.execute(query, {"cod_centro": cod_centro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener ambientes activos por centro: {e}")
        raise Exception("Error de base de datos al obtener los ambientes activos")


def modificar_estado_ambiente(db: Session, id_ambiente: int):
    try:
        query = text("""
            UPDATE ambiente_formacion SET estado = IF(estado, FALSE, TRUE)
            WHERE id_ambiente = :id_ambiente
        """)
        db.execute(query, {"id_ambiente": id_ambiente})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al modificar el estado del ambiente: {e}")
        raise Exception("Error de base de datos al modificar el estado del ambiente")

