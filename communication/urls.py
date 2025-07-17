from django.urls import path
from django.views.generic import TemplateView
from .views import SMSView, VoiceCallView

app_name = 'communication'

urlpatterns = [
    path('sms/', SMSView.as_view(), name='sms'),
    path('voice/', VoiceCallView.as_view(), name='voice'),
    path('sms/success/', TemplateView.as_view(template_name='communication/success.html'), name='sms_success'),
    path('voice/success/', TemplateView.as_view(template_name='communication/success.html'), name='voice_success'),
]
