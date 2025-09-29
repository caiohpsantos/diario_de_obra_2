from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios import urls as urls_usuarios
from usuarios import views as views_usuarios
from diarios import urls as urls_diarios

urlpatterns = [
    path('', views_usuarios.pagina_inicial, name='pagina_inicial') ,
    path('admin/', admin.site.urls),
    path('usuarios/', include(urls_usuarios)),
    path('diarios/', include(urls_diarios))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
