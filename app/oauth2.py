from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


# Declares that the login endpoint will be the one that the client should use to get the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# Secret Key
# Algorithm
# Expiration time of token

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : expire})

    # Encode the user id, expiration date and secret key into the payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try: 

        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Store the id of the user that was assigned the token
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        # Stores the id of the token as per the TokenData schema
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data



# Pass this as a dependency to every path operation that requires a login
# This will take the token from the request, extract the id, verify it and fetch the user
# Can be added as a parameter to path operations
# Idea behind is that once the token_data is returned from the verify_access_token function, 
# the get_current_user will fetch the user from the database and attach him to the path operation
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    # Looks for the Authorization header in the request and checks if the value is "Bearer"
    # Returns the token as a str
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail=f"Could not validate credentials", 
                                          headers={"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token, credentials_exception)

    # Store the current user that is logged in
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user