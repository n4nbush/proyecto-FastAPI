import sqlite3, os, json
from contextlib import closing
from datetime import datetime
from utils.constant import grupos
from config import Config


DATABASE = Config.DATABASE



def init_db():
    os.makedirs(Config.DATABASE_FOLDER, exist_ok=True)

    """Crea la tabla si no existe"""
    with closing(get_db()) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS datos_crudos (
                FECHA TEXT,
                TIPO TEXT,
                METODO TEXT,
                CATEGORIA TEXT,
                IMPORTE REAL,
                DESCRIPCION TEXT
            )
        """)
        db.commit()
def borrar_tabla(tabla):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Sentencia SQL para borrar la tabla 'usuarios'
    # La cláusula IF EXISTS es opcional, evita errores si la tabla no existe
    cursor.execute(f'DROP TABLE IF EXISTS "{tabla}"')

    # Confirmar los cambios
    conn.commit()

    # Cerrar la conexión
    conn.close()
    print(f'Tabla{tabla}eliminada exitosamente')

def get_db():
    """Abre y retorna una conexión"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Para acceder por nombre de columna
    return conn

def traer_datos(dias:  int = 30):
    """Trae datos de la DB"""
    with closing(get_db()) as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM movimientos WHERE date(FECHA) >= date('now', ?)"
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
    fecha = fecha.replace("T", " ")
    formatos = ['%Y-%m-%d %H:%M:%S','%d/%m/%Y %H:%M:%S','%Y-%m-%d %H:%M']
    dt = None
    for formato in formatos:
        try:
            dt = datetime.strptime(fecha.strip(), formato)
            break
        except ValueError:
            continue
    if dt is None:
        print(f"No se pudo parsear la fecha: {fecha}")
        return fecha
    return dt.strftime("%d-%m-%Y %H:%M:%S")

def limpiar_monto(monto):
    monto_limpio = monto.replace("$","").replace("-","").replace(",","")

    return(monto_limpio)

def procesar_datos(listado):
    
    resultado = []
    for i in listado:
        fecha = procesado_fecha(i[0])
        tipo = i[1]
        if i[1] == "Tarjeta":
            tipo = "Gasto"
            metodo_pago = "Tarjeta"
        else:
            metodo_pago = "Debito"
        grupo = asignar_grupos(i[2])
        categoria = i[2]
        monto = limpiar_monto(i[3])
        descripcion = i[4]
        resultado.append([fecha,tipo,metodo_pago,categoria,monto,descripcion])
    return(resultado)

def filtrar(dias=30,categoria_select=None,grupo_select=None):
    listado = procesar_datos(dias)
    total = 0
    resultado=[]
    if grupo_select == "None":
        grupo_select = None
    if categoria_select == "None":
        categoria_select = None
    for fecha,tipo,grupo,categoria,monto,descripcion in listado:
        if grupo_select is not None and grupo != grupo_select:
            continue
        if categoria_select is not None and categoria != categoria_select:
            continue
        resultado.append([fecha,tipo,grupo,categoria,monto,descripcion])
    return(resultado,total)


def resumen_grupos(registro):
    
    init_db()
    for x in registro:
        with closing(get_db()) as db:
            db.execute(
                "INSERT INTO datos_crudos VALUES (?, ?, ?, ?, ?,?)",
                (x[0], x[1], x[2], x[3], x[4],x[5])
            )
            db.commit()

def obtener_datos(tabla):
    import sqlite3
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM {tabla}")
    datos = cursor.fetchall()
    
    conn.close()
    return datos

listado = obtener_datos("datos_crudos")

    