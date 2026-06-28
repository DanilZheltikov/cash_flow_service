from django.contrib import admin
from django.urls import include, path

handler403 = 'custom_error.views.error_handler'
handler404 = 'custom_error.views.error_handler'
handler500 = 'custom_error.views.error_handler'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('', include('transaction.urls', namespace='transaction')),
]
