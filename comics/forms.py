from django import forms

from .models import Comic, Genre, Chapter, ChapterImage


class ComicForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, help_text='Enter Comic Title', widget=forms.TextInput())
    summary = forms.CharField(required=True, help_text='Enter Comic Description', widget=forms.Textarea())
    cover = forms.ImageField(required=True, help_text='Upload Comic Cover')
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(), required=True, help_text='Select Genres',
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}
        )
    )

    class Meta:
        model = Comic
        fields = ['title', 'summary', 'cover', 'genres']


class ChapterForm(forms.ModelForm):
    chapter_number = forms.IntegerField(required=True, help_text='Enter Chapter Number', min_value=0)

    class Meta:
        model = Chapter
        fields = ['chapter_number']


class ChapterImageForm(forms.ModelForm):
    images = forms.ImageField(
        required=True,
        help_text='Upload Chapter Images',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = ChapterImage
        fields = ['images']
