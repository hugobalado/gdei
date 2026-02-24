def test_index_route(client):
    """Test para la ruta del Dashboard principal"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'FIWARE Smart Store' in response.data

def test_stores_route(client):
    """Test para la ruta del listado de Tiendas"""
    response = client.get('/stores')
    assert response.status_code == 200

def test_products_route(client):
    """Test para la ruta del listado de Productos"""
    response = client.get('/products')
    assert response.status_code == 200

def test_inventory_route(client):
    """Test para la ruta del Inventario"""
    response = client.get('/inventory')
    assert response.status_code == 200
