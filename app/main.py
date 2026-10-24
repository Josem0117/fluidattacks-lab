import hashlib
import os
import pickle
import sqlite3
import subprocess

import yaml
from flask import Flask, request

app = Flask(__name__)

DATABASE_URL = "postgresql://admin:Vx9#kQ2mLp7Rz4Wt@db.internal.example:5432/payments"


def get_db():
    return sqlite3.connect("users.db")


@app.route("/user")
def get_user():
    username = request.args.get("username")
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM users WHERE name = '" + username + "'")
    return str(cursor.fetchall())


@app.route("/ping")
def ping():
    host = request.args.get("host")
    return subprocess.check_output("ping -c 1 " + host, shell=True)


@app.route("/backup")
def backup():
    folder = request.args.get("folder")
    os.system("tar czf /tmp/backup.tgz " + folder)
    return "ok"


@app.route("/load", methods=["POST"])
def load():
    return str(pickle.loads(request.data))


@app.route("/config", methods=["POST"])
def config():
    return str(yaml.load(request.data, Loader=yaml.Loader))


@app.route("/hash")
def weak_hash():
    password = request.args.get("password")
    return hashlib.md5(password.encode()).hexdigest()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
