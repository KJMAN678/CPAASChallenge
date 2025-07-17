from django.test import TestCase
from .forms import SMSForm, VoiceCallForm


class SMSFormTest(TestCase):
    def test_valid_form(self):
        """有効なSMSフォームデータのテスト"""
        form_data = {
            'phone_number': '+81901234567',
            'message': 'テストメッセージです'
        }
        form = SMSForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number_without_plus(self):
        """+記号なしの電話番号のテスト"""
        form_data = {
            'phone_number': '81901234567',
            'message': 'テストメッセージです'
        }
        form = SMSForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_invalid_phone_number_with_letters(self):
        """文字が含まれた電話番号のテスト"""
        form_data = {
            'phone_number': '+81abc1234567',
            'message': 'テストメッセージです'
        }
        form = SMSForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_empty_message(self):
        """空のメッセージのテスト"""
        form_data = {
            'phone_number': '+81901234567',
            'message': ''
        }
        form = SMSForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_message_too_long(self):
        """長すぎるメッセージのテスト"""
        form_data = {
            'phone_number': '+81901234567',
            'message': 'a' * 161  # 161文字
        }
        form = SMSForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)


class VoiceCallFormTest(TestCase):
    def test_valid_form(self):
        """有効な音声通話フォームデータのテスト"""
        form_data = {
            'phone_number': '+81901234567',
            'message': 'こんにちは、これはテストメッセージです。',
            'voice_type': 'Mizuki'
        }
        form = VoiceCallForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_with_takumi_voice(self):
        """Takumi音声タイプでの有効なフォームテスト"""
        form_data = {
            'phone_number': '+81901234567',
            'message': 'こんにちは、これはテストメッセージです。',
            'voice_type': 'Takumi'
        }
        form = VoiceCallForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number(self):
        """無効な電話番号のテスト"""
        form_data = {
            'phone_number': '901234567',
            'message': 'テストメッセージです',
            'voice_type': 'Mizuki'
        }
        form = VoiceCallForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_message_too_long(self):
        """長すぎるメッセージのテスト"""
        form_data = {
            'phone_number': '+81901234567',
            'message': 'a' * 501,  # 501文字
            'voice_type': 'Mizuki'
        }
        form = VoiceCallForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)

    def test_invalid_voice_type(self):
        """無効な音声タイプのテスト"""
        form_data = {
            'phone_number': '+81901234567',
            'message': 'テストメッセージです',
            'voice_type': 'InvalidVoice'
        }
        form = VoiceCallForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('voice_type', form.errors)
