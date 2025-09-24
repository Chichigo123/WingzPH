from datetime import timedelta

from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Func, Prefetch
from django.utils import timezone
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication

from .authentication import CustomHeaderAuthentication
from .filters import CustomOrderingFilter, RideFilterSet
from .models import Ride, Ride_Event, User
from .permissions import UserAdmin
from .serializers import Ride_EventSerializer, RideSerializer, UserSerializer


class MakePostGisPoint(Func):
    """
    Creates a PostGis Point using Ride.pickup_longitude and Ride.pickup_latitude
    """

    function = "ST_SetSRID"
    template = "%(function)s(ST_MakePoint(%(expressions)s), 4326)"
    output_field = PointField()


class RideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ride.objects.all().select_related("id_rider", "id_driver")
    serializer_class = RideSerializer
    authentication_classes = [CustomHeaderAuthentication, SessionAuthentication]
    permission_classes = (UserAdmin,)
    filter_backends = [DjangoFilterBackend, CustomOrderingFilter]
    filterset_class = RideFilterSet
    ordering_fields = ["pickup_time", "distance_to_pickup"]

    def get_queryset(self):
        """
        Support ordering by pickup_time and distance_to_pickup given a GPS position as input in the same API
        """
        queryset = self.queryset.annotate(
            point=MakePostGisPoint("pickup_longitude", "pickup_latitude")
        ).order_by("-pickup_time")

        longitude = self.request.query_params.get("longitude", None)
        latitude = self.request.query_params.get("latitude", None)

        if longitude is not None and latitude is not None:
            # The default spatial reference system for geometry fields is WGS84 (meaning the SRID is 4326)
            # in other words, the field coordinates are in longitude, latitude
            reference_point = Point(float(longitude), float(latitude), srid=4326)
            queryset = queryset.annotate(
                distance_to_pickup=Distance("point", reference_point)
            )

        # prefetch todays_ride_events (Ride_Events in the last 24 hours)
        # Use prefetch_related (reverse relationship) + Prefetch (granular control to filter Ride_Events)

        prefetch_ride_events = Prefetch(
            "ride_events",
            queryset=Ride_Event.objects.filter(
                created_at__gte=timezone.now() - timedelta(days=1)
            ),
            to_attr="todays_ride_events",
        )

        queryset = queryset.prefetch_related(prefetch_ride_events)

        return queryset


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Ride_EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ride_Event.objects.all()
    serializer_class = Ride_EventSerializer


class HomePageView(TemplateView):
    template_name = "home.html"
