from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from product.views import ProductViewSet

router = SimpleRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls'))
]

urlpatterns += router.urls
