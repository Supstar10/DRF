from rest_framework import viewsets
from django_filters import rest_framework as filters

from materials.models import Course, Lesson
from .models import Payments
from .serializers import PaymentsSerializer


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
