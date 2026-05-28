from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            
            raise PermissionDenied("Debes iniciar sesión")
        if request.user.systemuser.role != 'admin':

            raise PermissionDenied("Se requieren permisos de administrador")
        return view_func(request, *args, **kwargs)
    return wrapper
 
