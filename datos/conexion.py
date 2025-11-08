#============================================
# datos/conexion.py
# Configuración y gestión de la conexión a la base de datos
#============================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

#============================================
# Configuración de la base de datos
#============================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'triton12',  # Contraseña
    'database': 'universidad'
}

#============================================
# Crear URL de conexión
#============================================
DATABASE_URL = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    f"?charset=utf8mb4"
)

#============================================
# Crear engine con pool de conexiones
#============================================
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    echo=False  # Cambiar a True para ver queries SQL
)

#============================================
# Crear sesión
#============================================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#============================================
# Base para los modelos
#============================================
Base = declarative_base()

#============================================
# Generador de sesiones de base de datos
# Uso con context manager:
# with get_session() as session:
#     # operaciones
#============================================
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

#============================================
# Inicializa la base de datos creando todas las tablas
#============================================
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada correctamente")

#============================================
# Elimina todas las tablas (usar con precaución)
#============================================
def drop_all():
    Base.metadata.drop_all(bind=engine)
    print("Todas las tablas han sido eliminadas")
