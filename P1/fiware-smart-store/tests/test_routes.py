from models import db, Store, Product, Shelf, InventoryItem

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

def test_shelf_crud(client):
    """Test para operaciones CRUD de Shelf"""
    with client.application.app_context():
        store = Store(name="Test Store", address="Test Address")
        db.session.add(store)
        db.session.commit()
        store_id = store.id
    
    # Create
    response = client.post(f'/store/{store_id}/shelf/new', data={
        'name': 'Test Shelf',
        'location': 'Aisle 1'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with client.application.app_context():
        shelf = Shelf.query.filter_by(name='Test Shelf').first()
        assert shelf is not None
        shelf_id = shelf.id
        
    # Edit
    response = client.post(f'/shelf/{shelf_id}/edit', data={
        'name': 'Updated Shelf',
        'location': 'Aisle 2'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with client.application.app_context():
        shelf = Shelf.query.get(shelf_id)
        assert shelf.name == 'Updated Shelf'
        
    # Delete
    response = client.post(f'/shelf/{shelf_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    
    with client.application.app_context():
        shelf = Shelf.query.get(shelf_id)
        assert shelf is None

def test_inventory_crud(client):
    """Test para operaciones CRUD de Inventory en vistas detalle"""
    with client.application.app_context():
        store = Store(name="Test Store", address="Test Address")
        product = Product(name="Test Product", price=1.0)
        db.session.add(store)
        db.session.add(product)
        db.session.commit()
        store_id = store.id
        product_id = product.id
        
    # Add product to store
    response = client.post(f'/store/{store_id}/inventory/new', data={
        'refProduct': product_id,
        'stockCount': '15'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with client.application.app_context():
        inv = InventoryItem.query.filter_by(refStore=store_id, refProduct=product_id).first()
        assert inv is not None
        assert inv.stockCount >= 15
        inv_id = inv.id
        
    # Edit inventory
    response = client.post(f'/inventory/{inv_id}/edit', data={
        'stockCount': '20'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with client.application.app_context():
        inv = InventoryItem.query.get(inv_id)
        assert inv.stockCount == 20
        
    # Delete inventory
    response = client.post(f'/inventory/{inv_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    
    with client.application.app_context():
        inv = InventoryItem.query.get(inv_id)
        assert inv is None
