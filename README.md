# Tarea 2: Sistema de Adopción de Mascotas con Flask

Una aplicación web completa para gestión de adopción de perros y gatos, desarrollada con Flask, SQLAlchemy y MySQL. Incluye validaciones del lado del servidor y cliente.

## Características

- **Formulario de adopción** con validaciones JavaScript y del servidor
- **Listado paginado** de avisos de adopción
- **Vista detallada** con galería de fotos y modal
- **API REST** para obtener comunas por región
- **Portal de estadísticas** con gráficos estaticos, usado como maqueta, sin ninguna funcionalidad hasta el momento.
- **Gestión de archivos** con validación de imágenes
- **Base de datos MySQL** con relaciones complejas

## Tecnologías

- **Backend**: Flask 3.0.0
- **Base de datos**: MySQL con SQLAlchemy 2.0.23
- **Frontend**: HTML5, CSS3, JavaScript
- **Validaciones**: JavaScript (cliente) + Python (servidor)
- **Templates**: Jinja2

## Requisitos

- Python 3.8+
- MySQL 5.7+
- pip (gestor de paquetes Python)

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Desarrollo_Web_Martin_Bahamonde
```

### 2. Crear entorno virtual
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
# Conectar a MySQL
mysql -u root -p

# Ejecutar scripts SQL
SOURCE database/tarea2.sql;
SOURCE database/region-comuna.sql;
```

### 5. Configurar variables de entorno
```bash
# Crear archivo .env (opcional, yo no lo hice)
DB_HOST=localhost
DB_PORT=3306
DB_USER=cc5002
DB_PASSWORD=programacionweb
DB_NAME=tarea2
SECRET_KEY=tu-clave-secreta-aqui
```

## Ejecución

### Desarrollo
```bash
# Activar entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# Ejecutar aplicación
python app.py
```

### Acceder a la aplicación
```
http://localhost:5000
```


## Funcionalidades

### 1. Agregar Aviso de Adopción
- Formulario completo con validaciones
- Subida de múltiples imágenes
- Validaciones JavaScript y del servidor
- Modal de confirmación

### 2. Listado de Avisos
- Paginación
- Información resumida de cada aviso
- Enlaces a vista detallada

### 3. Detalle de Aviso
- Información completa del aviso
- Galería de fotos con modal
- Datos de contacto
- Información de la mascota


## Seguridad

- **Validaciones del servidor**: Prevención de inyección SQL y XSS
- **SQLAlchemy ORM**: Escapado automático de consultas
- **Validación de archivos**: Extensiones y tamaños permitidos

## Validaciones

### Cliente (JavaScript)
- Formato de email
- Formato de celular (+NNN.NNNNNNNN)
- Fechas válidas
- Archivos de imagen
- Campos obligatorios

### Servidor (Python)
- Validación robusta de todos los campos
- Prevención de inyección SQL
- Validación de archivos
- Sanitización de datos

## Base de datos

### Tablas principales
- `region`: Regiones de Chile
- `comuna`: Comunas por región
- `aviso_adopcion`: Avisos de adopción
- `contactar_por`: Métodos de contacto
- `foto`: Imágenes de avisos

### Relaciones
- Una región tiene muchas comunas
- Una comuna tiene muchos avisos
- Un aviso tiene muchos contactos
- Un aviso tiene muchas fotos

## Notas 

- **Separación de responsabilidades**: Lógica de negocio separada de la presentación
- **Validaciones duales**: Cliente para UX, servidor para seguridad
- **Manejo de errores**: Try-catch en operaciones de BD
- **Configuración**: Se usan valores por defecto considerando que estamos en desarrollo y es una tarea, para producción se deberían usar variables de entorno globalizadas.

##  Autor

**Martin Bahamonde** - Desarrollo Web Tarea 2