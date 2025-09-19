from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser

from .filters import RideFilterSet
from .models import Ride, Ride_Event, User
from .serializers import Ride_EventSerializer, RideSerializer, UserSerializer


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all().select_related("id_rider", "id_driver")
    serializer_class = RideSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RideFilterSet
    ordering_fields = ['pickup_time']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Ride_EventViewSet(viewsets.ModelViewSet):
    queryset = Ride_Event.objects.all()
    serializer_class = Ride_EventSerializer


class HomePageView(TemplateView):
    template_name = "home.html"
