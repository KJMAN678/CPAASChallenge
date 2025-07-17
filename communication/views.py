from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
import logging

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse

from .forms import SMSForm, VoiceCallForm

logger = logging.getLogger(__name__)


class SMSView(FormView):
    template_name = 'communication/sms_form.html'
    form_class = SMSForm
    success_url = reverse_lazy('communication:sms_success')
    
    def form_valid(self, form):
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                body=form.cleaned_data['message'],
                from_=settings.TWILIO_FROM_NUMBER,
                to=form.cleaned_data['phone_number']
            )
            
            if message.sid:
                messages.success(self.request, 'SMSが正常に送信されました。')
                logger.info(f"SMS sent successfully to {form.cleaned_data['phone_number']}, SID: {message.sid}")
            else:
                messages.error(self.request, 'SMS送信に失敗しました。')
                logger.error("SMS sending failed: No SID returned")
                
        except Exception as e:
            messages.error(self.request, f'SMS送信中にエラーが発生しました: {str(e)}')
            logger.error(f"SMS sending error: {str(e)}")
            
        return super().form_valid(form)


class VoiceCallView(FormView):
    template_name = 'communication/voice_form.html'
    form_class = VoiceCallForm
    success_url = reverse_lazy('communication:voice_success')
    
    def form_valid(self, form):
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            twiml = VoiceResponse()
            twiml.say(
                form.cleaned_data['message'],
                voice='Polly.Mizuki-Neural' if form.cleaned_data['voice_type'] == 'Mizuki' else 'Polly.Takumi-Neural',
                language='ja-JP'
            )
            
            call = client.calls.create(
                twiml=str(twiml),
                to=form.cleaned_data['phone_number'],
                from_=settings.TWILIO_FROM_NUMBER
            )
            
            if call.sid:
                messages.success(self.request, '音声通話が正常に開始されました。')
                logger.info(f"Voice call started successfully to {form.cleaned_data['phone_number']}, SID: {call.sid}")
            else:
                messages.error(self.request, '音声通話の開始に失敗しました。')
                logger.error("Voice call initiation failed: No SID returned")
                
        except Exception as e:
            messages.error(self.request, f'音声通話中にエラーが発生しました: {str(e)}')
            logger.error(f"Voice call error: {str(e)}")
            
        return super().form_valid(form)
