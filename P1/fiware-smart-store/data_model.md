# Modelo de Datos

## 1. Visión General de Entidades
La base de datos relacional de la aplicación `fiware-smart-store` se define sobre SQLite usando `SQLAlchemy`. Está compuesta por cuatro entidades principales: Tienda, Producto, Inventario (pivot), y Empleado.

## 2. Diagrama de Relación (Lógico)

- Una `Tienda` (Store) puede albergar múltiples productos en su inventario.
- Una `Tienda` (Store) puede tener múltiples elementos físicos o secciones representadas por Baldas (`Shelf`).
- Una `Tienda` (Store) puede tener múltiples empleados asignados a ella.
- Un `Producto` (Product) puede estar presente en diferentes tiendas simultáneamente.
- El vínculo que une a Tiendas y Productos es la tabla `Inventario`, que aporta información adicional vital: la cantidad de stock actual.
- Un `Empleado` (Employee) está directamente asociado (1:N) a una única tienda y se borra en cascada si ésta cierra.
- Una `Balda` (Shelf) pertenece de forma única a una Tienda (1:N) y desaparece en cascada junto con su tienda madre.

## 3. Esquemas de Base de Datos

### Tabla: `store`
Representa una sucursal física de la cadena de supermercados.

| Columna | Tipo de Dato | Llave | Modificadores | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String(255) | PK | URN UUID | Identificador único de la tienda (formato URN `urn:ngsi-ld:Store:...`). |
| `name` | String(100) | | Not Null | Nombre descriptivo de la sucursal. |
| `address`| String(200) | | Not Null | Dirección postal o ubicación de la misma. |
| `image` | String(500) | | Nullable | URL externa (ej. Unsplash) a una imagen representativa. |

### Tabla: `shelf`
Representa una estantería o balda organizativa dentro de las dependencias de una tienda.

| Columna | Tipo de Dato | Llave | Modificadores | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String(255) | PK | URN UUID | Identificador único de la estantería (formato URN `urn:ngsi-ld:Shelf:...`). |
| `name` | String(100) | | Not Null | Nombre descriptivo de la balda. |
| `location` | String(200) | | Nullable | Ubicación semántica o física. |
| `refStore` | String(255) | FK | Not Null | Relación (Foreign Key) a `store.id`. |

### Tabla: `employee`
Representa un trabajador de una sucursal específica.

| Columna | Tipo de Dato | Llave | Modificadores | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `id` | String(255) | PK | URN UUID | Identificador único del empleado (formato URN `urn:ngsi-ld:Employee:...`). |
| `name` | String(100) | | Not Null | Nombre completo del empleado. |
| `image` | String(500) | | Nullable | URL externa (ej. Unsplash) de la foto del trabajador. |
| `salary` | Float | | Not Null | Salario del empleado. |
| `role` | String(100) | | Not Null | Puesto laboral (ej. "Cajero", "Gerente"). |
| `refStore` | String(255) | FK | Not Null | Relación (Foreign Key) a `store.id`. |

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
- Tanto el modelo `Store` como el `Product` están configurados con relaciones `cascade="all, delete-orphan"` para proteger dependencias directas.
- Si una Tienda (Store) se borra, todos sus registros de `Inventario`, `Empleados` y `Baldas` (`Shelf`) asociados son automáticamente purgados como huérfanos de la base de datos.
- Si un `Producto` se retira permanentemente del catalogo (`deleted`), todos sus registros dependientes en la tabla asociativa `inventoryitem` (su distribución física en tiendas) son purgados del mismo modo.

## 5. Estrategia de Internacionalización (i18n)
- **Agnosticismo del Dato:** Los modelos están diseñados para almacenar exclusivamente información de forma neutral al lenguaje regional activo de la sesión del usuario.
- Cualquier dato extraído (e.g., `store.name` o `product.description`) se transfiere crudo ("raw") al frontend sin aplicar directivas de traducción `_()`. Esto asegura la paridad de los datos a nivel logístico entre diferentes regiones y previene desajustes estructurales de inventario por traducciones equívocas.

## 6. Base de Datos en el Entorno de Testing (`Pytest`)
- Para la validación automatizada de los modelos y las operaciones *CRUD*, la suite de testing genera dinámicamente una **base de datos temporal vacía aislada** mediante el módulo `tempfile` en cada iteración de la fixture de `pytest`.
- Esto garantiza que todas las transacciones sobre Tiendas, Productos o Inventario realizadas durante las pruebas:
  - No colisionen con el volumen principal `instance/smart_store.db`.
  - Sean revertidas y purgadas de forma segura una vez el *kernel* de tests finalice (drop total del esquema temporal en disco).

## 7. Políticas de Integridad Visual (Imágenes)
- Las columnas `image` de **Tienda**, **Producto** y **Empleado** (que referencian URLs externas como Unsplash) están sometidas a control de calidad y coherencia visual semántica.
- Los empleados requieren fotografías de personas reales portando ropa de trabajo afín a su rol (ej. azul corporativo para reponedores/cajeros), prohibiendo el uso de objetos o fotografías sin personas.
- Se implementan mecanismos `onerror` a nivel de presentación en Jinja2; si un asset remoto desaparece o provoca un HTTP 404, la plataforma muestra de forma automática un *placeholder* (fallback) manteniendo la cuadrícula de la aplicación intacta.
