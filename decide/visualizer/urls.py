from django.urls import path
from .views import VisualizerView, VisualizerPdf, VisualizerCsv


urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('<int:voting_id>/pdf/', VisualizerPdf.as_view()),
    path('<int:voting_id>/csv/', VisualizerCsv.as_view()),
]
