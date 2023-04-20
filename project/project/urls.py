
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500, url

from django.views.static import serve

urlpatterns = [
    path('khclubdashboard/', admin.site.urls),
    path('', include('main.urls'  , namespace='main')),
    path('', include('users.urls'  , namespace='users')),
    path('competitions/', include('competitions.urls'  , namespace='competitions')),
    path('', include('category.urls'  , namespace='category')),
]

handler404 = 'main.views.handel404'
handler500 = 'main.views.handel500'


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
    
    
    

admin.site.site_header = "إدارة النادي العلمي بخليص"
admin.site.site_title = "النادي العلمي بخليص"
admin.site.index_title = "إدارة الموقع"