from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<level>[\w-]+)/$',
        views.QuestionView.as_view(), name='questions'),
]
