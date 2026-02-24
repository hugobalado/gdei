# Modelo de Datos

## 1. Visión General de Entidades
La base de datos relacional de la aplicación `fiware-smart-store` se define sobre SQLite usando `SQLAlchemy`. Está compuesta por tres entidades principales con una relación de Muchos-a-Muchos a través de una tabla pivot enriquecida (Inventario).

## 2. Diagrama de Relación (Lógico)

- Una `Tienda` (Store) puede albergar múltiples productos en su inventario.
- Un `Producto` (Product) puede estar presente en diferentes tiendas simultáneamente.
- El vínculo que une a Tiendas y Productos es la tabla `Inventario`, que aporta información adicional vital: la cantidad de stock actual.

## 3. Esquemas de Base de Datos

### Tabla: `store`
Representa una sucursal física de la cadena de supermercados.

| Columna | Tipo de Dato | Llave | Modificadores | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String(255) | PK | URN UUID | Identificador único de la tienda (formato URN `urn:ngsi-ld:Store:...`). |
| `name` | String(100) | | Not Null | Nombre descriptivo de la sucursal. |
| `address`| String(200) | | Not Null | Dirección postal o ubicación de la misma. |
| `image` | String(500) | | Nullable | URL externa (ej. Unsplash) a una imagen representativa. |

### Tabla: `product`
Representa un artículo genérico del catálogo disponible para venderse.

| Columna | Tipo de Dato | Llave | Modificadores | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String(255) | PK | URN UUID | Identificador único del producto (formato URN `urn:ngsi-ld:Product:...`). |
| `name` | String(100) | | Not Null | Nombre del producto comercializado. |
| `size` | Text | | Nullable | Tamaño o breve caracterización (ej. "1 Litro", "S", "M"). |
| `price` | Float | | Not Null | Precio general o recomendando de venta (€). |
| `originCountry` | String(100) | | Nullable | País de procedencia del producto (ej. "España"). |
| `image` | String(500) | | Nullable | URL externa (ej. Unsplash) a una foto del producto. |

### Tabla: `inventoryitem` (Modelo `InventoryItem`)
Tabla asociativa transaccional. Registra qué cantidad de cada producto concreto está albergada en cada tienda específica.

| Columna | Tipo de Dato | Llave | Modificadores | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String(255) | PK | URN UUID | Identificador transaccional único (formato URN `urn:ngsi-ld:InventoryItem:...`). |
| `refStore` | String(255)| FK | Not Null | Relación (Foreign Key) a `store.id`. |
| `refProduct` | String(255)| FK | Not Null | Relación (Foreign Key) a `product.id`. |
| `stockCount` | Integer | | Not Null, Default(0)| Cantidad de unidades físicas de stock disponibles. |

## 4. Políticas en Cascada (Cascade)
- Ambos el modelo de `Store` y `Product` están configurados con relaciones tipo `lazy=True, cascade="all, delete-orphan"`.
- Estó significa metodológicamente que si un producto se retira permanentemente del catalogo (`deleted`), todos sus registros de inventario (asociaciones con tiendas) en la tabla `inventoryitem` serán automáticamente purgados huérfanos. Lo mismo ocurre si se cierra (elimina) una tienda desde el sistema.

## 5. Estrategia de Internacionalización (i18n)
- **Agnosticismo del Dato:** Los modelos están diseñados para almacenar exclusivamente información de forma neutral al lenguaje regional activo de la sesión del usuario.
- Cualquier dato extraído (e.g., `store.name` o `product.description`) se transfiere crudo ("raw") al frontend sin aplicar directivas de traducción `_()`. Esto asegura la paridad de los datos a nivel logístico entre diferentes regiones y previene desajustes estructurales de inventario por traducciones equívocas.

## 6. Base de Datos en el Entorno de Testing (`Pytest`)
- Para la validación automatizada de los modelos y las operaciones *CRUD*, la suite de testing genera dinámicamente una **base de datos temporal vacía aislada** mediante el módulo `tempfile` en cada iteración de la fixture de `pytest`.
- Esto garantiza que todas las transacciones sobre Tiendas, Productos o Inventario realizadas durante las pruebas:
  - No colisionen con el volumen principal `instance/smart_store.db`.
  - Sean revertidas y purgadas de forma segura una vez el *kernel* de tests finalice (drop total del esquema temporal en disco).
