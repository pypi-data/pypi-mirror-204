from django.urls import path
from huscy.project_consents import views

urlpatterns = [
    path(
        '<int:project_id>/consents/',
        views.CreateProjectConsentView.as_view(),
        name="create-project-consent"
    ),
    path('create/token/', views.CreateTokenView.as_view(), name='create-project-consent-token'),
    path('sign/<uuid:token>/', views.SignProjectConsentView.as_view(), name="sign-project-consent"),
]
