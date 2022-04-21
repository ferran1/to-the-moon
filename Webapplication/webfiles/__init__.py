from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from os import path
from flask_login import LoginManager
from flask_talisman import Talisman
from flask_seasurf import SeaSurf

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net'
    ]
}

    Talisman(app, content_security_policy=csp)
    # csrf = SeaSurf(app)
    app.config['SECRET_KEY'] = 'Tothemooon123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .cryptoapi import Crypto, UserProfit

    api = Api(app)
    api.add_resource(Crypto, "/api/crypto")
    api.add_resource(UserProfit, "/api/users/profit")

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User 

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app):
    if not path.exists('webfiles/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
        from .models import Authentication

        # Create api key
        num_items = db.session.query(Authentication).count()
        if not num_items:
            api_key = Authentication("zaCELgL.0imfnc8mVLWwsAawjYr4Rx-Af50DDqtlx")
            db.session.add(api_key)
            db.session.commit()




