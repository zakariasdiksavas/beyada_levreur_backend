from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('v1/admin/', admin.site.urls),
    path('v1/auth/', include('authentication.urls')),
    path('v1/base/', include('base.urls')),
    path('v1/charge/', include('charge.urls')),
    path('v1/commands/', include('commands.urls')),
    path('v1/direct-sales/', include('direct_sales.urls')),
    path('v1/paiements/', include('paiements.urls')),
    path('v1/production/', include('production.urls')),
    path('v1/inventaire/', include('inventaire.urls')),
    path('v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
