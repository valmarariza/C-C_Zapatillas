from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from .models import db  # asegúrate de que models.py tenga db = SQLAlchemy()

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Configuración de seguridad
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://mariana:marianac@isladigital.xyz:3311/f58_mariana"


    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuración de correo
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "tunombre@gmail.com"
    app.config["MAIL_PASSWORD"] = "miclave123"

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Rutas extra (profile)
    from .routes.profile import profile_bp
    app.register_blueprint(profile_bp)

    # Importar modelos
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints principales
    from .routes.auth import auth_bp
    from .routes.public import public_bp
    from .routes.cart import cart_bp
    from .routes.orders import orders_bp
    from .routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Crear tablas y datos iniciales (solo si la BD está vacía)
    with app.app_context():
        db.create_all()
        seed_data()

    return app

# -------------------
# Función seed_data
# -------------------
def seed_data():
    from .models import User, Category, Product, db

    # Crear admin si no existe
    if not User.query.filter_by(email="admin@tienda.com").first():
        admin = User(
            name="Admin",
            email="admin@tienda.com",
            password_hash=bcrypt.generate_password_hash("admin123").decode("utf-8"),
            role="admin"
        )
        db.session.add(admin)

    # Crear categorías si no existen
    if Category.query.count() == 0:
        cats = [
            "Zapatillas para césped artificial",
            "Zapatillas para césped natural",
            "Zapatillas de fútbol multitacos",
            "Zapatillas de futbol de toque",
            "Zapatillas de futbol de potencia",
            "Zapatillas de futbol clásicas"
        ]
        categories = [Category(name=c) for c in cats]
        db.session.add_all(categories)
        db.session.flush()
    else:
        categories = Category.query.order_by(Category.id).all()

    # Normalizador de nombres
    def normalize_name(name):
        return name.strip().lower()

    existing_names = {normalize_name(p.name) for p in Product.query.all()}

    sample_products = [
        # Aquí deberías poner productos de ejemplo
        # Product(name="Ejemplo 1", price=100, category_id=categories[0].id)
    ]

    # Solo agrega productos que no existan por nombre normalizado
    to_add = [p for p in sample_products if normalize_name(p.name) not in existing_names]
    if to_add:
        db.session.add_all(to_add)
        db.session.commit()
