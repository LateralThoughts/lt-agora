from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.shortcuts import render
from django.conf import settings
from datetime import datetime

from agora.models import Decision
from agora.forms import DecisionForm


class DecisionListView(ListView):

    model = Decision


class DecisionDetailView(DetailView):

    model = Decision


class DecisionCreateView(CreateView):
    form_class = DecisionForm
    login_required = True


class AuthorDetailView(DetailView):

    model = User


def index(request,
          template_name="index.html"):
    in_progress = Decision.objects.filter(closed_at__gt=datetime.now())
    closed = Decision.objects.filter(closed_at__lt=datetime.now())
    return render(request, template_name,
                {
                    'in_progress': in_progress,
                    'closed': closed,
                    'organization_name': settings.AGORA_ORGANIZATION_SHORTNAME
                })


def about(request,
          template_name="about.html"):
    return render(request, template_name)
