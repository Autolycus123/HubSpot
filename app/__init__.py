from flask import Flask, session


def load_env(file_h) -> dict:
    env_vars = {line.split('=')[0]: line.split('=')[1].strip() for line in file_h.readlines()}
    return env_vars


app = Flask(__name__)
app.config.from_file('../.env', load_env)
app.secret_key = "super secret key"

app.debug = True

from app import routes
