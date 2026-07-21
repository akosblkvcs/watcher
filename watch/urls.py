from django.urls import path

from watch import views

app_name = "watch"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("targets/", views.TargetListView.as_view(), name="target-list"),
    # path("targets/new/", views.TargetCreateView.as_view(), name="target-create"),
    path("observations/", views.ObservationListView.as_view(), name="observation-list"),
]
