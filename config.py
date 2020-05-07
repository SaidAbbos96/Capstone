import os

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

auth0_config = {
    "AUTH0_DOMAIN": "kuberx.auth0.com",
    "ALGORITHMS": ["RS256"],
    "API_AUDIENCE": "caps_id",
}

