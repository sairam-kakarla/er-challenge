# claims/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # This maps the homepage ('') to our claims_list view
    path('', views.claims_list, name='claims-list'),
    path('dashboard', views.admin_dashboard, name='dashboard'),
    path('claim/<int:claim_id>/detail', views.claim_detail, name='claim-detail'),
    path('claim/<int:claim_id>/flag', views.flag_claim, name='flag-claim'),
    path('claim/<int:claim_id>/add-note', views.add_note, name='add-note'),
      
]