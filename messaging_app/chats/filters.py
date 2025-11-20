import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # filter messages exchanged with a specific user
    user = django_filters.NumberFilter(field_name="sender__id")  
    
    # filter by time range
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["user", "start_date", "end_date"]
