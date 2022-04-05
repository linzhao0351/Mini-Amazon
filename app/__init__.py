from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .search import bp as search_bp
    app.register_blueprint(search_bp)

    from .customer import bp as customer_bp
    app.register_blueprint(customer_bp)

    from .seller import bp as seller_bp
    app.register_blueprint(seller_bp)    

    from .product import bp as product_bp
    app.register_blueprint(product_bp)   

    return app
