# Documento de Requisitos del Producto (PRD)

## 1. Visión del Producto
FIWARE Smart Store es una aplicación web intuitiva diseñada para la gestión integral de una cadena de supermercados corporativa. Su objetivo es facilitar el control de tiendas, productos y stock de inventario a través de una interfaz moderna y eficiente.

## 2. Objetivos
- Simplificar la adición y seguimiento de nuevas sucursales.
- Mantener un catálogo centralizado de productos disponibles.
- Rastrear las unidades en stock de cada producto en cada tienda en tiempo real.
- Proveer una experiencia de usuario rápida, atractiva, y reactiva que fomente su adopción.
- Ofrecer soporte multi-idioma nativo para adaptarse a diferentes equipos corporativos internacionales.

## 3. Funcionalidades Clave
1. **Gestión de Tiendas:** Visualización de todas las sucursales con soporte para imágenes y vistas de detalle avanzado mostrando el stock local específico de esa tienda.
2. **Gestión de Baldas:** Organización espacial del interior de cada tienda, facilitando su estructuración (crear, editar ubicación y borrar) desde el detalle de cada sucursal.
3. **Gestión de Empleados:** Control del personal asignado a cada tienda, detallando roles, salarios e información de contacto o imagen.
4. **Catálogo de Productos:** Consulta exhaustiva de mercancías con soporte para la procedencia (`originCountry`), imágenes, e información cruzada de disponibilidad en qué tiendas se halla el artículo.
5. **Control de Inventario Avanzado:** Capacidad de operaciones CRUD completas sobre el inventario para reubicar stock y alterar cantidades individualmente, tanto desde la vista de Tienda como desde Producto.
6. **Dashboard Estratégico:** Panel de control principal con KPIs clave (Total de Tiendas, Total de Empleados, Total de Productos, Stock Físico Total) extraídos de la BD en tiempo real.
7. **Formularios Dinámicos Aislados:** Vistas únicas de creación para facilitar el alta de tiendas, empleados, productos y sus interrelaciones sin sobrecargar las interfaces iterativas.
7. **Modo Oscuro/Claro:** Adaptación automática a las preferencias de visualización del usuario usando almacenamiento en el navegador (Local Storage).
8. **Soporte Multi-Idioma (ES/EN):** Cambio en tiempo real de toda la interfaz estática garantizando que el usuario pueda usar el sistema en su idioma de preferencia, conservando las preferencias en sesión de manera ininterrumpida.
9. **Mapas Interactivos:** Geolocalización visual y en tiempo real de las tiendas a través de Leaflet.js y OpenStreetMap.
10. **Diseño Visual Corporativo:** Estética inmersiva (inspirada en los colores del RC Deportivo), feedback interactivo (`hover`), interfaces limpias (supresión visual de UUIDs) y control robusto de consistencia y carga de imágenes (`fallback`).

## 4. Requisitos No Funcionales
- **Usabilidad:** Interfaz con diseño "clean" y moderno, empleando fuentes modernas e iconografía representativa para todos los conceptos del dominio.
- **Rendimiento:** Las operaciones de creación y consulta deben ser instantáneas mediante la recarga directa de interfaz.
- **Persistencia:** Todos los datos deben ser almacenados estructuradamente en base de datos.
- **Responsive:** Navegación diseñada para funcionar óptimamente a diferentes resoluciones (Desktop/Web/Tablet).
- **Internacionalización Constante:** Sólo el contenido estático de las interfaces debe ser traducido localmente; los datos que conforman el catálogo o sucursales extraídos dinámicamente de la base de datos se rigen por un principio de "Lenguaje Agnóstico" (Intra-traducibles).
- **Calidad y Testing (QA):** La aplicación debe contar con una suite de tests automatizados que asegure el correcto funcionamiento de las rutas, cambios de configuración de la interfaz y operaciones de base de datos (CRUD), garantizando que futuras actualizaciones no rompan las funcionalidades críticas.

## 5. Público Objetivo
- Operadores y gerentes de sede central del supermercado.
- Jefes de tienda que necesiten verificar el catálogo corporativo.
- Personal de logística enfocado en reabastecimiento.
