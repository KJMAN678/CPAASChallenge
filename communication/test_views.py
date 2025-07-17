from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock


class SMSViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('communication:sms')

    def test_get_sms_form(self):
        """SMS フォームページの GET リクエストテスト"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SMS送信')
        self.assertContains(response, 'phone_number')
        self.assertContains(response, 'message')

    @patch('communication.views.SmsApi')
    @patch('communication.views.ApiClient')
    @patch('communication.views.Configuration')
    def test_valid_sms_submission(self, mock_config, mock_client, mock_sms_api):
        """有効なSMS送信のテスト"""
        mock_response = MagicMock()
        mock_response.messages = [MagicMock()]
        mock_response.messages[0].status.group_name = "PENDING"
        
        mock_api_instance = MagicMock()
        mock_api_instance.send_sms_message.return_value = mock_response
        mock_sms_api.return_value = mock_api_instance

        form_data = {
            'phone_number': '+81901234567',
            'message': 'テストメッセージです'
        }
        
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertRedirects(response, reverse('communication:sms_success'))

    def test_invalid_sms_submission(self):
        """無効なSMS送信のテスト"""
        form_data = {
            'phone_number': 'invalid_number',
            'message': 'テストメッセージです'
        }
        
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)  # フォームエラーで同じページ
        self.assertContains(response, 'error')


class VoiceCallViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('communication:voice')

    def test_get_voice_form(self):
        """音声通話フォームページの GET リクエストテスト"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '音声通話')
        self.assertContains(response, 'phone_number')
        self.assertContains(response, 'message')
        self.assertContains(response, 'voice_type')

    @patch('communication.views.CallsApi')
    @patch('communication.views.ApiClient')
    @patch('communication.views.Configuration')
    @patch('communication.views.PollyService')
    def test_valid_voice_call_submission(self, mock_polly, mock_config, mock_client, mock_calls_api):
        """有効な音声通話のテスト"""
        mock_polly_instance = MagicMock()
        mock_polly_instance.synthesize_speech.return_value = b'fake_audio_data'
        mock_polly_instance.save_audio_file.return_value = '/tmp/fake_audio.mp3'
        mock_polly.return_value = mock_polly_instance

        mock_call_response = MagicMock()
        mock_call_response.call_id = 'test_call_id'
        
        mock_say_response = MagicMock()
        
        mock_api_instance = MagicMock()
        mock_api_instance.create_call.return_value = mock_call_response
        mock_api_instance.say_text.return_value = mock_say_response
        mock_calls_api.return_value = mock_api_instance

        form_data = {
            'phone_number': '+81901234567',
            'message': 'こんにちは、テストメッセージです。',
            'voice_type': 'Mizuki'
        }
        
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertRedirects(response, reverse('communication:voice_success'))

        mock_polly_instance.synthesize_speech.assert_called_once_with(
            'こんにちは、テストメッセージです。', 'Mizuki'
        )
        mock_polly_instance.save_audio_file.assert_called_once()
        mock_polly_instance.cleanup_audio_file.assert_called_once()

    def test_invalid_voice_call_submission(self):
        """無効な音声通話のテスト"""
        form_data = {
            'phone_number': 'invalid_number',
            'message': 'テストメッセージです',
            'voice_type': 'Mizuki'
        }
        
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)  # フォームエラーで同じページ
        self.assertContains(response, 'error')


class SuccessPageTest(TestCase):
    def test_sms_success_page(self):
        """SMS成功ページのテスト"""
        url = reverse('communication:sms_success')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '送信完了')

    def test_voice_success_page(self):
        """音声通話成功ページのテスト"""
        url = reverse('communication:voice_success')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '送信完了')
