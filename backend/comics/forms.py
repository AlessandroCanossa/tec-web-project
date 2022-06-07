from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Comic, Genre, Chapter, ChapterImage


class UserForm(UserCreationForm):
    username = forms.CharField(max_length=200, required=True, help_text='Enter Username', widget=forms.TextInput())
    email = forms.EmailField(max_length=100, required=True, help_text='Enter Email Address', widget=forms.TextInput())

    first_name = forms.CharField(max_length=100, required=True, help_text='Enter First Name', widget=forms.TextInput())
    last_name = forms.CharField(max_length=100, required=True, help_text='Enter Last Name', widget=forms.TextInput())

    password1 = forms.CharField(help_text='Enter Password', required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, help_text='Enter Password Again', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


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
