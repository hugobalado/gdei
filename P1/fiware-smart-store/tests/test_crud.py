from models import Store, Product, Inventory

def test_create_store(client, session):
    """Test para añadir una tienda mediante POST"""
    # Enviar solicitud POST
    response = client.post('/stores', data={
        'name': 'Test Store 1',
        'location': 'Test Location 123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Comprobar que en la UI devuelta aparece el nombre de la nueva tienda
    assert b'Test Store 1' in response.data
    
    # Comprobar en base de datos
    store = Store.query.filter_by(name='Test Store 1').first()
    assert store is not None
    assert store.location == 'Test Location 123'

def test_create_product(client, session):
    """Test para añadir un producto mediante POST"""
    # Enviar solicitud POST
    response = client.post('/products', data={
        'name': 'Test Product A',
        'description': 'Description A',
        'price': '9.99'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Test Product A' in response.data
    
    # Comprobar en base de datos
    product = Product.query.filter_by(name='Test Product A').first()
    assert product is not None
    assert product.price == 9.99

def test_create_inventory(client, session):
    """Test para la relación de inventario, sumando a uno existente o creando nuevo"""
    # 1. Crear dependencias en BD
    store = Store(name='Inventory Store', location='Loc')
    product = Product(name='Inventory Product', description='Desc', price=1.5)
    session.add(store)
    session.add(product)
    session.commit()

    # 2. Enviar POST al inventario
    response = client.post('/inventory', data={
        'store_id': store.id,
        'product_id': product.id,
        'quantity': '25'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # 3. Comprobar que la cantidad es 25 en BBDD
    inv = Inventory.query.filter_by(store_id=store.id, product_id=product.id).first()
    assert inv is not None
    assert inv.quantity == 25

    # 4. Enviar otro POST con 10 más
    client.post('/inventory', data={
        'store_id': store.id,
        'product_id': product.id,
        'quantity': '10'
    })

    # 5. Comprobar que ahora es 35
    inv_updated = Inventory.query.filter_by(store_id=store.id, product_id=product.id).first()
    assert inv_updated.quantity == 35
