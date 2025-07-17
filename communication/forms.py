from django import forms


class SMSForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        label="送信先電話番号",
        widget=forms.TextInput(attrs={
            'placeholder': '+81901234567',
            'class': 'form-control'
        }),
        help_text="国際形式で入力してください（例: +81901234567）"
    )
    message = forms.CharField(
        max_length=160,
        label="メッセージ内容",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'SMSで送信するメッセージを入力してください'
        }),
        help_text="最大160文字まで入力できます"
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith('+'):
            raise forms.ValidationError("電話番号は+から始まる国際形式で入力してください")
        if not phone_number[1:].isdigit():
            raise forms.ValidationError("電話番号は数字のみで入力してください")
        return phone_number


class VoiceCallForm(forms.Form):
    VOICE_CHOICES = [
        ('Mizuki', '日本語女性（Mizuki）'),
        ('Takumi', '日本語男性（Takumi）'),
    ]

    phone_number = forms.CharField(
        max_length=15,
        label="通話先電話番号",
        widget=forms.TextInput(attrs={
            'placeholder': '+81901234567',
            'class': 'form-control'
        }),
        help_text="国際形式で入力してください（例: +81901234567）"
    )
    message = forms.CharField(
        max_length=500,
        label="音声メッセージ内容",
        widget=forms.Textarea(attrs={
            'rows': 6,
            'class': 'form-control',
            'placeholder': '音声で読み上げるメッセージを入力してください'
        }),
        help_text="最大500文字まで入力できます"
    )
    voice_type = forms.ChoiceField(
        choices=VOICE_CHOICES,
        label="音声タイプ",
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='Mizuki'
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith('+'):
            raise forms.ValidationError("電話番号は+から始まる国際形式で入力してください")
        if not phone_number[1:].isdigit():
            raise forms.ValidationError("電話番号は数字のみで入力してください")
        return phone_number
