# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status
from rest_framework_filters import backends
from rest_framework.decorators import list_route
from rest_framework.response import Response

from migasfree.server.permissions import PublicPermission
from migasfree.server.models import Computer
from . import models, serializers
from .filters import ApplicationFilter, PackagesByProjectFilter, PolicyFilter


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
    filter_class = ApplicationFilter
    filter_backends = (filters.OrderingFilter, backends.DjangoFilterBackend)
    permission_classes = (PublicPermission,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' \
                or self.action == 'partial_update':
            return serializers.ApplicationWriteSerializer

        return serializers.ApplicationSerializer

    @list_route(methods=['get'])
    def levels(self, request):
        return Response(
            dict(models.Application.LEVELS),
            status=status.HTTP_200_OK
        )

    @list_route(methods=['get'])
    def categories(self, request):
        return Response(
            dict(models.Application.CATEGORIES),
            status=status.HTTP_200_OK
        )

    @list_route(methods=['get'])
    def availables(self, request):
        """
        :param request:
            cid (computer Id) int,
            category int,
            level int,
            q string (name or description contains...),
            page int
        :return: ApplicationSerializer set
        """
        computer = get_object_or_404(Computer, pk=request.GET.get('cid', 0))
        category = request.GET.get('category', 0)
        level = request.GET.get('level', '')
        query = request.GET.get('q', '')

        results = models.Application.objects.filter(
            available_for_attributes__in=computer.sync_attributes.values_list('id', flat=True),
            packages_by_project__project=computer.project
        ).order_by('-score', 'name')
        if category:
            results = results.filter(category=category)
        if level:
            results = results.filter(level=level)
        if query:
            results = results.filter(Q(name__icontains=query) | Q(description__icontains=query))

        page = self.paginate_queryset(results)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PackagesByProjectViewSet(viewsets.ModelViewSet):
    queryset = models.PackagesByProject.objects.all()
    serializer_class = serializers.PackagesByProjectSerializer
    filter_class = PackagesByProjectFilter
    filter_backends = (filters.OrderingFilter, backends.DjangoFilterBackend)
    permission_classes = (PublicPermission,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' \
                or self.action == 'partial_update':
            return serializers.PackagesByProjectWriteSerializer

        return serializers.PackagesByProjectSerializer


class PolicyViewSet(viewsets.ModelViewSet):
    queryset = models.Policy.objects.all()
    serializer_class = serializers.PolicySerializer
    filter_class = PolicyFilter
    filter_backends = (filters.OrderingFilter, backends.DjangoFilterBackend)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' \
                or self.action == 'partial_update':
            return serializers.PolicyWriteSerializer

        return serializers.PolicySerializer


class PolicyGroupViewSet(viewsets.ModelViewSet):
    queryset = models.PolicyGroup.objects.all()
    serializer_class = serializers.PolicyGroupSerializer
    filter_backends = (filters.OrderingFilter, backends.DjangoFilterBackend)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' \
                or self.action == 'partial_update':
            return serializers.PolicyGroupWriteSerializer

        return serializers.PolicyGroupSerializer
