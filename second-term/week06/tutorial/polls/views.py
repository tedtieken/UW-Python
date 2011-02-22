# Create your views here.
from polls.models import Poll

from django.conf import settings
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, Context
from django.contrib import messages
from datetime import datetime

def poll_index(request):
    polls = Poll.objects.all()
    return render_to_response('polls/poll_index.html', locals(), context_instance=RequestContext(request))
    
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    return render_to_response('polls/poll_detail.html', locals(), context_instance=RequestContext(request))

    
def poll_vote(request, poll_id):
    return None
    
def poll_results(request, poll_id):
    return None
    
