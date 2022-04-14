from flask import Flask, session
from flask_login import LoginManager
from .config import Config
from .db import DB
from flask_session import Session


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = 'filesystem'
    Session(app)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .customer import bp as customer_bp
    app.register_blueprint(customer_bp)

    from .seller import bp as seller_bp
    app.register_blueprint(seller_bp)    

    from .product import bp as product_bp
    app.register_blueprint(product_bp)   

    from .balance import bp as balance_bp
    app.register_blueprint(balance_bp) 

    from .review import bp as review_bp
    app.register_blueprint(review_bp)

    return app
