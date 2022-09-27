from models.user import User

"""Methods only used for unit testing."""
def get_all_users():
    try:
        users = User.objects.all()
        return users
    except User.DoesNotExist:
        return None

def delete_all_users():
    users = get_all_users()
    if users:
        for user in users:
            user.delete()