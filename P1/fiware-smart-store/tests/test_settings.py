def test_set_language_english(client):
    """Prueba que podamos cambiar el idioma a inglés"""
    # Solicitamos cambiar a inglés
    response = client.get('/set_language/en')
    # Nos tendría que redirigir
    assert response.status_code == 302
    
    # Comprobamos que bajo el idioma nuevo (inglés), vemos las cadenas en inglés en el dashboard
    response = client.get('/')
    assert b'Stores' in response.data or b'Products' in response.data
    assert b'Total Stores' in response.data or b'Total Products' in response.data

def test_set_language_spanish(client):
    """Prueba que el idioma se puede forzar a español"""
    # Solicitamos cambiar a español
    response = client.get('/set_language/es')
    assert response.status_code == 302
    
    # Cargamos la principal para ver texto local
    response = client.get('/')
    assert b'Tiendas' in response.data
    assert b'Productos' in response.data
    assert b'Inventario' in response.data

def test_dark_mode_support_exists(client):
    """Comprueba que la interfaz proporciona el botón y marcadores del modo oscuro/claro"""
    response = client.get('/')
    assert response.status_code == 200
    
    # Comprobar el botón que usa Javascript luego
    assert b'id="theme-toggle"' in response.data
    assert b'class="theme-toggle"' in response.data
    
    # Comprobar el default html data-theme
    assert b'data-theme="light"' in response.data
    
    # Comprobar que script exist en html
    assert b'script.js' in response.data
