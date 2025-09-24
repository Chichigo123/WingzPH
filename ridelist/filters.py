from django.core.exceptions import FieldError
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

from .models import Ride


class RideFilterSet(filters.FilterSet):

    class Meta:
        model = Ride
        fields = ["status", "id_rider__email"]


class CustomOrderingFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            try:
                queryset = queryset.order_by(*ordering)
            except FieldError:
                if "distance_to_pickup" or "-distance_to_pickup" in ordering:
                    raise FieldError(
                        "Ordering by distance_to_pickup requires longitude and latitude as input in the API."
                    )
        return queryset
