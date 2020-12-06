from django.urls import include, path
from rest_framework import routers
from secretpass import views, webviews

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"accounts", views.AccountViewSet)

urlpatterns = [
    path("", webviews.index, name="spindex"),
    path("create/", webviews.create, name="spcreate"),
    path("edit/<int:acc_id>/", webviews.edit, name="spedit"),
    path("movetotrash/<int:acc_id>/", webviews.movetotrash, name="spmovetotrash"),
    path("trash/", webviews.trash, name="sptrash"),
    path("delete/<int:acc_id>/", webviews.delete, name="spdelete"),
    path("api/accounts/search/", views.search_account),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]
