from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import os
from datetime import datetime
from werkzeug.utils import secure_filename

from config import SECRET_KEY, UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from models.db import get_session, AvisoAdopcion, Region, Comuna, Foto, ContactarPor, Comentario
from utils.validations import validar_formulario_completo, validar_comentario_completo

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_files(files, aviso_id):
    fotos_guardadas = []
    
    for file in files:
        if file and file.filename and allowed_file(file.filename):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            unique_filename = f"{aviso_id}_{timestamp}_{name}{ext}"
            
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(file_path)
            foto = Foto(
                ruta_archivo=file_path,
                nombre_archivo=unique_filename,
                actividad_id=aviso_id
            )
            fotos_guardadas.append(foto)
    
    return fotos_guardadas


@app.route('/')
def index():
    session = get_session()
    try:
        # Acá se obtienen los últimos 5 avisos ordenados por fecha de ingreso
        avisos = session.query(AvisoAdopcion)\
            .order_by(AvisoAdopcion.fecha_ingreso.desc())\
            .limit(5)\
            .all()
        
        regiones = session.query(Region).all()
        comunas = session.query(Comuna).all()
        
        return render_template('index.html', 
                             avisos=avisos, 
                             regiones=regiones, 
                             comunas=comunas)
    except Exception as e:
        flash(f'Error al cargar la portada: {str(e)}', 'error')
        return render_template('index.html', avisos=[], regiones=[], comunas=[])
    finally:
        session.close()


@app.route('/agregar-adopcion', methods=['GET', 'POST'])
def agregar_adopcion():
    session = get_session()
    
    try:
        regiones = session.query(Region).all()
        comunas = session.query(Comuna).all()
        
        if request.method == 'POST':
            
            datos = {
                'nombre': request.form.get('nombre'),
                'email': request.form.get('email'),
                'celular': request.form.get('celular'),
                'sector': request.form.get('sector'),
                'comuna_id': request.form.get('comuna_id'),
                'tipo': request.form.get('tipo'),
                'cantidad': request.form.get('cantidad'),
                'edad': request.form.get('edad'),
                'unidad_medida': request.form.get('unidad_medida'),
                'fecha_entrega': request.form.get('fecha_entrega'),
                'descripcion': request.form.get('descripcion')
            }
            
            archivos = request.files.getlist('fotos')
            contactos = []
            contactar_por = request.form.getlist('contactarPor')
            
            for red_social in contactar_por:
                identificador = request.form.get(f'contact_{red_social}')
                if identificador and identificador.strip():
                    contactos.append({
                        'red_social': red_social,
                        'identificador': identificador.strip()
                    })
            
            print(f"Contactos recibidos: {contactos}")
            print(f"Form data: {dict(request.form)}")
            
            datos['contactos'] = contactos
            #Validamos el formulario
            es_valido, errores = validar_formulario_completo(datos, archivos)
            
            if not es_valido:
                return render_template('agregar.html', 
                                     errores=errores, 
                                     datos=datos,
                                     regiones=regiones, 
                                     comunas=comunas)
            
            # Creamos el aviso en la db
            aviso = AvisoAdopcion(
                fecha_ingreso=datetime.now(),
                comuna_id=int(datos['comuna_id']),
                sector=datos['sector'] if datos['sector'] else None,
                nombre=datos['nombre'],
                email=datos['email'],
                celular=datos['celular'] if datos['celular'] else None,
                tipo=datos['tipo'],
                cantidad=int(datos['cantidad']),
                edad=int(datos['edad']),
                unidad_medida=datos['unidad_medida'],
                fecha_entrega=datetime.fromisoformat(datos['fecha_entrega'].replace('Z', '+00:00')),
                descripcion=datos['descripcion'] if datos['descripcion'] else None
            )
            
            session.add(aviso)
            session.flush()
            fotos = save_uploaded_files(archivos, aviso.id)
            for foto in fotos:
                session.add(foto)
            
            for contacto_data in contactos:
                contacto = ContactarPor(
                    nombre=contacto_data['red_social'],
                    identificador=contacto_data['identificador'],
                    actividad_id=aviso.id
                )
                session.add(contacto)
            
            session.commit()
            flash('Aviso de adopción creado exitosamente!', 'success')
            return redirect(url_for('index'))
        
        return render_template('agregar.html', 
                             regiones=regiones, 
                             comunas=comunas)
    
    except Exception as e:
        session.rollback()
        flash(f'Error al procesar el formulario: {str(e)}', 'error')
        return render_template('agregar.html', 
                             regiones=regiones, 
                             comunas=comunas)
    finally:
        session.close()


