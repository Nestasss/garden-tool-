from database import get_user_role

def check_permission(user_id, required_role):
    user_role = get_user_role(user_id)
    if not user_role:
        return False
    role_hierarchy = {"observer": 0, "worker": 1, "admin": 2}
    return role_hierarchy.get(user_role, -1) >= role_hierarchy.get(required_role, -1)

def can_create_task(user_id):
    return check_permission(user_id, "worker")

def can_send_to_chat(user_id):
    return check_permission(user_id, "worker")

def can_manage_calendar(user_id):
    return check_permission(user_id, "admin")
