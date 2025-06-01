from fastapi import  HTTPException
from sqlalchemy.orm import Session as f_Session
from database.connection import  Session
session = Session()

def get_object_by_id(model, obj_id, id_field='id' ,   not_found_msg='Object not found', session: f_Session = session):
    obj = session.query(model).filter(getattr(model, id_field) == obj_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=not_found_msg)
    return obj

def validate_param(param, valid_params):
    if param not in valid_params:
        raise HTTPException(status_code=400, detail=f"Invalid parameter: {param}")

def set_and_commit(obj, param, value):
    try:
        setattr(obj, param, value)
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def commit_session():
    try: 
        session.commit() 
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def apply_updates(instance, update_data, allowed_fields):
    updated = False
    for field, value in update_data.dict(exclude_unset=True).items():
        if field in allowed_fields and value is not None:
            setattr(instance, field, value)
            updated = True
    return updated

def handle_update_response(updated):
    if not updated:
        raise HTTPException(status_code=400, detail="No data provided to update")

def get_updatable_fields(model, exclude_fields=["id"]):
    return [column.name for column in model.__table__.columns if column.name not in exclude_fields]
