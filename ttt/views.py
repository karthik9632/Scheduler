# from django.shortcuts import render
# from .models import Candidate, GTIPanelist, Interviews
# from django.urls import reverse, path

# # Create your views here.

# def schedule_view(self, request, panelist_id):
#     candidate_id = request.GET.get('candidate_id')
#     candidate = Candidate.objects.get(id=candidate_id)
#     panelist = GTIPanelist.objects.get(id=panelist_id)
#     interview = Interviews(candidate=candidate, panelist=panelist)
#     form = InterviewForm(instance=interview)
#     context = {
#         'form': form,
#         'candidate_id': candidate_id,
#         'panelist_id': panelist_id,
#         'url': reverse('admin:app:interview_add'),
#     }
#     return render(request, 'admin/schedule_interview.html', context)


# from django.views.generic.edit import CreateView
# from .models import Interviews

# class InterviewCreateView(CreateView):
#     model = Interviews
#     fields = ['candidate', 'panelist', 'interview_date', 'interview_time']


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Candidate, GTIPanelist

# @login_required
# def all_panelists(request, candidate_id):
#     candidate = Candidate.objects.get(id=candidate_id)
#     panelists = GTIPanelist.objects.exclude(lob=candidate.lob)
#     context = {
#         'candidate': candidate,
#         'panelists': panelists,
#     }
#     return render(request, 'all_paneladmin/ttt/candidate/ists.html', context)

from django.http import HttpResponse
from .models import *
from django.db.models import Q

def candidate_list(request):
    candidates = Candidate.objects.all()
    # context = {'candidates': candidates}
    args = {}
    args['candidates'] = list(Candidate.objects.values('id','req_id','candidate_name', 'email', 'lob' ,'interview_status', 'resume'))
    return render(request, 'candidate.html', args)
    # return render(request, 'candidate.html', context=candidates.__dict__)


def panelists_list(request):
    c_id = request.GET.get('candidate_id')
    if c_id:
        lob = Candidate.objects.filter(id=c_id).first().lob
    else:
        lob=None
    panelists = GTIPanelist.objects.filter(~Q(lob=lob)).values('sid','name', 'email', 'lob', 'is_available','number_of_interviews_in_a_month','prefered_round', 'location')
    args = {}
    args['panelists'] = list(panelists)
    args['candidate_id'] = c_id
    return render(request, 'panelist.html', args)


