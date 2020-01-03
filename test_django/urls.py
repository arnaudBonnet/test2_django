"""test_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from apptwo import views as apptwoviews
from appone import views as apponeviews
from projet_forum import views as projetforumviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', apponeviews.hello),
    path('hello2/', apptwoviews.djangorocks),
    path('login/', projetforumviews.login, name='login'),
    path('auth/', projetforumviews.auth),
    path('list_topics/', projetforumviews.list_topics, name='list_topics'),
    path('topic/<int:topic_id>/', projetforumviews.topic, name='topic'),
    path('suppress_topic/<int:topic_id>/', projetforumviews.suppress_topic),
    path('creer_compte/', projetforumviews.create_account),
    path('logout/', projetforumviews.logout)
]
