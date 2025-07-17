import boto3
import tempfile
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class PollyService:
    def __init__(self):
        self.polly_client = boto3.client(
            'polly',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
    
    def synthesize_speech(self, text, voice_id='Mizuki'):
        """テキストを音声ファイルに変換"""
        try:
            response = self.polly_client.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=voice_id,
                LanguageCode='ja-JP'
            )
            return response['AudioStream'].read()
        except Exception as e:
            logger.error(f"AWS Polly synthesis error: {str(e)}")
            raise
    
    def save_audio_file(self, audio_data):
        """音声データを一時ファイルに保存してパスを返す"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.write(audio_data)
            temp_file.close()
            return temp_file.name
        except Exception as e:
            logger.error(f"Audio file save error: {str(e)}")
            raise
    
    def cleanup_audio_file(self, file_path):
        """一時音声ファイルを削除"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
                logger.info(f"Cleaned up audio file: {file_path}")
        except Exception as e:
            logger.error(f"Audio file cleanup error: {str(e)}")
