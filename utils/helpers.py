from datetime import datetime
import shutil, json, os
from config import Config


def backup():
    ahora = datetime.now()
    os.makedirs(Config.BACKUP_FOLDER, exist_ok=True)
    db = Config.DATABASE
    ultimo_backup = Config.ULTIMOBACKUP
    try:
        with open(ultimo_backup,'r') as f:
            fecha_str = json.load(f)
            fecha_ultimo_backup = datetime.fromisoformat(fecha_str)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        print("Archivo json de fecha backup no existe, creando uno nuevo")
        fecha_ultimo_backup = datetime.now()
        with open(ultimo_backup, 'w', encoding='utf-8') as archivo:
            json.dump(fecha_ultimo_backup.isoformat(), archivo, indent=4, ensure_ascii=False)
            nombre_backup=f"backup/gastos_{ahora.strftime('%Y-%m-%d_%H-%M')}.db"
            shutil.copy2(db,nombre_backup)


    diff = ahora - fecha_ultimo_backup
    diff = diff.days


    if diff > 15:
        print("Creando nuevo backup")
        nombre_backup=f"gastos_{ahora.datetimestr('%Y-%m-%d_%H-%M')}.db"
        shutil.copy2(db,nombre_backup)
        fecha_ultimo_backup=datetime.now()
        print("Actualizando fecha del ultimo backup")
        with open(ultimo_backup, 'w', encoding='utf-8') as archivo:
            json.dump(fecha_ultimo_backup.isoformat(), archivo, indent=4, ensure_ascii=False)