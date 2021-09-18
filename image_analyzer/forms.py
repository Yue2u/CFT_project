from django import forms
from django.core.validators import RegexValidator


class ImageForm(forms.Form):
    document = forms.ImageField(required=False, label='Прикрепите изображение')
    hex_color = forms.CharField(max_length=7, required=False,
                                validators=[RegexValidator(r'#[a-zA-z0-9]{3,6}', 'Enter valid HEX color')],
                                label='Введите цвет в формате HEX')
