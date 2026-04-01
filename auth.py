from utilis import hash_password, verify_password
from jwt import create_access_token, create_refresh_token, decode_token
from database import DATABASE_URL
from models import UserSignup, UserLogin,UserRefresh
from database import get_cursor

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Helpers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_user_by_email(cursor, email: str):
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Auth functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def register_user(sign: UserSignup) -> dict:
    with get_cursor() as cursor:

        if get_user_by_email(cursor, sign.email):
            return {"error": "Account already exists"}
        
        hashed_password = hash_password(sign.password)

        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                       (sign.name,sign.email,hashed_password))

        return {"Message": "Account registered Successfully"}
    
def login_user(userlogin: UserLogin) -> dict:
    with get_cursor() as cursor:
        user = get_user_by_email(cursor, userlogin.email)

        if not user or not verify_password(userlogin.password, user["password"]):
            return {"error": "Invalid email or password"}
        

        token_data = {"sub": user["email"], "name": user["name"]}

        return {
            "access_token": create_access_token(token_data),
            "refresh_token": create_refresh_token(token_data),
            "token_type": "bearer",
        }
        
        
def refresh(token: UserRefresh) -> dict:
    payload = decode_token(token.token)
   
    if payload.get("token_type") != "refresh":
        return {"error": "Invalid token"}
    
    email = payload.get("sub")

    with get_cursor() as cursor:
        user = get_user_by_email(cursor, email)

        if not user:
            return {"error": "User not found"}
        
        return{
        "access_token": create_access_token({
            "sub": user["email"],
            "name": user["name"],
        }),
        "token_type": "bearer",
    }
