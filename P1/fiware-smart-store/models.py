import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def generate_urn(entity_type):
    return f"urn:ngsi-ld:{entity_type}:{uuid.uuid4()}"

class Store(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=lambda: generate_urn('Store'))
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    inventories = db.relationship('InventoryItem', backref='store', lazy=True, cascade="all, delete-orphan")
    employees = db.relationship('Employee', backref='store', lazy=True, cascade="all, delete-orphan")
    shelves = db.relationship('Shelf', backref='store', lazy=True, cascade="all, delete-orphan")

class Product(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=lambda: generate_urn('Product'))
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500), nullable=True)
    originCountry = db.Column(db.String(100), nullable=True)
    inventories = db.relationship('InventoryItem', backref='product', lazy=True, cascade="all, delete-orphan")

class InventoryItem(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=lambda: generate_urn('InventoryItem'))
    refStore = db.Column(db.String(255), db.ForeignKey('store.id'), nullable=False)
    refProduct = db.Column(db.String(255), db.ForeignKey('product.id'), nullable=False)
    stockCount = db.Column(db.Integer, nullable=False, default=0)

class Employee(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=lambda: generate_urn('Employee'))
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    salary = db.Column(db.Float, nullable=False)
    role = db.Column(db.String(100), nullable=False)
    refStore = db.Column(db.String(255), db.ForeignKey('store.id'), nullable=False)

class Shelf(db.Model):
    id = db.Column(db.String(255), primary_key=True, default=lambda: generate_urn('Shelf'))
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    refStore = db.Column(db.String(255), db.ForeignKey('store.id'), nullable=False)
