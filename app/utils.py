from passlib.context import CryptContext
#what hashing algorithm? we're using Bcrypt here
pwd_context = CryptContext(schemes=["bcrypt"],deprecated= "auto") 


def hash_pass(password : str):
    return pwd_context.hash(password)

def compare_pass(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)