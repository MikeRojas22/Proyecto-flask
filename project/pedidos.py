from flask import Blueprint, render_template, redirect, url_for, request, flash
#Importamos los módulos de seguridad para las funciones hash
from werkzeug.security import generate_password_hash, check_password_hash
#Importamos el método login_required de flask_security
from flask_security import login_required, current_user, roles_required
from flask import current_app
#Importamos los métodos login_user, logout_user flask_security.utils
#########################################################################################
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
##########################################################################################
#Importamos el modelo del usuario
#from . models import Pedidos
#Importamos el objeto de la BD y pedidosDataStore desde __init__
from . import db
import os
from . models import Productos

#Creamos el BluePrint y establecemos que todas estas rutas deben estar dentro de /pedidos para sobre escribir las vistas por omisión de flask-security.
#Por lo que ahora las rutas deberán ser /pedidos/login y security/register
pedidos = Blueprint('pedidos', __name__, url_prefix='/pedidos')

@pedidos.route('/pedido/<id>', methods=['POST','GET'])
@login_required
def pedido(id):
    producto = Productos.query.get(id)
    if request.method == 'POST':
        nombre = request.form.get('cantidad')
        return redirect(url_for('productos.listaProductos'))

    return render_template('/pedidos/pedido.html', producto=producto)