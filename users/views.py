import stripe
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, generics
from rest_framework.generics import CreateAPIView
from django_filters import rest_framework as filters
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from materials.models import Course, Lesson
from .models import Payments, User
from .serializers import PaymentsSerializer, UserSerializer
from .services import create_stripe_price, create_stripe_sessions, create_stripe_product


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


class PaymentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # Создание продукта и цены в Stripe
        product_name = f"{payment.course.name} Course"
        product = create_stripe_product(product_name)
        price = create_stripe_price(payment.amount, product)

        # Создание сессии для оплаты
        session_id, payment_link = create_stripe_sessions(price)

        # Сохранение данных в модель Payments
        payment.stripe_session_id = session_id
        payment.link = payment_link
        payment.save()

        # Возвращаем ссылку на оплату
        course = payment.course
        return HttpResponse(
            f"Payment URL: {payment_link}",
            content_type="text/plain",
        )


class PaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer


class PaymentStatusAPIView(APIView):
    """Эндпоинт для получения статуса платежа по ID сессии Stripe"""

    def get(self, request, session_id):
        session = stripe.checkout.Session.retrieve(session_id)
        payment_status = session.get('payment_status', 'unknown')

        return JsonResponse({
            'session_id': session.id,
            'payment_status': payment_status
        })
