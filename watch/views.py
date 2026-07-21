"""Views for the watch app (thin — logic lives in models and services)."""

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from watch.forms import TargetForm
from watch.models import Observation, Target


class HomeView(TemplateView):
    """Dashboard landing page."""

    template_name = "watch/home.html"


class TargetListView(ListView[Target]):
    """List active targets."""

    queryset = Target.objects.filter(active=True)
    context_object_name = "targets"


class TargetCreateView(SuccessMessageMixin[TargetForm], CreateView[Target, TargetForm]):
    """Create a new watch target."""

    model = Target
    form_class = TargetForm
    success_url = reverse_lazy("watch:target-list")
    success_message = 'Target "%(name)s" created.'


class ObservationListView(ListView[Observation]):
    """List recent observations (newest first)."""

    queryset = Observation.objects.select_related("run", "target")
    context_object_name = "observations"
    paginate_by = 20
