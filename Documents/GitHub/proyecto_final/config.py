
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave")
    # Formato: mysql+pymysql://usuario:password@host/base?charset=utf8mb4
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        'mysql+pymysql://root:@127.0.0.1:3306/tienda_zapatillas'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
