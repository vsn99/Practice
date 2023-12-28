from flask import Flask
from user import user_bp
from calc import calc_bp
from currency import currency_bp
from auth import roles_required

app = Flask(__name__)

# ... Other configurations

app.register_blueprint(user_bp)
app.register_blueprint(calc_bp)
app.register_blueprint(currency_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
