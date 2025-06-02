from fastapi import APIRouter,HTTPException, Path, Query
from database.connection import Session
from models.organization import Organization
from schemas.base_schemas import UpdateParam,MultiUpdate
from schemas.organization_schemas import OrgCreate
from controllers.base_controller import get_object_by_id,get_updatable_fields,commit_session,set_and_commit,validate_param
from fastapi import Query
from sqlalchemy.exc import IntegrityError, OperationalError,ProgrammingError



router = APIRouter()
session = Session()


@router.post("/create")
def create_org(org: OrgCreate):
    """
    Creates a new organization.

    Args:
        org (OrgCreate): Organization name.

    Returns:
        dict: Success message with organization ID.

    Raises:
        HTTPException: If validation fails or a database error occurs.
    """
    session = Session()
    try:
        # Validate organization name
        if not org.name.strip():
            raise HTTPException(status_code=400, detail="Invalid organization name: Cannot be empty.")

        new_org = Organization(name=org.name)

        session.add(new_org)
        session.commit()
        session.refresh(new_org)  # Ensure returning latest organization data

        return {"message": "Organization created successfully", "organization_id": new_org.id}

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Duplicate entry: Organization already exists.")

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred.")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create organization: {str(e)}")

    finally:
        session.close()


@router.get("/organizations/{page_number}")
def get_orgs(
    page_number: int = Path(..., gt=0, description="Page number must be greater than 0"), 
    limit: int = Query(10, gt=0, description="Results per page")
):
    """
    Retrieves a paginated list of organizations.

    Args:
        page_number (int): The page number (must be >= 1).
        limit (int): The number of organizations per page.

    Returns:
        dict: A list of organizations with pagination metadata.

    Raises:
        HTTPException: If no organizations exist or a database error occurs.
    """
    session = Session()
    try:
        # Get total organizations count
        total_orgs = session.query(Organization).count()
        total_pages = max(1, (total_orgs + limit - 1) // limit)  # Ensure at least one page exists

        # Handle empty results gracefully
        if total_orgs == 0:
            return {
                "total_organizations": 0,
                "total_pages": 1,
                "current_page": page_number,
                "organizations": []
            }

        # Validate requested page
        if page_number > total_pages:
            raise HTTPException(status_code=404, detail="Page number exceeds total pages.")

        # Fetch paginated results
        offset = (page_number - 1) * limit
        orgs = session.query(Organization).offset(offset).limit(limit).all()

        return {
            "total_organizations": total_orgs,
            "total_pages": total_pages,
            "current_page": page_number,
            "organizations": orgs
        }

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Database integrity error occurred.")

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred.")

    except ProgrammingError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database query error occurred.")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    finally:
        session.close()
        
@router.delete("/organization/{org_id}")
def delete_organization(org_id: int):
    """
    Deletes an organization from the database.

    Args:
        org_id (int): The ID of the organization to be deleted.

    Returns:
        dict: Success message if deletion is completed.

    Raises:
        HTTPException: If organization not found or a database error occurs.
    """
    session = Session()
    try:
        # Retrieve organization
        organization = session.query(Organization).filter(Organization.id == org_id).first()

        # Handle organization not found
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")

        session.delete(organization)
        session.commit()

        return {"message": "Organization deleted successfully", "organization_id": org_id}

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Deletion conflicts with database constraints")

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    finally:
        session.close()

@router.put("/organization/{org_id}")
def update_organization(org_id: int, update: UpdateParam):
    """
    Updates an organization's details.

    Args:
        org_id (int): The ID of the organization to be updated.
        update (UpdateParam): Parameter and value to update.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If validation fails, organization is not found, or a database error occurs.
    """
    session = Session()
    try:
        # Retrieve organization
        org = get_object_by_id(Organization, org_id, not_found_msg="Organization not found")

        valid_params = get_updatable_fields(Organization)

        # Validate provided parameter
        if not update.param or update.param not in valid_params:
            raise HTTPException(status_code=400, detail=f"Invalid update parameter: {update.param}")

        set_and_commit(org, update.param, update.value)
        
        return {"message": "Organization updated successfully", "updated_field": update.param, "new_value": update.value}

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Update conflicts with database constraints")

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update organization: {str(e)}")

    finally:
        session.close()

@router.get("/search/{name}")
def search_organizations(name: str):
    """
    Searches for organizations by name (case-insensitive).

    Args:
        name (str): Partial or full name to search for.

    Returns:
        dict: A list of matching organizations.

    Raises:
        HTTPException: If no organizations are found or a database error occurs.
    """
    session = Session()
    try:
        # Validate input: Ensure name is not empty or just whitespace
        if not name.strip():
            raise HTTPException(status_code=400, detail="Invalid search query: Name cannot be empty.")

        orgs = session.query(Organization).filter(Organization.name.ilike(f"%{name}%")).all()

        # Handle empty search result
        if not orgs:
            raise HTTPException(status_code=404, detail="No organizations found with that name.")

        return {"organizations": orgs}

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred.")

    except ProgrammingError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database query error occurred.")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    finally:
        session.close()