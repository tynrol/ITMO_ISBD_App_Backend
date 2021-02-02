from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from .serializers import *
from .models import *

class SortedSuitabilityView(viewsets.ModelViewSet):
    serializer_class = SuitabilitySerializer
    queryset = Suitability.objects.all().order_by('days_to_couple')

class TransformView(viewsets.ModelViewSet):
    serializer_class = LodgerSerializer
    queryset = Lodger.objects.all().filter(days_left=0)

class LodgerView(viewsets.ModelViewSet):
    serializer_class = LodgerSerializer
    queryset = Lodger.objects.all()

    @action(methods=['get'], detail=False, url_path='update_day', url_name='update_day')
    def update_day(self, request):
        self.queryset = self.queryset.exclude(days_left=-1)
        self.queryset.update(days_left=F('days_left') - 1)
        return Response()

class SearchView(viewsets.ModelViewSet):
    serializer_class = SearchSerializer
    queryset = Lodger.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class SuitabilityView(viewsets.ModelViewSet):
    serializer_class = SuitabilitySerializer
    queryset = Suitability.objects.all()

    @action(methods=['get'], detail=False, url_path='get', url_name='get')
    def get_object(self, request):
        _man_id = request.GET.get('man_id')
        _woman_id = request.GET.get('woman_id')
        _queryset = Suitability.objects.all().filter(man_id=_man_id, woman_id=_woman_id)
        serializer = self.get_serializer(_queryset, many=True)
        if _queryset.count() == 0:
            return Response(status=404)
        return Response(serializer.data)

class ScheduleView(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

class EscapeAttemptView(viewsets.ModelViewSet):
    serializer_class = EscapeAttemptSerializer
    queryset = EscapeAttempt.objects.all()
    #schedule = Schedule.objects.all()

class CouplesView(viewsets.ModelViewSet):
    serializer_class = CouplesSerializer
    queryset = Couples.objects.all()


    @action(methods=['get'], detail=False, url_path='set', url_name='set')
    def set_couple(self, request):
        _man_id = request.GET.get('man_id')
        _woman_id = request.GET.get('woman_id')
        try:
            _check = self.queryset.get(man_id=_man_id)
            _check = self.queryset.get(woman_id=_woman_id)
        except BaseException:
            self.queryset.create(man_id=_man_id,woman_id=_woman_id)
            return Response()
        return Response(status=400)



