from django.urls import path

from . import views


urlpatterns = (
    # Network Diagram
    path('network-diagram/', views.NetworkDiagramView.as_view(), name='network_diagram'),
)
