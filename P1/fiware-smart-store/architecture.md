# Arquitectura del Sistema

## 1. Patrón Arquitectónico
La aplicación sigue un patrón unificado **MVC/MVT** (Model, View, Template) propuesto nativamente por el Framework web **Flask** de Python. 
- **Models:** Las estructuras de datos están reflejadas en clases Python a través de SQLAlchemy (ORM) usando URNs semánticas de NGSI-v2.
- **Views (Controladores):** Las funciones de manejo de rutas (`@app.route`) separan la lógica de lectura (listados y vistas de Detalle) de la de escritura (Formularios POST separados), gestionando el ciclo de peticiones asiladamente.
- **Templates (Vistas):** Documentos Jinja2 (`.html`) renderizados dinámicamente en el servidor en función de los datos que inyecta la lógica de la aplicación.

## 2. Stack Tecnológico
### Backend
- **Lenguaje:** Python 3.
- **Framework Web:** Flask 3.0.
- **ORM / Base de Datos:** Flask-SQLAlchemy para crear una abstracción sobre una base de datos embebida `SQLite`.
- **Internacionalización:** Flask-Babel (i18n) para traducción de elementos estáticos e interfaces al vuelo mediante archivos compilados `.mo`.
- **Testing y QA:** `pytest` y `pytest-flask` para el modelado de la suite de pruebas unitarias y de integración del ecosistema, probando interacciones tanto estáticas como transaccionales.

### Frontend
- **HTML:** Etiquetas semánticas estructuradas con directivas Jinja2. Manejo de fallos en carga de archivos multimedia (`onerror` image fallbacks).
- **Estilos (CSS):** Vanilla CSS con variables (`root` variables) inyectado para gestionar estilos y paletas de colores (Modo claro/oscuro y estética blanquiazul) de modo dinámico sin librerías pesadas, aplicando flexbox/grids y transiciones fluidas.
- **Interactividad (JS):** Vanilla JavaScript enfocado a manipular el DOM para el cambio persistente de tema, usando `localStorage`.
- **Mapas (JS):** Leaflet.js combinado con la API de Nominatim (OpenStreetMap) para renderizar mapas interactivos de ubicación por tienda.
- **Iconografía:** FontAwesome (CDN) integrado directamente para renderizar SVG Icons asociados al domino ("Tienda", "Producto", "Cajas", "Personal").

## 3. Estructura de Proyecto
```
P1/fiware-smart-store/
├── app.py             # Controlador principal y enrutador web. Rutinas inicializadoras y configuración de Babel (i18n).
├── models.py          # Definición de estructuras y relaciones SQLAlchemy.
├── requirements.txt   # Dependencias de pip.
├── .gitignore         # Configuración de exclusión para Git (.venv, pycache, etc).
├── babel.cfg          # Archivo de configuración para la extracción de textos traducibles (Flask-Babel).
├── translations/      # Directorio que almacena los catálogos de mensajes regionales (.po, .mo).
├── static/
│   ├── style.css      # Sistema de utilidades CSS, UI Cards, Formularios, Variables del ecosistema.
│   └── script.js      # Script de conmutación de temáticas claras/oscuras.
├── templates/
│   ├── base.html          # Layout principal contenedor. (Barra de navegación, footer, headers).
│   ├── index.html         # Dashboard principal con métricas (KPIs).
│   ├── stores.html        # Listado de lectura de Tiendas.
│   ├── products.html      # Listado de lectura del Catálogo de Productos.
│   ├── employees.html     # Listado de lectura del conjunto de Empleados.
│   ├── store_detail.html  # Vista en profundidad de una sucursal única y su inventario.
│   ├── product_detail.html# Vista en profundidad de un artículo y su disponibilidad.
│   ├── employee_detail.html # Vista individual del trabajador (salario, rol).
│   ├── store_form.html    # Formulario aislado de creación/edición de una tienda.
│   ├── product_form.html  # Formulario aislado de creación/edición de un producto.
│   ├── employee_form.html # Formulario de registro de un empleado y asignación a tienda.
│   ├── shelf_form.html    # Formulario dinámico de gestión de unidades de almacenaje o baldas.
│   ├── inventory_form.html# Componente de interfaz integrado para agregar o modificar stock entre tienda y producto.
│   └── inventory.html     # Vista general macro listando de forma masiva los registros globales del Inventario.
├── tests/             # Directorio de la suite de tests automatizados con pytest.
│   ├── conftest.py    # Fixtures (cliente de pruebas, base de datos de test temporal).
│   ├── test_settings.py # Tests de modos e idiomas (oscuro/claro, ES/EN).
│   ├── test_routes.py # Validaciones de disponibilidad de las rutas web (HTTP 200).
│   └── test_crud.py   # Pruebas integradas de inyección de datos (POST) y base de datos.
└── instance/
    └── smart_store.db # Fichero SQLite autogenerado con los datos y seed data.
```
