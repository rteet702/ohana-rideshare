from flask_app import app
from flask_app.controllers import login_registration, rides


if __name__ == '__main__':
    app.run(debug=True)