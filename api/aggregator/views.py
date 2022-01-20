import datetime
from collections import defaultdict

from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from aggregator.models import Event
from aggregator.serializers import EventSerializer


class EventView(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(opportunity_list_id=self.request.resolver_match.kwargs['opportunity_list_id'])


class CounterView(APIView):
    http_method_names = ['post']

    def post(self, request):
        timestamp = request.data.get('timestamp', None)
        date = None

        if timestamp is None:  # validator
            return Response({"message": "expected timestamp"}, status=status.HTTP_417_EXPECTATION_FAILED)

        try:
            date = datetime.datetime.fromtimestamp(timestamp / 1e3)
        except Exception as e:
            return Response({"message": e}, status=status.HTTP_417_EXPECTATION_FAILED)

        del request.data['timestamp']

        events = list()

        for key in request.data:

            if not isinstance(request.data[key], int):  # validator
                return Response({"message": "integer is expected"}, status=status.HTTP_417_EXPECTATION_FAILED)

            events.append(Event(domain=key, requests_number=request.data[key], timestamp=date))

        events_obj = Event.objects.bulk_create(events)

        response_data = EventSerializer(events_obj, many=True)

        return Response(response_data.data, status=status.HTTP_200_OK)


class StatisticsView(APIView):
    http_method_names = ['get']

    def get(self, request):
        now = timezone.now().replace(microsecond=0)

        upper_limit_minute = now - datetime.timedelta(seconds=now.second)
        lower_limit_minute = upper_limit_minute - datetime.timedelta(minutes=1)

        upper_limit_hour = now - datetime.timedelta(seconds=now.second, minutes=now.minute)
        lower_limit_hour = upper_limit_hour - datetime.timedelta(hours=1)

        events_minute = Event.objects.filter(timestamp__gte=lower_limit_minute, timestamp__lte=upper_limit_minute)
        events_hour = Event.objects.filter(timestamp__gte=lower_limit_hour, timestamp__lte=upper_limit_hour)

        counter_minute = defaultdict(int)
        counter_hour = defaultdict(int)

        for event in events_minute:
            counter_minute[event.domain] += event.requests_number

        for event in events_hour:
            counter_hour[event.domain] += 1

        top_ten_minute = list(sorted(counter_minute.items(), key=lambda item: item[1]))[:10]
        top_ten_hour = list(sorted(counter_hour.items(), key=lambda item: item[1]))[:10]

        return Response(
            {
                "last_minute": dict(top_ten_minute),
                "last_hour": dict(top_ten_hour)
            },
            status=status.HTTP_200_OK
        )

