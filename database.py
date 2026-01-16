import sqlite3
from contextlib import closing
from datetime import datetime

DATABASE = 'database/database.db'

grupos={
    "🧾 Finanzas y Deudas":["Deuda Viejo","Tarjeta Visa","Tarjeta Master","Deuda Banco"],
    "🛒 Consumo y Vida Diaria":["Gastos Hormiga", "Comida Trabajo","Almacén"],
    "🏠 Hogar y Servicios":["Internet","Celular","Ferretería","Luz","Servicios Digitales"],
    "👨‍👩‍👦 Familia":["Niñera","Boris","Agustina"],
    "🧍‍♂️ Bienestar y Personales":["Gustos","Ropa","GIM","Farmacia","Psicóloga","Peluquería","Indoor"],
    "🚗 Transporte y Movilidad":["Uber","Moto","Clio","SUBE"],
    "Otros Gastos":["Otros Gastos"],
    "Ingresos":["Salario","Inversiones","Regalo","Reembolso","Otros Ingresos"]
}

def init_db():
    """Crea la tabla si no existe"""
    with closing(get_db()) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS datos (
                FECHA TEXT,
                TIPO TEXT,
                MOTIVO TEXT,
                IMPORTE REAL,
                DESCRIPCION TEXT
            )
        """)
        db.commit()

def get_db():
    """Abre y retorna una conexión"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
    return conn

def traer_datos(dias:  int = 30):
    """Trae datos de la DB"""
    with closing(get_db()) as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM datos WHERE date(FECHA) >= date('now', ?)"
        params = [f'-{dias} day']
        
        query += " ORDER BY FECHA DESC"
        cursor.execute(query, params)
        
        resultados = [list(row) for row in cursor.fetchall()]        
        return (resultados)

def asignar_grupos(categoria):
    
    for nombre_grupo,lista_categoria in grupos.items():
        if categoria in lista_categoria:
            return(nombre_grupo)

def procesado_fecha(fecha):
    fecha = fecha.replace("T"," ")
    dt = datetime.strptime(fecha, "%Y-%m-%d %H:%M")
    
    fechas = dt.strftime("%d/%m/%Y %H:%M")
    return(fechas)

def procesar_datos(dias=30):
    listado = traer_datos(dias)
    resultado = []
    for i in listado:
        fecha = procesado_fecha((i[0]))
        tipo = i[1]
        grupo = asignar_grupos(i[2])
        categoria = i[2]
        monto = i[3]
        descripcion = i[4]
        resultado.append([fecha,tipo,grupo,categoria,monto,descripcion])
    return(resultado)

def filtrar(dias=30,categoria_select=None,grupo_select=None):
    listado = procesar_datos(dias)
    total = 0
    resultado=[]
    for fecha,tipo,grupo,categoria,monto,descripcion in listado:
        if grupo_select is not None and grupo != grupo_select:
            continue
        if categoria_select is not None and categoria != categoria_select:
            continue
        total += monto
        resultado.append([fecha,tipo,grupo,categoria,monto,descripcion])
    return(resultado,total)
