import os
import tempfile
import pytest

# Usaremos la aplicación real y su base de datos
from app import app as flask_app
from models import db, Store, Product, InventoryItem

@pytest.fixture
def app():
    """Genera una instancia de la aplicación Flask configurada de manera aislada para testing."""
    # Creamos un archivo temporal para la base de datos local
    db_fd, db_path = tempfile.mkstemp()
    
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'BABEL_DEFAULT_LOCALE': 'es', # Valor por defecto explicitamente
    })

    # El contexto de la app nos permite interactuar con la base de datos
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Genera un cliente de pruebas para enviar peticiones a la app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Para probar comandos CLI de Flask si fuera necesario"""
    return app.test_cli_runner()

@pytest.fixture
def session(app):
    """Fixture auxiliar para transacciones de db concretas dentro de tests."""
    with app.app_context():
        yield db.session

