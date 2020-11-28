from django.urls import include, path
from rest_framework import routers
from secretpass import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"accounts", views.AccountViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path('api/generate_password/', views.generate_password),
    path("api-auth/", include("rest_framework.urls")),
]
