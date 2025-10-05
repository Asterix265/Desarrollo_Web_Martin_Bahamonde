import re
import os
from datetime import datetime, timedelta
from config import VALIDATION_RULES, ALLOWED_EXTENSIONS, MAX_FILE_SIZE, MAX_PHOTOS, MIN_PHOTOS


def validar_nombre(nombre):
    if not nombre or not isinstance(nombre, str):
        return False, "El nombre es requerido"
    
    nombre = nombre.strip()
    
    if len(nombre) < VALIDATION_RULES['nombre']['min_length']:
        return False, f"El nombre debe tener al menos {VALIDATION_RULES['nombre']['min_length']} caracteres"
    
    if len(nombre) > VALIDATION_RULES['nombre']['max_length']:
        return False, f"El nombre no puede exceder {VALIDATION_RULES['nombre']['max_length']} caracteres"
    
    # Solo letras, espacios, guiones y acentos
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-]+$', nombre):
        return False, "El nombre solo puede contener letras, espacios, guiones y acentos"
    
    return True, ""


def validar_email(email):
    if not email or not isinstance(email, str):
        return False, "El email es requerido"
    
    email = email.strip().lower()
    
    if len(email) > VALIDATION_RULES['email']['max_length']:
        return False, f"El email no puede exceder {VALIDATION_RULES['email']['max_length']} caracteres"
    
    # Patrón del email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "El formato del email no es válido"
    
    return True, ""


def validar_celular(celular):
    if not celular:
        return True, ""
    
    if not isinstance(celular, str):
        return False, "El celular debe ser texto"
    
    celular = celular.strip()
    
    if len(celular) > VALIDATION_RULES['celular']['max_length']:
        return False, f"El celular no puede exceder {VALIDATION_RULES['celular']['max_length']} caracteres"
    
    # Patrón: +NNN.NNNNNNNN 
    celular_pattern = r'^\+\d{3}\.\d{8}$'
    if not re.match(celular_pattern, celular):
        return False, "El celular debe tener formato +NNN.NNNNNNNN (ej: +569.12345678)"
    
    return True, ""


def validar_sector(sector):
    if not sector:
        return True, ""  # Sector es opcional
    
    if not isinstance(sector, str):
        return False, "El sector debe ser texto"
    
    sector = sector.strip()
    
    if len(sector) > VALIDATION_RULES['sector']['max_length']:
        return False, f"El sector no puede exceder {VALIDATION_RULES['sector']['max_length']} caracteres"
    
    return True, ""


def validar_cantidad_edad(valor, campo_nombre):
    if not valor:
        return False, f"La {campo_nombre} es requerida"
    
    try:
        valor_int = int(valor)
        if valor_int < VALIDATION_RULES['cantidad_edad']['min_value']:
            return False, f"La {campo_nombre} debe ser mayor o igual a {VALIDATION_RULES['cantidad_edad']['min_value']}"
        return True, ""
    except (ValueError, TypeError):
        return False, f"La {campo_nombre} debe ser un número entero"


def validar_fecha_entrega(fecha_entrega_str):
    if not fecha_entrega_str:
        return False, "La fecha de entrega es requerida"
    
    try:
        fecha_entrega = datetime.fromisoformat(fecha_entrega_str.replace('Z', '+00:00'))
        
        fecha_minima = datetime.now() + timedelta(hours=3)
        
        if fecha_entrega < fecha_minima:
            return False, "La fecha de entrega debe ser al menos 3 horas después de ahora"
        
        return True, ""
    except (ValueError, TypeError):
        return False, "El formato de fecha no es válido"


def validar_descripcion(descripcion):
    if not descripcion:
        return True, ""
    
    if not isinstance(descripcion, str):
        return False, "La descripción debe ser texto"
    
    if len(descripcion) > VALIDATION_RULES['descripcion']['max_length']:
        return False, f"La descripción no puede exceder {VALIDATION_RULES['descripcion']['max_length']} caracteres"
    
    return True, ""


def validar_archivo(archivo):
    if not archivo:
        return False, "Archivo requerido"
    
    if not hasattr(archivo, 'filename') or not archivo.filename:
        return False, "Nombre de archivo requerido"
    
    # Verificar extensión
    nombre_archivo = archivo.filename.lower()
    extension = os.path.splitext(nombre_archivo)[1][1:]
    
    if extension not in ALLOWED_EXTENSIONS:
        return False, f"Tipo de archivo no permitido. Extensiones válidas: {', '.join(ALLOWED_EXTENSIONS)}"
    
    if hasattr(archivo, 'content_length') and archivo.content_length:
        if archivo.content_length > MAX_FILE_SIZE:
            return False, f"El archivo es muy grande. Tamaño máximo: {MAX_FILE_SIZE // (1024*1024)} MB"
    
    return True, ""