@app.route('/listado')
def listado():
    session = get_session()
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 5
        
        avisos_query = session.query(AvisoAdopcion)\
            .order_by(AvisoAdopcion.fecha_ingreso.desc())
        
        total_avisos = avisos_query.count()
        avisos = avisos_query.offset((page - 1) * per_page).limit(per_page).all()
        
        total_pages = (total_avisos + per_page - 1) // per_page
        has_prev = page > 1
        has_next = page < total_pages
        
        return render_template('listado.html',
                             avisos=avisos,
                             page=page,
                             total_pages=total_pages,
                             has_prev=has_prev,
                             has_next=has_next,
                             total_avisos=total_avisos)
    
    except Exception as e:
        flash(f'Error al cargar el listado: {str(e)}', 'error')
        return render_template('listado.html', avisos=[], page=1, total_pages=0)
    finally:
        session.close()


@app.route('/detalle/<int:aviso_id>')
def detalle(aviso_id):
    session = get_session()
    
    try:
        aviso = session.query(AvisoAdopcion)\
            .filter(AvisoAdopcion.id == aviso_id)\
            .first()
        
        if not aviso:
            flash('Aviso no encontrado', 'error')
            return redirect(url_for('listado'))
        
        return render_template('detalle.html', aviso=aviso)
    
    except Exception as e:
        flash(f'Error al cargar el detalle: {str(e)}', 'error')
        return redirect(url_for('listado'))
    finally:
        session.close()


@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')


@app.route('/api/comunas/<int:region_id>')
def api_comunas(region_id):
    session = get_session()
    
    try:
        comunas = session.query(Comuna)\
            .filter(Comuna.region_id == region_id)\
            .all()
        
        comunas_data = [{'id': c.id, 'nombre': c.nombre} for c in comunas]
        return jsonify(comunas_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/api/estadisticas/avisos-por-dia')
def api_avisos_por_dia():
    session = get_session()
    try:
        avisos = session.query(
            AvisoAdopcion.fecha_ingreso
        ).all()
        
        avisos_por_dia = {}
        for aviso in avisos:
            fecha = aviso.fecha_ingreso.strftime('%Y-%m-%d')
            avisos_por_dia[fecha] = avisos_por_dia.get(fecha, 0) + 1
        
        dias = sorted(avisos_por_dia.keys())
        cantidades = [avisos_por_dia[dia] for dia in dias]
        
        return jsonify({
            'dias': dias,
            'cantidades': cantidades
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/estadisticas/avisos-por-tipo')
def api_avisos_por_tipo():
    session = get_session()
    try:
        perros = session.query(AvisoAdopcion)\
            .filter(AvisoAdopcion.tipo == 'perro')\
            .count()
        
        gatos = session.query(AvisoAdopcion)\
            .filter(AvisoAdopcion.tipo == 'gato')\
            .count()
        
        return jsonify({
            'perros': perros,
            'gatos': gatos
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/estadisticas/avisos-por-mes')
def api_avisos_por_mes():
    session = get_session()
    try:
        avisos = session.query(
            AvisoAdopcion.fecha_ingreso,
            AvisoAdopcion.tipo
        ).all()
        
        avisos_por_mes = {}
        for aviso in avisos:
            mes = aviso.fecha_ingreso.strftime('%Y-%m')
            if mes not in avisos_por_mes:
                avisos_por_mes[mes] = {'perros': 0, 'gatos': 0}
            
            if aviso.tipo == 'perro':
                avisos_por_mes[mes]['perros'] += 1
            else:
                avisos_por_mes[mes]['gatos'] += 1
        
        meses = sorted(avisos_por_mes.keys())
        perros = [avisos_por_mes[mes]['perros'] for mes in meses]
        gatos = [avisos_por_mes[mes]['gatos'] for mes in meses]
        
        meses_nombres = []
        for mes in meses:
            fecha = datetime.strptime(mes, '%Y-%m')
            mes_nombre = fecha.strftime('%B %Y')
            meses_nombres.append(mes_nombre)
        
        return jsonify({
            'meses': meses_nombres,
            'perros': perros,
            'gatos': gatos
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/comentarios/<int:aviso_id>', methods=['GET'])
def api_obtener_comentarios(aviso_id):
    session = get_session()
    try:
        comentarios = session.query(Comentario)\
            .filter(Comentario.aviso_id == aviso_id)\
            .order_by(Comentario.fecha.desc())\
            .all()
        
        comentarios_data = []
        for comentario in comentarios:
            comentarios_data.append({
                'id': comentario.id,
                'nombre': comentario.nombre,
                'texto': comentario.texto,
                'fecha': comentario.fecha.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify(comentarios_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/comentarios', methods=['POST'])
def api_agregar_comentario():
    session = get_session()
    try:
        datos = request.get_json()
        
        es_valido, errores = validar_comentario_completo(datos)
        
        if not es_valido:
            return jsonify({'success': False, 'errores': errores}), 400
        
        comentario = Comentario(
            nombre=datos['nombre'].strip(),
            texto=datos['texto'].strip(),
            fecha=datetime.now(),
            aviso_id=int(datos['aviso_id'])
        )
        
        session.add(comentario)
        session.commit()
        
        return jsonify({
            'success': True,
            'comentario': {
                'id': comentario.id,
                'nombre': comentario.nombre,
                'texto': comentario.texto,
                'fecha': comentario.fecha.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    except Exception as e:
        session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
