from django import forms
from projet_forum.models import User, Topic, Messages


class LoginForm(forms.Form):
    login = forms.CharField(label="Votre login", max_length=50)
    mdp = forms.CharField(widget=forms.PasswordInput, label="Votre mot de passe", max_length=50)


class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["nom"]


class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ["message"]


class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "mdp"]
