from fastapi import APIRouter,HTTPException
from database.connection import Session
from models.organization import Organization
from schemas.base_schemas import UpdateParam,MultiUpdate
from schemas.organization_schemas import OrgCreate
from controllers.base_controller import get_object_by_id,get_updatable_fields,commit_session,set_and_commit,validate_param


router = APIRouter()
session = Session()


@router.post("/orgs")
def create_org(org: OrgCreate):
    try:
        session_org = Organization(name=org.name)
        session.add(session_org)
        session.commit()
        return {"message": "Organization created successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/orgs/{page_number}/{limit}")
def get_org(page_number: int, limit: int):
    try:
        offset = (page_number - 1) * limit
        orgs = session.query(Organization).offset(offset).limit(limit).all()
        return orgs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/orgs/{org_id}")
def del_org(org_id: int):
    try:
        session_org = session.query(Organization).filter(Organization.id == org_id).first()
        if not session_org:
            raise HTTPException(status_code=404, detail="Organization not found")
        session.delete(session_org)
        session.commit()
        return {"message": "Organization deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/orgs/{org_id}")
def update_org(org_id: int, update: UpdateParam):
    try:
        org = get_object_by_id(Organization, org_id, not_found_msg="Organization not found")
        valid_params = get_updatable_fields(Organization)
        validate_param(update.param, valid_params)
        set_and_commit(org, update.param, update.value)
        return {"message": "Organization updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search_orgs/{name}")
def search_orgs(name: str):
    try:
        orgs = session.query(Organization).filter(Organization.name.ilike(f"%{name}%")).all()
        if not orgs:
            raise HTTPException(status_code=404, detail="No organizations found with that name")
        return orgs
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))