from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    user_name = forms.CharField(max_length=30, required=True, label="名前")
    email = forms.EmailField(required=True, label="メールアドレス")

    class Meta:
        model = User
        fields = ["user_name", "email", "password1", "password2"]

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'image']  # ✅ 画像フィールドを含める

#設定画面
from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    new_first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '新しい名前を入力'})
    )
    new_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '新しいメールアドレスを入力'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'email']
        labels = {
            'first_name': '現在の名前',
            'email': '現在のメールアドレス',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}),
        }

#絵本登録
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'image']
        labels = {
            'title': 'タイトル',
            'author': '作者',
            'image': '画像',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '絵本のタイトルを入力'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '作者を入力'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
