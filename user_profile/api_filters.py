from rest_framework import filters


class IsOwnerFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user.id)

class IsWorkerFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user__worker=request.user)