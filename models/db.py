from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import DATABASE_URI


engine = create_engine(DATABASE_URI, echo=False, pool_pre_ping=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
def get_session():
    """Retorna una nueva sesión de base de datos"""
    return SessionLocal()


# Modelos

class Region(Base):
    __tablename__ = 'region'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    
    comunas = relationship('Comuna', back_populates='region')
    
    def __repr__(self):
        return f"<Region(id={self.id}, nombre='{self.nombre}')>"


class Comuna(Base):
    __tablename__ = 'comuna'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    

    region = relationship('Region', back_populates='comunas')
    avisos = relationship('AvisoAdopcion', back_populates='comuna')
    
    def __repr__(self):
        return f"<Comuna(id={self.id}, nombre='{self.nombre}', region_id={self.region_id})>"


class AvisoAdopcion(Base):
    __tablename__ = 'aviso_adopcion'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, nullable=False)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100), nullable=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    tipo = Column(Enum('gato', 'perro', name='tipo_enum'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum('a', 'm', name='unidad_medida_enum'), nullable=False)
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(Text(500), nullable=True)
    
    comuna = relationship('Comuna', back_populates='avisos')
    fotos = relationship('Foto', back_populates='aviso', cascade='all, delete-orphan')
    contactos = relationship('ContactarPor', back_populates='aviso', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<AvisoAdopcion(id={self.id}, tipo='{self.tipo}', cantidad={self.cantidad})>"


class Foto(Base):
    __tablename__ = 'foto'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('aviso_adopcion.id'), nullable=False)
    
    aviso = relationship('AvisoAdopcion', back_populates='fotos')
    
    def __repr__(self):
        return f"<Foto(id={self.id}, nombre='{self.nombre_archivo}')>"


class ContactarPor(Base):
    __tablename__ = 'contactar_por'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra', name='contacto_enum'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('aviso_adopcion.id'), nullable=False)
    
    aviso = relationship('AvisoAdopcion', back_populates='contactos')
    
    def __repr__(self):
        return f"<ContactarPor(id={self.id}, nombre='{self.nombre}', identificador='{self.identificador}')>"


# Función para inicializar la base de datos (crear tablas si no existen)
def init_db():
    """Crea todas las tablas en la base de datos"""
    Base.metadata.create_all(engine)


# Función para cerrar la sesión
def close_session(session):
    """Cierra una sesión de base de datos"""
    if session:
        session.close()

