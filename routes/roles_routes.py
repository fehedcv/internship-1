from fastapi import APIRouter,HTTPException
from database.connection import Session
from schemas.roles_schemas import RoleCreate,AssignUserRole
from schemas.base_schemas import UpdateParam
from models.user import UserRole,Role
from controllers.base_controller import commit_session,set_and_commit,get_object_by_id,get_updatable_fields,validate_param

router = APIRouter()


@router.post("/create")
def create_role(newRole: RoleCreate):
    #create role
    session = Session()
    try:
        new_role = Role(name=newRole.name)
        session.add(new_role)
        session.commit()
        return {"message": "Role created successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create role: {str(e)}")


@router.get("/")
def get_roles():
    session = Session()
    try:
        roles = session.query(Role).all()
        return {"Roles": roles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch roles: {str(e)}")


@router.post("/assign")
def assign_role(assign: AssignUserRole):
    session = Session()
    try:
        assignRole = UserRole(user_id=assign.user_id, role_id=assign.role_id)
        session.add(assignRole)
        commit_session()
        return {"message": "Role assigned successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to assign role: {str(e)}")


@router.get("/assigned")
def get_assigned_roles():
    session = Session()
    try:
        assigned_roles = session.query(UserRole).all()
        return {"AssignedRoles": assigned_roles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch assigned roles: {str(e)}")


@router.put("/{role_id}")
def update_role(role_id: int, update: UpdateParam):
    session = Session()
    try:
        role = get_object_by_id(Role, role_id, not_found_msg="Role not found")
        valid_params = get_updatable_fields(Role)
        validate_param(update.param, valid_params)
        set_and_commit(role, update.param, update.value)
        return {"message": "Role updated successfully"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update role: {str(e)}")
