## Key Management System

import redis
import os
# Password handling
from cryptography.fernet import Fernet
from getpass import getpass
# Environment Variables
from dotenv import load_dotenv, dotenv_values

load_dotenv()

config = {
    **dotenv_values(".env.redis"),  # load redis variables
    **os.environ  # override loaded values with environment variables
}

# KMS -------------------------------------
def kms():

    env_data = dotenv_values(".env.redis")

    r = redis.Redis(
        host = env_data.get("REDIS_HOST"),
        port = int(env_data.get("REDIS_PORT")),
        password = env_data.get("REDIS_PASSWORD")
    )


    if not r.get("encryption_key"):
        encryption_key = Fernet.generate_key()
        r.set("encryption_key", encryption_key)

    encryption_key = r.get("encryption_key")
    fernet = Fernet(encryption_key)

    return fernet