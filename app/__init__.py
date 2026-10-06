from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db            = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.auth            import auth
    from app.routes.dashboard       import dashboard
    from app.routes.invoices        import invoices
    from app.routes.vendors         import vendors
    from app.routes.purchase_orders import purchase_orders

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(invoices)
    app.register_blueprint(vendors)
    app.register_blueprint(purchase_orders)

    with app.app_context():
        from app import models
        db.create_all()
        create_default_user()

    return app

def create_default_user():
    from app.models import User
    from werkzeug.security import generate_password_hash
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username = 'admin',
            password = generate_password_hash('admin123'),
            role     = 'admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created!")
