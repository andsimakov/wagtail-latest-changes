from django.shortcuts import render
from wagtail.admin.views.reports import PageReportView
from wagtail.admin.auth import permission_denied
from wagtail.core.models import UserPagePermissionsProxy
from wagtail.core.models import Page


class LatestChangesView(PageReportView):
    template_name = "reports/latest_changes.html"
    title = "Latest changes"
    header_icon = "date"

    def get_queryset(self):
        self.queryset = Page.objects.exclude(last_published_at__isnull=True).order_by("-last_published_at")
        return super().get_queryset()

    def dispatch(self, request, *args, **kwargs):
        if not UserPagePermissionsProxy(request.user).can_remove_locks():
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)
