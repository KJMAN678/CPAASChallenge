from django.test import TestCase
from unittest.mock import patch, MagicMock
import tempfile
import os
from .services import PollyService


class PollyServiceTest(TestCase):
    def setUp(self):
        self.polly_service = PollyService()

    @patch('boto3.client')
    def test_synthesize_speech_success(self, mock_boto_client):
        """AWS Polly音声合成成功のテスト"""
        mock_polly = MagicMock()
        mock_response = {
            'AudioStream': MagicMock()
        }
        mock_response['AudioStream'].read.return_value = b'fake_audio_data'
        mock_polly.synthesize_speech.return_value = mock_response
        mock_boto_client.return_value = mock_polly

        service = PollyService()
        result = service.synthesize_speech('こんにちは', 'Mizuki')

        self.assertEqual(result, b'fake_audio_data')
        mock_polly.synthesize_speech.assert_called_once_with(
            Text='こんにちは',
            OutputFormat='mp3',
            VoiceId='Mizuki',
            LanguageCode='ja-JP'
        )

    @patch('boto3.client')
    def test_synthesize_speech_with_takumi_voice(self, mock_boto_client):
        """Takumi音声での音声合成テスト"""
        mock_polly = MagicMock()
        mock_response = {
            'AudioStream': MagicMock()
        }
        mock_response['AudioStream'].read.return_value = b'fake_audio_data'
        mock_polly.synthesize_speech.return_value = mock_response
        mock_boto_client.return_value = mock_polly

        service = PollyService()
        result = service.synthesize_speech('こんにちは', 'Takumi')

        self.assertEqual(result, b'fake_audio_data')
        mock_polly.synthesize_speech.assert_called_once_with(
            Text='こんにちは',
            OutputFormat='mp3',
            VoiceId='Takumi',
            LanguageCode='ja-JP'
        )

    def test_save_audio_file(self):
        """音声ファイル保存のテスト"""
        test_data = b'fake_audio_data'
        file_path = self.polly_service.save_audio_file(test_data)

        self.assertTrue(os.path.exists(file_path))
        self.assertTrue(file_path.endswith('.mp3'))

        with open(file_path, 'rb') as f:
            saved_data = f.read()
        self.assertEqual(saved_data, test_data)

        os.unlink(file_path)

    def test_cleanup_audio_file(self):
        """音声ファイルクリーンアップのテスト"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.write(b'test_data')
        temp_file.close()

        self.assertTrue(os.path.exists(temp_file.name))

        self.polly_service.cleanup_audio_file(temp_file.name)

        self.assertFalse(os.path.exists(temp_file.name))

    def test_cleanup_nonexistent_file(self):
        """存在しないファイルのクリーンアップテスト"""
        try:
            self.polly_service.cleanup_audio_file('/nonexistent/path/file.mp3')
        except Exception as e:
            self.fail(f"cleanup_audio_file raised an exception: {e}")

    @patch('boto3.client')
    def test_synthesize_speech_error(self, mock_boto_client):
        """AWS Polly音声合成エラーのテスト"""
        mock_polly = MagicMock()
        mock_polly.synthesize_speech.side_effect = Exception('AWS Error')
        mock_boto_client.return_value = mock_polly

        service = PollyService()
        
        with self.assertRaises(Exception) as context:
            service.synthesize_speech('テスト', 'Mizuki')
        
        self.assertEqual(str(context.exception), 'AWS Error')
