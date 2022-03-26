from flask import Flask
from flask_security import current_user, login_required, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib  import sqla
import os

from wtforms.fields import PasswordField

import logging
import datetime

db = SQLAlchemy()
from .models import User, Role, UserAdmin, RoleAdmin
#Creamos un objeto de la clase SQLAlchemyUserDatastore
userDataStore = SQLAlchemyUserDatastore(db, User, Role)

LOG_FILENAME = './logs/logs.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

#Método de inicio de la aplicación
def create_app():
    #Creamos una instancia de la clase Flask
    app = Flask(__name__)
    logging.debug('Arranque de la aplicacion, Fecha: {}'.format(datetime.datetime.today()))
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG']=True
    #Generamos la clave aleatoria de sesión Flask para crear una cookie con la inf. de la sesión
    app.config['SECRET_KEY'] = 'super-secret'
    #Definimos la ruta a la BD: mysql://user:password@localhost/bd'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/bytech'
    # We're using PBKDF2 with salt.
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    #Semilla para el método de encriptado que utiliza flask-security
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    #Inicializamos y creamos la BD
    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()
        
        # Create the Roles "admin" and "end-user" -- unless they already exist
        userDataStore.find_or_create_role(name='admin', description='Administrator')
        userDataStore.find_or_create_role(name='end-user', description='End user')

        # Create two Users for testing purposes -- unless they already exists.
        # In each case, use Flask-Security utility function to encrypt the password.
        encrypted_password = utils.encrypt_password('password')
        if not userDataStore.get_user('someone@example.com'):
            userDataStore.create_user(name='end-user', email='someone@example.com', password=encrypted_password)
        if not userDataStore.get_user('admin@example.com'):
            userDataStore.create_user(name='admin', email='admin@example.com', password=encrypted_password)

        # Commit any database changes; the User and Roles must exist before we can add a Role to the User
        db.session.commit()

        # Give one User has the "end-user" role, while the other has the "admin" role. (This will have no effect if the
        # Users already have these Roles.) Again, commit any database changes.
        userDataStore.add_role_to_user('someone@example.com', 'end-user')
        userDataStore.add_role_to_user('admin@example.com', 'admin')
        db.session.commit()

    #Conectando los modelos a fask-security usando SQLAlchemyUserDatastore
    security = Security(app, userDataStore)
    
    # Initialize Flask-Admin
    admin = Admin(app)

    # Add Flask-Admin views for Users and Roles
    admin.add_view(UserAdmin(User, db.session))
    admin.add_view(RoleAdmin(Role, db.session))
    #Registramos el blueprint para las rutas auth de la aplicación
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    #Registramos el blueprint para las partes no auth de la aplicación
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    #Registramos el blueprint para los productos de la aplicación
    from .productos import productos as main_blueprint
    app.register_blueprint(main_blueprint)


    return app