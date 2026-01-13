from django.urls import path
from app.views.auth import LoginView
from app.views.evidence import (
    EvidenceCreateView, 
    EvidenceVersionCreateView
)
from app.views.requests import (
    RequestCreateView, 
    FactoryRequestListView,
    BuyerRequestListView,
    FulfillItemView
) 
from app.views.audit import AuditListView



urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('evidence/', EvidenceCreateView.as_view(), name='create_evidence'),
    path('evidence/<int:evidence_id>/versions/', 
         EvidenceVersionCreateView.as_view(), 
         name='create_evidence_version'),
    path('requests/', RequestCreateView.as_view(), name='create_request'),
    path('requests/factory/', FactoryRequestListView.as_view(), name='factory_requests'),
    path('requests/buyer/', BuyerRequestListView.as_view(), name='buyer_requests'),
    path('requests/<int:request_id>/items/<int:item_id>/fulfill/', 
         FulfillItemView.as_view(), 
         name='fulfill_item'),
    path('audit/logs/', AuditListView.as_view(), name='audit_logs'),
]

