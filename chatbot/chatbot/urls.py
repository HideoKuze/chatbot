"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from bot import views
from bot.views import Events, chatlio_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^events/', Events.as_view()),
   # url(r'^data/', Data.as_view()),
   # url(r'^conversation-archive/', ConversationArchive.as_view()),
    url(r'^widget/', chatlio_view.as_view()),

]
