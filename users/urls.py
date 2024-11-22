from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from users.apps import UsersConfig
from users.views import PaymentsViewSet, PaymentsFilter
app_name = UsersConfig.name

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [

] + router.urls
