from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from projet_forum import forms
from django.http import HttpResponseForbidden

from projet_forum.forms import CreateTopicForm, CreateMessageForm, CreateAccountForm, LoginForm
from projet_forum.models import Topic, Messages, User


def login(request):
    if 'member_id' not in request.session:
        form = LoginForm()
        template = loader.get_template('projet_forum/template_login.html')
        account_form = CreateAccountForm()
        return HttpResponse(template.render({"form": form, "form2": account_form}, request))
    else:
        template = loader.get_template('projet_forum/template_logged_in.html')
        user = User.objects.filter(pk=request.session['member_id'])[0]
        return HttpResponse(template.render({"name": user.name}, request))


def auth(request):
    username = "unknown"
    mdp = "unknown"
    if (request.method == 'POST'):
        form = forms.LoginForm(request.POST)
        if form.is_valid() == False:
            return HttpResponse(
                "Il y a eu une erreur dans le traitment du formulaire, veuillez vérifier les entrées saisies.")
        username = form.cleaned_data['login']
        mdp = form.cleaned_data['mdp']
        list_user = User.objects.filter(name__exact=username).filter(mdp__exact=mdp)
        if len(list_user) > 0:
            # On fait une création de session.
            request.session["member_id"] = list_user[0].pk
            # return HttpResponse("Vous êtes bien authentifié en tant que "+username)
            return HttpResponseRedirect(reverse("list_topics"))
        else:
            return HttpResponse(
                "Impossible de vous authentifier en tant que " + username + " verifier votre couple username/mdp.")
    else:
        return HttpResponseForbidden()

def suppress_topic(request, topic_id):
    if 'member_id' in request.session:
        #On est connecté donc on a le droit de supprimer le topic.
        topics = Topic.objects.filter(pk=topic_id)
        if len(topics) > 0:
            topic = topics[0]
            try:
                topic.delete()
                return HttpResponseRedirect(reverse("list_topics"))
            except:
                return HttpResponse("Une erreur est survenue pendant la tentative de suppression du topic.")
        else:
            return HttpResponse("La suppression du topic demandée est impossible, aucun topic avec l'id "+str(topic_id))
    else:
        return HttpResponse("L'action de suppression d'un topic ne peut être effectuée que lorsque vous êtes connecté !")

def list_topics(request):
    if 'member_id' in request.session:
        if request.method == 'GET':
            # On est en méthode GET, donc on récupère la liste
            # de topics et on affiche le formulaire de création de topic.
            topicForm = CreateTopicForm()
            list_topic = Topic.objects.all()
            new_liste_topic = []
            for topic in list_topic:
                new_liste_topic.append({"nom": topic.nom, "id": topic.pk})
            template = loader.get_template('projet_forum/template_liste_topic.html')
            return HttpResponse(template.render({"liste_topic": new_liste_topic, "form": topicForm}, request))
        else:
            # On est en méthode POST, donc on sait que c'est le formulaire de creation de topic qui a été envoyé.
            topicForm = CreateTopicForm(request.POST)
            topicForm.save()
            return HttpResponseRedirect(reverse("list_topics"))
    else:
        return HttpResponse("Vous n'etes pas authentifié, vous n'avez pas le droit d'accéder à la liste de topics.")


def topic(request, topic_id):
    if 'member_id' in request.session:
        if request.method == 'GET':
            id = topic_id
            list_messages = Messages.objects.filter(topic_id=id).select_related("author_id")
            new_liste_messages = []
            message_form = CreateMessageForm()
            for message in list_messages:
                new_liste_messages.append({"auteur": message.author_id.name, "message": message.message})
            template = loader.get_template('projet_forum/template_page_topic.html')
            return HttpResponse(
                template.render({"liste_messages_topic": new_liste_messages, "form": message_form}, request))
        else:
            # On est en méthode POST, donc un message a été posté.
            message = CreateMessageForm(request.POST)
            new_message = message.save(commit=False)
            author = User.objects.filter(pk=request.session['member_id'])[0]
            current_topic = Topic.objects.filter(pk=topic_id)[0]
            new_message.author_id = author
            new_message.topic_id = current_topic
            new_message.save()
            return HttpResponseRedirect(reverse("topic", args=[topic_id]))
    else:
        return HttpResponse("Vous n'etes pas authentifié, vous n'avez pas le droit d'accéder à la liste de topics.")


def reset_session(request):
    request.session.flush()
    return HttpResponse("Vous êtes déconnectés !")


def logout(request):
    if 'member_id' in request.session:
        request.session.flush()
    return HttpResponseRedirect(reverse("login"))


def create_account(request):
    if request.method == 'POST':
        # On vient de recevoir une requete POST, cela veux dire qu'on doit créer un nouveau user.
        account_form = CreateAccountForm(request.POST)
        if account_form.is_valid():
            # Ok
            new_user = account_form.save(commit=False)
            nom = account_form.cleaned_data["name"]
            prenom = nom
            mdp = account_form.cleaned_data["mdp"]
            new_user.prenom = nom
            try:
                new_user.save()
                return HttpResponse("Votre compte a bien été créé, vous pouvez maintenant vous connecter avec.")
            except:
                return HttpResponse("Une erreur est survenue pendant l'enregistrement de User ")
        else:
            # Ko
            return HttpResponse("Impossible de créer un nouvel utilisateur, une erreur est survenue !")
    else:
        return HttpResponseRedirect(reverse("login"))
