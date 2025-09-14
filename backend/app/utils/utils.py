# file: app/models/utils.py

from sqlalchemy import inspect
from sqlalchemy.orm import UnloadedAttributeError # <-- PATH BENAR

def safe_repr(instance) -> str:
    """
    Membuat representasi string yang aman untuk objek SQLAlchemy.
    Tidak akan pernah memicu lazy loading atau attribute refresh.
    """
    cls_name = instance.__class__.__name__
    
    # Gunakan inspect untuk mendapatkan state tanpa memicu loader
    state = inspect(instance)
    
    # Coba dapatkan primary key, jika sudah dimuat
    try:
        # state.identity adalah tuple dari primary key
        pk = ", ".join(map(str, state.identity)) if state.identity else "None"
    except UnloadedAttributeError:
        pk = "Unloaded"
        
    return f"<{cls_name}(pk={pk})>"