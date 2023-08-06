import pytz
from datetime import datetime, timedelta

F_DATE = '%Y-%m-%d'
F_DATE_TIME1 = '%Y-%m-%d %H:%M'
F_DATE_TIME2 = '%Y-%m-%d %H:%M:%S'
F_TIME1 = '%H:%M'
F_TIME2 = '%H:%M:%S'

def get_fecha_now():
    """
    Función para calcular la fecha actual en zona horaria guatemalteca.
    
    Return
    ----------
    Fecha en formato Guatemala
    """
    gtTz = pytz.timezone("America/Guatemala")
    return datetime.now(gtTz)

def get_fecha_anterior():
    """
    Función para calcular la fecha anterior respecto a la fecha actual en zona horaria guatemalteca.
    
    Return
    ----------
    Fecha en formato Guatemala
    """
    now = get_fecha_now()
    ayer = now - timedelta(days=1)
    return datetime.strptime(ayer.strftime(F_DATE), F_DATE)