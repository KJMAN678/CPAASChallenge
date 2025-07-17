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

    @patch('communication.views.Client')
    def test_valid_sms_submission(self, mock_client):
        """有効なSMS送信のテスト"""
        mock_message = MagicMock()
        mock_message.sid = 'test_sms_sid'
        
        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.return_value = mock_message
        mock_client.return_value = mock_client_instance

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

    @patch('communication.views.VoiceResponse')
    @patch('communication.views.Client')
    def test_valid_voice_call_submission(self, mock_client, mock_voice_response):
        """有効な音声通話のテスト"""
        mock_twiml = MagicMock()
        mock_voice_response.return_value = mock_twiml
        
        mock_call = MagicMock()
        mock_call.sid = 'test_call_sid'
        
        mock_client_instance = MagicMock()
        mock_client_instance.calls.create.return_value = mock_call
        mock_client.return_value = mock_client_instance

        form_data = {
            'phone_number': '+81901234567',
            'message': 'こんにちは、テストメッセージです。',
            'voice_type': 'Mizuki'
        }
        
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 302)  # リダイレクト
        self.assertRedirects(response, reverse('communication:voice_success'))

        mock_twiml.say.assert_called_once_with(
            'こんにちは、テストメッセージです。',
            voice='Polly.Mizuki-Neural',
            language='ja-JP'
        )
        mock_client_instance.calls.create.assert_called_once()

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
