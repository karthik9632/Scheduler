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

@login_required
def all_panelists(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    panelists = GTIPanelist.objects.exclude(lob=candidate.lob)
    context = {
        'candidate': candidate,
        'panelists': panelists,
    }
    return render(request, 'all_panelists.html', context)
