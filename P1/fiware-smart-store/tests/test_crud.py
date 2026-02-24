from models import Store, Product, InventoryItem

def test_create_store(client, session):
    """Test para añadir una tienda mediante POST"""
    # Enviar solicitud POST
    response = client.post('/store/new', data={
        'name': 'Test Store 1',
        'address': 'Test Location 123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Comprobar que en la UI devuelta aparece el nombre de la nueva tienda
    assert b'Test Store 1' in response.data
    
    # Comprobar en base de datos
    store = Store.query.filter_by(name='Test Store 1').first()
    assert store is not None
    assert store.address == 'Test Location 123'

def test_create_product(client, session):
    """Test para añadir un producto mediante POST"""
    # Enviar solicitud POST
    response = client.post('/product/new', data={
        'name': 'Test Product A',
        'size': 'Description A',
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
    store = Store(name='Inventory Store', address='Loc')
    product = Product(name='Inventory Product', size='Desc', price=1.5)
    session.add(store)
    session.add(product)
    session.commit()

    # 2. Enviar POST al inventario
    response = client.post('/inventory', data={
        'refStore': store.id,
        'refProduct': product.id,
        'stockCount': '25'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # 3. Comprobar que la cantidad es 25 en BBDD
    inv = InventoryItem.query.filter_by(refStore=store.id, refProduct=product.id).first()
    assert inv is not None
    assert inv.stockCount == 25

    # 4. Enviar otro POST con 10 más
    client.post('/inventory', data={
        'refStore': store.id,
        'refProduct': product.id,
        'stockCount': '10'
    })

    # 5. Comprobar que ahora es 35
    inv_updated = InventoryItem.query.filter_by(refStore=store.id, refProduct=product.id).first()
    assert inv_updated.stockCount == 35
