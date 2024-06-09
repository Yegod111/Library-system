from flask import Flask
from secrets import token_hex

app = Flask(__name__)
app.secret_key = token_hex(16)