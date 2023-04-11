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
from .forms import ScheduleForm

def candidate_list(request):
    # candidates = Candidate.objects.all()
    # context = {'candidates': candidates}
    candidate_id = request.GET.get('cid')
    if candidate_id:
        candidates = list(Candidate.objects.filter(id=candidate_id).values('id','req_id','candidate_name', 'email', 'lob' ,'interview_status', 'resume'))
    else:
        candidates = list(Candidate.objects.values('id','req_id','candidate_name', 'email', 'lob' ,'available_date', 'interview_status', 'resume', 'req_id__grade', 'req_id__internal_external', 'req_id__diversity', 'req_id__hiring_manager'))

    context = {'candidates': candidates}
    return render(request, 'candidate.html', context)



def panelists_list(request):
    candidate_id = request.GET.get('cid')
    panelist_id = request.GET.get('pid')
    if candidate_id:
        lob = Candidate.objects.filter(id=candidate_id).first().lob
        panelists = GTIPanelist.objects.filter(~Q(lob=lob)&(Q(number_of_interviews_in_a_month__lt=2))).values('sid','name', 'email', 'lob', 'is_available','number_of_interviews_in_a_month','prefered_round', 'location')
    elif panelist_id:
        panelists = GTIPanelist.objects.filter(sid=panelist_id).values('sid','name', 'email', 'lob', 'is_available','number_of_interviews_in_a_month','prefered_round', 'location')    
    else:
        panelists = GTIPanelist.objects.values('sid','name', 'email', 'lob', 'is_available','number_of_interviews_in_a_month','prefered_round', 'location')    
    
    context ={
        'panelists': list(panelists),
        'candidate_id':candidate_id
    }
    return render(request, 'panelist.html', context)

def schedule_list(request):
    args = {}
    args['schedules'] = list(Interviews.objects.values())
    return render(request, 'schedule.html', args)


def schedule_interview(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            req_id = form.cleaned_data.get('req_id')
            req_id = Requistion.objects.filter(req_id=req_id).first()
            interviewer = form.cleaned_data.get('interviewer')
            interviewer = GTIPanelist.objects.filter(sid=interviewer).first()
            candidate = form.cleaned_data.get('candidate')
            candidate = Candidate.objects.filter(id=candidate).first()
            interview_round = form.cleaned_data.get('interview_round')
            status = form.cleaned_data.get('status')
            new_interview = Interviews(req_id=req_id, interviewer=interviewer, candidate=candidate,interview_round=interview_round, status=status)
            print(req_id, interviewer, candidate, interview_round, status)
            new_interview.save()
            return HttpResponse("success")

    cid = request.GET.get('cid')
    pid = request.GET.get('pid')
    args ={}
    args['cid'] = cid
    args['pid'] = pid
    candidate = Candidate.objects.filter(id=cid).first()
    panelist = GTIPanelist.objects.filter(sid=pid).first()
    if candidate and panelist:
        initial_values = {
            "req_id":str(candidate.req_id.req_id),
            "interviewer":str(panelist.sid),
            "candidate":str(candidate.id),
            }
        form = ScheduleForm(initial=initial_values)
        args['form'] = form
        return render(request, 'schedule_interview.html', args)
    return render(request, 'schedule_interview.html', args)

