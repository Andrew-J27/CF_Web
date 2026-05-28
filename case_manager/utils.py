# cases/utils.py
from django.db import connection, transaction
from django.db.utils import DatabaseError

def soft_delete_case_with_user(case_id, user):
    """Realiza soft delete pasando el usuario de Django"""
    
    user_info = f"{user.id}|{user.username}"
    
    try:
        with connection.cursor() as cursor:
            # Establecer CONTEXT_INFO con el usuario de Django
            cursor.execute(
                "SET CONTEXT_INFO = ?", 
                [user_info.encode('utf-8')]
            )
            
            # Realizar el soft delete (esto activará el trigger)
            cursor.execute("""
                UPDATE [case] 
                SET active = 0, updated_at = GETDATE()
                WHERE id = ?
            """, [case_id])
            
            return True
            
    except DatabaseError as e:
        # El error del trigger se captura aquí
        error_message = str(e)
        print(f"Error en soft delete: {error_message}")
        raise Exception(error_message)  # O manejar el error como prefieras