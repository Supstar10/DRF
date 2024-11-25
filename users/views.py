from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny

from materials.models import Course, Lesson
from .models import Payments, User
from .serializers import PaymentsSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class PaymentsFilter(filters.FilterSet):
    course = filters.ModelChoiceFilter(queryset=Course.objects.all())
    lesson = filters.ModelChoiceFilter(queryset=Lesson.objects.all())
    payment_method = filters.ChoiceFilter(choices=Payments.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payments
        fields = ['payment_date', 'course', 'lesson', 'payment_method']


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentsFilter
