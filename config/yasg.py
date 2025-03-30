from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Define API schema and metadata
schema_view = get_schema_view(
    openapi.Info(
        title="AutoPartsEcommerce API",
        default_version="v1",
        description="API documentation for the AutoPartsEcommerce project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@autopartsecommerce.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # Allow public access to the documentation
    permission_classes=[permissions.AllowAny],  # No authentication required
)

# Define URL patterns for Swagger and ReDoc
urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
