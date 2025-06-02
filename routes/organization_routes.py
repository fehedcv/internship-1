from fastapi import APIRouter,HTTPException
from database.connection import Session
from models.organization import Organization
from schemas.base_schemas import UpdateParam,MultiUpdate
from schemas.organization_schemas import OrgCreate
from controllers.base_controller import get_object_by_id,get_updatable_fields,commit_session,set_and_commit,validate_param


router = APIRouter()
session = Session()


@router.post("/create")
def create_org(org: OrgCreate):
    #create organization
    try:
        session_org = Organization(name=org.name)
        session.add(session_org)
        session.commit()
        return {"message": "Organization created successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import Query

@router.get("/{page_number}")
def get_org(page_number: int, limit: int = Query(10)):
    if page_number < 1:
        raise HTTPException(status_code=400, detail="Invalid page number. Must be >= 1.")
    
    session = Session()
    try:
        total_orgs = session.query(Organization).count()
        total_pages = (total_orgs + limit - 1) // limit  # ceiling division

        if page_number > total_pages and total_orgs != 0:
            raise HTTPException(status_code=404, detail="Page not found.")

        offset = (page_number - 1) * limit
        orgs = session.query(Organization).offset(offset).limit(limit).all()
        return orgs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
        
@router.delete("/{org_id}")
def del_org(org_id: int):
    #delete organization
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

@router.put("/{org_id}")
def update_org(org_id: int, update: UpdateParam):
    #update organization
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

@router.get("/search/{name}")
def search_orgs(name: str):
    #search for organizations by name
    try:
        orgs = session.query(Organization).filter(Organization.name.ilike(f"%{name}%")).all()
        if not orgs:
            raise HTTPException(status_code=404, detail="No organizations found with that name")
        return orgs
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))