def validar_archivos(archivos):
    if not archivos:
        return False, "Se requiere al menos una foto"
    
    if not isinstance(archivos, list):
        archivos = [archivos]
    
    archivos_validos = [archivo for archivo in archivos if archivo and hasattr(archivo, 'filename') and archivo.filename]
    
    if len(archivos_validos) < MIN_PHOTOS:
        return False, f"Se requiere al menos {MIN_PHOTOS} foto"
    
    if len(archivos_validos) > MAX_PHOTOS:
        return False, f"Máximo {MAX_PHOTOS} fotos permitidas"
    
    # Validar cada archivo
    for i, archivo in enumerate(archivos_validos):
        es_valido, mensaje = validar_archivo(archivo)
        if not es_valido:
            return False, f"Foto {i+1}: {mensaje}"
    
    return True, ""


def validar_identificador_contacto(identificador):
    if not identificador or not isinstance(identificador, str):
        return False, "El identificador es requerido"
    
    identificador = identificador.strip()
    
    if len(identificador) < VALIDATION_RULES['identificador_contacto']['min_length']:
        return False, f"El identificador debe tener al menos {VALIDATION_RULES['identificador_contacto']['min_length']} caracteres"
    
    if len(identificador) > VALIDATION_RULES['identificador_contacto']['max_length']:
        return False, f"El identificador no puede exceder {VALIDATION_RULES['identificador_contacto']['max_length']} caracteres"
    
    return True, ""


def validar_tipo_mascota(tipo):
    if not tipo:
        return False, "El tipo de mascota es requerido"
    
    if tipo not in ['gato', 'perro']:
        return False, "El tipo de mascota debe ser 'gato' o 'perro'"
    
    return True, ""


def validar_unidad_medida(unidad):
    if not unidad:
        return False, "La unidad de medida es requerida"
    
    if unidad not in ['a', 'm']:
        return False, "La unidad de medida debe ser 'a' (años) o 'm' (meses)"
    
    return True, ""


def validar_comuna_id(comuna_id):
    if not comuna_id:
        return False, "La comuna es requerida"
    
    try:
        comuna_int = int(comuna_id)
        if comuna_int <= 0:
            return False, "ID de comuna inválido"
        return True, ""
    except (ValueError, TypeError):
        return False, "ID de comuna debe ser un número"


def validar_contacto_red_social(red_social, identificador):
    if not red_social:
        return False, "La red social es requerida"
    
    redes_validas = ['whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra']
    if red_social not in redes_validas:
        return False, f"Red social no válida. Opciones: {', '.join(redes_validas)}"
    
    return validar_identificador_contacto(identificador)


def validar_formulario_completo(datos, archivos):
    errores = {}
    
    es_valido, mensaje = validar_nombre(datos.get('nombre'))
    if not es_valido:
        errores['nombre'] = mensaje
    
    es_valido, mensaje = validar_email(datos.get('email'))
    if not es_valido:
        errores['email'] = mensaje
    
    es_valido, mensaje = validar_celular(datos.get('celular'))
    if not es_valido:
        errores['celular'] = mensaje
    
    es_valido, mensaje = validar_sector(datos.get('sector'))
    if not es_valido:
        errores['sector'] = mensaje
    
    es_valido, mensaje = validar_cantidad_edad(datos.get('cantidad'), 'cantidad')
    if not es_valido:
        errores['cantidad'] = mensaje
    
    es_valido, mensaje = validar_cantidad_edad(datos.get('edad'), 'edad')
    if not es_valido:
        errores['edad'] = mensaje
    
    es_valido, mensaje = validar_tipo_mascota(datos.get('tipo'))
    if not es_valido:
        errores['tipo'] = mensaje
    
    es_valido, mensaje = validar_unidad_medida(datos.get('unidad_medida'))
    if not es_valido:
        errores['unidad_medida'] = mensaje
    
    es_valido, mensaje = validar_fecha_entrega(datos.get('fecha_entrega'))
    if not es_valido:
        errores['fecha_entrega'] = mensaje
    
    es_valido, mensaje = validar_descripcion(datos.get('descripcion'))
    if not es_valido:
        errores['descripcion'] = mensaje
    
    es_valido, mensaje = validar_comuna_id(datos.get('comuna_id'))
    if not es_valido:
        errores['comuna_id'] = mensaje
    
    # Validar archivos
    es_valido, mensaje = validar_archivos(archivos)
    if not es_valido:
        errores['fotos'] = mensaje
    
    contactos = datos.get('contactos', [])
    if not contactos:
        errores['contactos'] = "Se requiere al menos un método de contacto"
    else:
        for i, contacto in enumerate(contactos):
            red_social = contacto.get('red_social')
            identificador = contacto.get('identificador')
            es_valido, mensaje = validar_contacto_red_social(red_social, identificador)
            if not es_valido:
                errores[f'contacto_{i}'] = mensaje
    
    return len(errores) == 0, errores
