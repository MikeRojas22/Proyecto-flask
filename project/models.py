from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

# Define models
roles_users = db.Table('roles_users',
        db.Column('userId', db.Integer(), db.ForeignKey('user.id')),
        db.Column('roleId', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    """Role model"""
    
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    """User account model"""
    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    
class Productos(db.Model, UserMixin):
    """Productos model"""
    __tablename__ = 'productos'
    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.String(255), unique=False)
    image_name = db.Column(db.String(255), unique=False)
    
