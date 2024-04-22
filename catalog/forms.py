from django import forms

from catalog.models import Product, Version


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = ('name', 'description', 'image_preview', 'category', 'price_per_unit')

    def clean_name(self):
        bad_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        cleaned_data = self.cleaned_data.get('name')

        if cleaned_data:
            for word in bad_words:
                if word in cleaned_data.lower():
                    raise forms.ValidationError('Ваш текст содержит неприемлемые слова.')

        return cleaned_data

    def clean_description(self):
        description = self.cleaned_data.get('description')
        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                           'радар']
        for word in forbidden_words:
            if word in description.lower():
                raise forms.ValidationError('Ваш текст содержит неприемлемые слова.')

        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_number',
                  'version_name',
                  'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].widget.attrs['class'] = 'form-check-input'
