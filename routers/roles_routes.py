from fastapi import APIRouter,HTTPException
from database.connection import Session
from schemas.roles_schemas import RoleCreate,AssignUserRole
from schemas.base_schemas import UpdateParam
from models.user import UserRole,Role
from controllers.base_controller import commit_session,set_and_commit,get_object_by_id,get_updatable_fields,validate_param
from sqlalchemy.exc import IntegrityError, OperationalError,ProgrammingError

router = APIRouter()


@router.post("/create")
def create_role(new_role: RoleCreate):
    """
    Creates a new role.

    Args:
        new_role (RoleCreate): Role name.

    Returns:
        dict: Success message with role ID.

    Raises:
        HTTPException: If validation fails or a database error occurs.
    """
    session = Session()
    try:
        # Validate role name
        if not new_role.name.strip():
            raise HTTPException(status_code=400, detail="Invalid role name: Cannot be empty.")

        role = Role(name=new_role.name)

        session.add(role)
        session.commit()
        session.refresh(role)  # Ensure returning latest role data

        return {"message": "Role created successfully", "role_id": role.id}

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Duplicate entry: Role already exists.")

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred.")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create role: {str(e)}")

    finally:
        session.close()


@router.get("/roles")
def get_roles():
    """
    Fetches all available roles.

    Returns:
        dict: List of roles.

    Raises:
        HTTPException: If a database error occurs.
    """
    session = Session()
    try:
        roles = session.query(Role).all()

        # Handle empty results
        if not roles:
            raise HTTPException(status_code=404, detail="No roles found.")

        return {"roles": roles}

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred.")

    except ProgrammingError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database query error occurred.")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch roles: {str(e)}")

    finally:
        session.close()



@router.post("/assign")
def assign_role(assign: AssignUserRole):
    """
    Assigns a role to a user.

    Args:
        assign (AssignUserRole): User ID and Role ID to be assigned.

    Returns:
        dict: Success message confirming role assignment.

    Raises:
        HTTPException: If assignment fails due to validation or database errors.
    """
    session = Session()
    try:
        # Validate input parameters
        if not assign.user_id or not assign.role_id:
            raise HTTPException(status_code=400, detail="Invalid input: user_id and role_id are required.")

        assign_role = UserRole(user_id=assign.user_id, role_id=assign.role_id)

        session.add(assign_role)
        session.commit()
        session.refresh(assign_role)  # Ensures returning latest assigned role data

        return {"message": "Role assigned successfully", "assigned_role": {"user_id": assign.user_id, "role_id": assign.role_id}}

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Role assignment conflicts with existing data.")

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred.")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to assign role: {str(e)}")

    finally:
        session.close()


@router.get("/assigned")
def get_assigned_roles():
    """
    Fetches all assigned user roles.

    Returns:
        dict: List of assigned roles.

    Raises:
        HTTPException: If a database error occurs.
    """
    session = Session()
    try:
        assigned_roles = session.query(UserRole).all()

        # Handle empty results
        if not assigned_roles:
            raise HTTPException(status_code=404, detail="No assigned roles found.")

        return {"assigned_roles": assigned_roles}

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred.")

    except ProgrammingError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database query error occurred.")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to fetch assigned roles: {str(e)}")

    finally:
        session.close()


@router.put("/role/{role_id}")
def update_role(role_id: int, update: UpdateParam):
    """
    Updates a role's details.

    Args:
        role_id (int): The ID of the role to be updated.
        update (UpdateParam): Parameter and value to update.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If validation fails, role is not found, or a database error occurs.
    """
    session = Session()
    try:
        # Retrieve role
        role = get_object_by_id(Role, role_id, not_found_msg="Role not found")

        valid_params = get_updatable_fields(Role)

        # Validate provided parameter
        if not update.param or update.param not in valid_params:
            raise HTTPException(status_code=400, detail=f"Invalid update parameter: {update.param}")

        set_and_commit(role, update.param, update.value)
        
        return {"message": "Role updated successfully", "updated_field": update.param, "new_value": update.value}

    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Update conflicts with database constraints")

    except OperationalError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Database operational error occurred")

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update role: {str(e)}")

    finally:
        session.close()