from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios import urls as urls_usuarios
from usuarios import views as views_usuarios
from contratos import urls as urls_contratos
from obras import urls as urls_obras
from diarios import urls as urls_diarios
from utils.views import historico_edicoes


urlpatterns = [
    path('', views_usuarios.pagina_inicial, name='pagina_inicial') ,
    path('admin/', admin.site.urls),
    path('usuarios/', include(urls_usuarios)),
    path('contratos/', include(urls_contratos)),
    path('obras/', include(urls_obras)),
    path('diarios/', include(urls_diarios)),
     #rota para visualização das edições gravadas para determinado registro
    path('historico_edicoes/<str:tipo>/<int:id>/', historico_edicoes, name='historico_edicoes')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
