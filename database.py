import sqlite3
from contextlib import closing

DATABASE = 'database/database.db'

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

def traer_datos(dias:  int = 60):
    """Trae datos de la DB"""
    with closing(get_db()) as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM datos WHERE date(FECHA) >= date('now', ?)"
        params = [f'-{dias} day']
        
        query += " ORDER BY FECHA DESC"
        cursor.execute(query, params)
        
        resultados = [list(row) for row in cursor.fetchall()]        
        return (resultados)

