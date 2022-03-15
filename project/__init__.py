from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
from .models import User, Role
#Creamos un objeto de la clase SQLAlchemyUserDatastore
userDataStore = SQLAlchemyUserDatastore(db, User, Role)


#Método de inicio de la aplicación
def create_app():
    #Creamos una instancia de la clase Flask
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #Generamos la clave aleatoria de sesión Flask para crear una cookie con la inf. de la sesión
    app.config['SECRET_KEY'] = os.urandom(24)
    #Definimos la ruta a la BD: mysql://user:password@localhost/bd'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/byTech'
    # We're using PBKDF2 with salt.
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    #Semilla para el método de encriptado que utiliza flask-security
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'

    #Inicializamos y creamos la BD
    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()

    #Conectando los modelos a fask-security usando SQLAlchemyUserDatastore
    security = Security(app, userDataStore)

    #login_manager = LoginManager()
    #login_manager.login_view = 'auth.login'
    #login_manager.init_app(app)

    #Importamos la clase User de models
    #from .models import User
    #@login_manager.user_loader
    #def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        #return User.query.get(int(user_id))


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

    #instancia flaks
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_ URI'] = 'mysql://root:root@localhost/byTech'
    
    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    #Importamos la clase user models
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        #Since the user_id is just the primary key of our user table. user it in the query for the user
        return User.query.get(int(user_id))
    
    #Rutas auth
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    #Rutas main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app