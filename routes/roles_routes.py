from fastapi import APIRouter
from database.connection import Session
from schemas.roles_schemas import RoleCreate,AssignUserRole
from schemas.base_schemas import UpdateParam
from models.user import UserRole,Role
from controllers.base_controller import commit_session,set_and_commit,get_object_by_id,get_updatable_fields,validate_param

router = APIRouter()
session = Session()


@router.post("/roles")
def create_user(newRole: RoleCreate):
    new_role = Role(name=newRole.name)
    session.add(new_role)
    session.commit()
    return {"message": "Role created successfully"}

@router.get("/roles")
def get_roles():
    roles = session.query(Role).all()
    return {"Roles": roles}

@router.post("/role_assign")
def assign_role(assign: AssignUserRole):
    assignRole = UserRole(user_id=assign.user_id, role_id=assign.role_id)
    session.add(assignRole)
    commit_session()
    return {"message": "Role assigned successfully"}

@router.get("/assignedRoles")
def get_assigned_roles():
    assigned_roles = session.query(UserRole).all()
    return {"AssignedRoles": assigned_roles}

@router.put("/roles/{role_id}")
def update_role(role_id: int, update: UpdateParam):
    role = get_object_by_id(Role, role_id, not_found_msg="Role not found")
    valid_params = get_updatable_fields(Role)
    validate_param(update.param, valid_params)
    set_and_commit(role, update.param, update.value)
    return {"message": "Role updated successfully"}
