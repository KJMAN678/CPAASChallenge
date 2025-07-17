from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
import logging

from infobip_api_client.api_client import ApiClient, Configuration
from infobip_api_client.api import SmsApi, CallsApi
from infobip_api_client.models import (
    SmsRequest, SmsDestination, SmsTextContent,
    CallRequest, CallsPhoneEndpoint, CallEndpointType, CallsSayRequest
)

from .forms import SMSForm, VoiceCallForm
from .services import PollyService

logger = logging.getLogger(__name__)


class SMSView(FormView):
    template_name = 'communication/sms_form.html'
    form_class = SMSForm
    success_url = reverse_lazy('communication:sms_success')
    
    def form_valid(self, form):
        try:
            client_config = Configuration(
                host=settings.INFOBIP_BASE_URL,
                api_key={"APIKeyHeader": settings.INFOBIP_API_KEY},
                api_key_prefix={"APIKeyHeader": settings.INFOBIP_API_PREFIX},
            )
            
            api_client = ApiClient(client_config)
            sms_api = SmsApi(api_client)
            
            destination = SmsDestination(to=form.cleaned_data['phone_number'])
            content = SmsTextContent(text=form.cleaned_data['message'])
            
            request = SmsRequest(
                destinations=[destination],
                content=content,
                var_from=settings.INFOBIP_FROM_NUMBER
            )
            
            response = sms_api.send_sms_message(sms_request=request)
            
            if response.messages and response.messages[0].status.group_name == "PENDING":
                messages.success(self.request, 'SMSが正常に送信されました。')
                logger.info(f"SMS sent successfully to {form.cleaned_data['phone_number']}")
            else:
                error_msg = response.messages[0].status.description if response.messages else "不明なエラー"
                messages.error(self.request, f'SMS送信に失敗しました: {error_msg}')
                logger.error(f"SMS sending failed: {error_msg}")
                
        except Exception as e:
            messages.error(self.request, f'SMS送信中にエラーが発生しました: {str(e)}')
            logger.error(f"SMS sending error: {str(e)}")
            
        return super().form_valid(form)


class VoiceCallView(FormView):
    template_name = 'communication/voice_form.html'
    form_class = VoiceCallForm
    success_url = reverse_lazy('communication:voice_success')
    
    def form_valid(self, form):
        polly_service = PollyService()
        audio_file_path = None
        
        try:
            audio_data = polly_service.synthesize_speech(
                form.cleaned_data['message'],
                form.cleaned_data['voice_type']
            )
            
            audio_file_path = polly_service.save_audio_file(audio_data)
            
            client_config = Configuration(
                host=settings.INFOBIP_BASE_URL,
                api_key={"APIKeyHeader": settings.INFOBIP_API_KEY},
                api_key_prefix={"APIKeyHeader": settings.INFOBIP_API_PREFIX},
            )
            
            api_client = ApiClient(client_config)
            calls_api = CallsApi(api_client)
            
            call_request = CallRequest(
                endpoint=CallsPhoneEndpoint(
                    phone_number=form.cleaned_data['phone_number'],
                    type=CallEndpointType.PHONE
                ),
                var_from=settings.INFOBIP_FROM_NUMBER,
                calls_configuration_id="ORION",
            )
            
            call_response = calls_api.create_call(call_request=call_request)
            
            if call_response and call_response.call_id:
                say_request = CallsSayRequest(
                    text=form.cleaned_data['message'],
                    language="ja"
                )
                
                say_response = calls_api.say_text(
                    call_id=call_response.call_id,
                    calls_say_request=say_request
                )
                
                if say_response:
                    messages.success(self.request, '音声通話が正常に開始されました。')
                    logger.info(f"Voice call started successfully to {form.cleaned_data['phone_number']}")
                else:
                    messages.error(self.request, '音声メッセージの再生に失敗しました。')
                    logger.error("Voice message playback failed")
            else:
                messages.error(self.request, '音声通話の開始に失敗しました。')
                logger.error("Voice call initiation failed")
                
        except Exception as e:
            messages.error(self.request, f'音声通話中にエラーが発生しました: {str(e)}')
            logger.error(f"Voice call error: {str(e)}")
        finally:
            if audio_file_path:
                polly_service.cleanup_audio_file(audio_file_path)
            
        return super().form_valid(form)
