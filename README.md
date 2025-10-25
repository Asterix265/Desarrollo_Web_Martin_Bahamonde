# Tarea 2 y 3: Sistema de Adopción de Mascotas con Flask

Una aplicación web completa para gestión de adopción de perros y gatos, desarrollada con Flask, SQLAlchemy y MySQL. Incluye validaciones del lado del servidor y cliente, estadísticas dinámicas con gráficos interactivos y sistema de comentarios.

## Características

- **Formulario de adopción** con validaciones JavaScript y del servidor
- **Listado paginado** de avisos de adopción
- **Vista detallada** con galería de fotos y modal
- **Sistema de comentarios** en tiempo real con AJAX
- **Estadísticas dinámicas** con graficos de highcharts
- **API REST** para comunas, estadísticas y comentarios
- **Gestión de archivos** con validación de imágenes
- **Base de datos MySQL** con relaciones complejas

## Tecnologías

- **Backend**: Flask 3.0.0
- **Base de datos**: MySQL con SQLAlchemy 2.0.23
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Highcharts
- **AJAX**: Fetch API para comunicación asíncrona
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
SOURCE database/tabla-comentario.sql;
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

##### TAREA 2 #######
### 1. Agregar Aviso de Adopción 
- Formulario completo con validaciones duales (cliente + servidor)
- Subida de múltiples imágenes (1-5 fotos, formatos: PNG, JPG, JPEG, WEBP)
- Selección dinámica de región y comuna
- Múltiples métodos de contacto (hasta 5)
- Modal de confirmación antes de enviar
- Mensaje de éxito tras agregar
- Almacenamiento seguro de archivos

### 2. Listado de Avisos 
- Paginación (5 avisos por página)
- Información resumida: tipo, cantidad, edad, región, comuna
- Foto principal de cada aviso
- Enlaces a vista detallada
- Navegación entre páginas

### 3. Detalle de Aviso
- Información completa del aviso
- Galería de fotos con modal para ampliar
- Datos de contacto (email, celular, redes sociales)
- Información de la mascota (tipo, edad, descripción)
- Ubicación (región, comuna, sector)
- Sistema de comentarios interactivo 


###### TAREA 3 ######

### 4. Sistema de Comentarios 
- Formulario para agregar comentarios (nombre 3-80 caracteres, texto 5-300 caracteres)
- Envío asíncrono con AJAX (Fetch API)
- Validaciones en cliente y servidor
- Lista de comentarios ordenados por fecha (más recientes primero)
- Actualización automática sin recargar página
- Manejo de errores con mensajes informativos

### 5. Estadísticas Dinámicas
- **Gráfico de líneas**: Cantidad de avisos por día
- **Gráfico de torta**: Distribución de avisos por tipo (perros vs gatos)
- **Gráfico de barras agrupadas**: Avisos por mes diferenciando perros y gatos
- Datos obtenidos en tiempo real desde la base de datos vía API REST
- Gráficos interactivos con Highcharts 
- Responsive y con colores diferenciados por tipo


### Separación de Responsabilidades
- **app.py**: Rutas Flask, manejo de requests/responses, integración de componentes
- **models/db.py**: Definición de modelos y acceso a BD (framework-agnostic)
- **utils/validations.py**: Lógica de validación pura (reutilizable)
- **config.py**: Configuración centralizada
- **templates/**: Presentación (Jinja2)
- **static/**: Assets del cliente

## Seguridad

### Prevención de Ataques
- **SQL Injection**: SQLAlchemy conqueries parametrizadas
- **XSS**: Jinja2 escapa automáticamente variables en templates
- **CSRF**: Flask con SECRET_KEY
- **File Upload**: Validación de extensiones, tamaños y nombres seguros

## Validaciones

#### Cliente (JavaScript - UX)
- Formato de email (regex)
- Formato de celular (+NNN.NNNNNNNN)
- Fechas válidas
- Archivos de imagen
- Campos obligatorios
- Feedback inmediato al usuario

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
- `comentario`: Comentarios de avisos (Tarea 3)

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
- **Highcharts**: Se utiliza bajo licencia gratuita para uso educativo/personal (https://www.highcharts.com/products/highcharts/#non-commercial). Puesto es para una tarea universitaia.

##  Autor

**Martin Bahamonde** - Desarrollo Web Tareas 2 y 3