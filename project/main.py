#Importamos la clase Blueprint del módulo flask
from flask import Blueprint, render_template
#Importamos login_required, current_user de flask_security
from flask_security import login_required, current_user, RoleMixin, Security, \
    SQLAlchemyUserDatastore, UserMixin, utils
#Importamos el decorador login_required de flask_security
from flask_security.decorators import roles_required
#Importamos el objeto de la BD desde __init__.py
from . import db
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib  import sqla

from wtforms.fields import PasswordField

main = Blueprint('main',__name__)

#Definimos la ruta a la página principal
@main.route('/')
@login_required
def index():
    return render_template('index.html')

#Definimos la ruta a la página de perfil
@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

#Definimos la ruta a la página de perfil
@main.route('/contacto')
def contacto():
    return render_template('contacto.html')

