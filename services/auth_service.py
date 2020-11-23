from services.crypt_service import pwd_context
from models.user import User


# Used to authenticate a user against the users table
def sign_in(email, password):

    # Try to find a user with matching credentials
    db_user = User.query.filter_by(email=email, active=True).first()

    if not db_user:
        return None

    # Verify the provided password with the hashed value
    valid_password = pwd_context.verify(password, db_user.password)

    if not valid_password:
        return None

    return db_user
