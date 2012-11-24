from django.shortcuts import render
from agora.models import Decision
from datetime import datetime

def index(request,
          template_name="index.html"):
    in_progress = Decision.objects.filter(closed_at__gt = datetime.now())
    closed = Decision.objects.filter(closed_at__lt = datetime.now())
    return render(request, template_name,
        {
            'in_progress' : in_progress,
            'closed' : closed,
        })

def about(request,
		  template_name="about.html"):
	return render(request, template_name)