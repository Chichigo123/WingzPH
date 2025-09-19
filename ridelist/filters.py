from django_filters import rest_framework as filters

from .models import Ride


class RideFilterSet(filters.FilterSet):
    rider_email = filters.CharFilter(
        field_name="id_rider__email", lookup_expr="contains"
    )

    class Meta:
        model = Ride
        fields = ["status"]  # 'id_rider_email' is handled by 'rider_email'
