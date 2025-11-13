# 🎓 Sistema de Matrícula Universitaria

Sistema completo de gestión académica desarrollado en Python con SQLAlchemy, organizado bajo arquitectura de capas modular.

## 📁 Estructura del Proyecto
```
proyecto_universidad/
│
├── auxiliares/          # Funciones de apoyo y utilidades
│   ├── __init__.py
│   ├── constantes.py    # Constantes del sistema
│   ├── validadores.py   # Validaciones de datos
│   └── formateadores.py # Formateo y presentación
│
├── datos/               # Capa de acceso a datos (DAO)
│   ├── __init__.py
│   ├── conexion.py      # Configuración de BD
│   ├── estudiante_dao.py
│   ├── profesor_dao.py
│   ├── curso_dao.py
│   ├── matricula_dao.py
│   └── historial_dao.py
│
├── negocio/             # Lógica de negocio
│   ├── __init__.py
│   ├── gestor_estudiantes.py
│   ├── gestor_profesores.py
│   ├── gestor_cursos.py
│   ├── gestor_matriculas.py
│   └── gestor_sistema.py
│
├── modelos/             # Modelos ORM (Entidades)
│   ├── __init__.py
│   ├── estudiante.py
│   ├── profesor.py
│   ├── curso.py
│   ├── matricula.py
│   └── historial.py
│
├── iu/                  # Interfaz de Usuario (CLI)
│   ├── __init__.py
│   ├── menu_principal.py
│   ├── menu_estudiantes.py
│   ├── menu_profesores.py
│   ├── menu_cursos.py
│   └── menu_reportes.py
│
├── requirements.txt
├── main.py
└── README.md
```

## 🏗️ Arquitectura en Capas

### 1. **Capa Auxiliares**
Funciones de apoyo que no pertenecen a la lógica principal:
- **Validadores**: RUT, email, notas, créditos, semestre
- **Formateadores**: Salida formateada, tablas, títulos
- **Constantes**: Valores fijos del sistema

### 2. **Capa Datos (DAO)**
Acceso y persistencia de datos:
- Operaciones CRUD puras
- Consultas a base de datos
- Transacciones y rollback

### 3. **Capa Negocio**
Lógica principal del sistema:
- Validaciones complejas
- Reglas de negocio
- Orquestación de operaciones

### 4. **Capa Modelos**
Entidades del dominio:
- Mapeo ORM con SQLAlchemy
- Relaciones entre tablas
- Métodos auxiliares de entidad

### 5. **Capa IU (Interfaz)**
Interacción con el usuario:
- Menús de consola
- Captura de entrada
- Presentación de resultados

## 🚀 Instalación

### 1. Requisitos Previos
```bash
Python 3.8+
MySQL 5.7+
pip
```

### 2. Configurar Base de Datos

Editar `datos/conexion.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'universidad'
}
```

### 3. Crear Base de Datos
Ejecutar el script SQL proporcionado en MySQL.

### 4. Ejecutar
```bash
python main.py
```

## 💡 Funcionalidades

### Gestión de Estudiantes
✅ Registrar con validaciones  
✅ Listar por carrera  
✅ Actualizar información  
✅ Cambiar estado (Activo/Inactivo/Egresado)  
✅ Estadísticas por carrera  

### Gestión de Profesores
✅ Registrar profesores  
✅ Asignar cursos  
✅ Verificar carga académica  
✅ Listar cursos dictados  

### Gestión de Cursos
✅ Crear cursos  
✅ Asignar profesor  
✅ Ver estudiantes inscritos  
✅ Verificar disponibilidad  

### Gestión de Matrículas
✅ Matricular con validaciones  
✅ Validar créditos máximos (20)  
✅ Validar capacidad del curso  
✅ Retirar de curso  
✅ Registrar notas  

### Reportes
✅ Reporte completo de estudiante  
✅ Reporte completo de curso  
✅ Reporte completo de profesor  
✅ Historial académico  
✅ Estadísticas generales  

## 📊 Flujo de Datos
```
Usuario → IU → Negocio → Datos → Base de Datos
                  ↓
              Auxiliares
```

## 🎯 Principios Aplicados

- **Separación de Responsabilidades**: Cada capa tiene un propósito único
- **Bajo Acoplamiento**: Módulos independientes
- **Alta Cohesión**: Funcionalidades relacionadas juntas
- **DRY**: No repetir código
- **SOLID**: Principios de diseño orientado a objetos

## 🔒 Validaciones Implementadas

### Estudiantes
- ✅ RUT válido
- ✅ Email formato correcto
- ✅ Máximo 20 créditos por semestre
- ✅ No duplicar matrículas

### Profesores
- ✅ Máximo 5 cursos por profesor
- ✅ Email único

### Cursos
- ✅ Código único
- ✅ Capacidad máxima respetada
- ✅ Semestre formato válido (YYYY-1 o YYYY-2)

### Notas
- ✅ Rango 1.0 - 7.0
- ✅ Aprobación >= 4.0

## 📝 Ejemplo de Uso
```python
# 1. Registrar estudiante
estudiante, error = GestorEstudiantes.crear_estudiante(
    session,
    rut="20.123.456-7",
    nombre="Pedro",
    apellido="Martínez",
    email="pedro@mail.com",
    carrera="Ingeniería Civil"
)

# 2. Matricular en curso
exito, mensaje = GestorMatriculas.matricular_estudiante(
    session,
    estudiante_id=1,
    curso_id=5
)

# 3. Registrar nota
exito, mensaje = GestorMatriculas.registrar_nota(
    session,
    estudiante_id=1,
    curso_id=5,
    semestre="2024-1",
    nota=6.5
)

# 4. Generar reporte
reporte, error = GestorSistema.generar_reporte_estudiante(
    session,
    estudiante_id=1
)
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **SQLAlchemy 2.0**: ORM
- **PyMySQL**: Conector MySQL
- **MySQL**: Base de datos

## 📧 Contacto

Sistema desarrollado como proyecto educativo de Programación Orientada a Objetos.

---

**Versión**: 2.0  
**Fecha**: 2024  
**Licencia**: Educativo
