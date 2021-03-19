from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth import views as auth_views
from rest_framework import routers
from secretpass import views, webviews
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"accounts", views.AccountViewSet)

urlpatterns = [
    path("", webviews.index, name="spindex"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="secretpass/login.html"),
        name="splogin",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="secretpass/logout.html"),
        name="splogout",
    ),
    path("signup/", webviews.SignUpView.as_view(), name="spsignup"),
    path("create/", webviews.create, name="spcreate"),
    path("edit/<int:acc_id>/", webviews.edit, name="spedit"),
    path("decrypt/<int:acc_id>/", webviews.decrypt, name="spdecrypt"),
    path("movetotrash/<int:acc_id>/", webviews.movetotrash, name="spmovetotrash"),
    path("restore/<int:acc_id>/", webviews.restore, name="sprestore"),
    path("trash/", webviews.trash, name="sptrash"),
    path("delete/<int:acc_id>/", webviews.delete, name="spdelete"),
    path("api/accounts/search/", views.search_account),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]
