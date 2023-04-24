from django.contrib import admin
from django.utils.html import format_html
from .models import *
from django.urls import reverse, path
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime

from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from .forms import ScheduleForm

def get_other_model_data(self, obj):
    return GTIPanelist.table_data()

from django import forms
from django.contrib import admin

from django import forms
from django.utils.safestring import mark_safe


class CandidateAdmin(admin.ModelAdmin):
    list_display = ['req_id','candidate_name', 'lob' ,'interview_status','available_date', 'get_candidate_job_title', 'get_candidate_grade', 'get_candidate_hiring_manager','get_candidate_recruiter','get_candidate_internal_external',  'get_candidate_diversity','resume', 'view_panelist'] 
    model = Candidate

    @admin.display(description='Grade')
    def get_candidate_grade(self, obj):
        return obj.req_id.grade
    
    @admin.display(description='Job Title')
    def get_candidate_job_title(self, obj):
        return obj.req_id.job_title 

    @admin.display(description='Internal_External')
    def get_candidate_internal_external(self, obj):
        return obj.req_id.internal_external

    @admin.display(description='Diversity')
    def get_candidate_diversity(self, obj):
        return obj.req_id.diversity

    @admin.display(description='Hiring Manager')
    def get_candidate_hiring_manager(self, obj):
        return obj.req_id.hiring_manager

    @admin.display(description='Recruiter')
    def get_candidate_recruiter(self, obj):
        return obj.req_id.recruiter

    def get_queryset(self, request):
        self.full_path = request.get_full_path()
        self.session_obj = request.session['schedule'] = {"cobj":"","pobj":""}
        return super().get_queryset(request)

    def view_panelist(self,obj):
        filter_lob = list(set([panelist.lob for panelist in GTIPanelist.objects.all()]))
        if obj.lob in filter_lob:
            filter_lob.remove(obj.lob)
        filter_lob=','.join(filter_lob)
        print("vieew")
        return format_html('<a href= "/admin/ttt/gtipanelist/?lob__in={}&candidate_id={}" class = "default"> View Panelist </a>'.format(filter_lob, obj.id))

    # def response_change(self, request, obj):
    #     # Customize the URL of the panelists admin page
    #     url = reverse('admin:ttt_gtipanelist')
    #     url += f'?candidate_id={obj.id}'  # Append candidate ID as query parameter
    #     return HttpResponseRedirect(url)


class GTIPanelsitInline(admin.TabularInline):
    model = Interviews
    extra = 0

class GTIPanelsitAdmin(admin.ModelAdmin):
    list_display = ('sid','name', 'lob', 'is_available','number_of_interviews_in_a_month','prefered_round', 'location', 'schedule_interview')
    model = GTIPanelist
    inlines = [GTIPanelsitInline, ]

    # def get_queryset(self, request):
    #     self.full_path = request.get_full_path()
    #     self.session_obj = request.session['schedule'] = {"cobj":"","pobj":""}
    #     return super().get_queryset(request)
    
    def schedule_interview(self,obj):
        return format_html('<a href= "/admin/ttt/interviews/add/?pid={}" class = "default"> Schedule </a>'.format(obj.sid) )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        query_copy = request.GET.copy()
        candidate_id = query_copy.pop('candidate_id')
        candidate_id = candidate_id[0]
        request.GET = query_copy
        self.session_obj = request.session['schedule'] = {"cobj":str(candidate_id),"pobj":""}
        # if candidate_id:
            # Filter panelists based on candidate ID
            # qs = qs.filter(candidate__id=candidate_id)
        return qs

# class InterviewForm(forms.ModelForm):
#     class Meta:
#         model = Interviews
#         exclude = ["name"]


# class ScheduleForm(forms.BaseModelForm):
#     req_id = models.ForeignKey(Requistion, related_name="interviews", on_delete=models.CASCADE, null=True)
#     Interview_date_time = models.DateTimeField()
#     interviewer = models.ForeignKey(GTIPanelist, related_name = 'Interviews',on_delete=models.CASCADE, null =True)
#     candidate = models.ForeignKey(Candidate, related_name = 'Interviews', on_delete=models.CASCADE, null =True)
#     created_at = models.DateTimeField(auto_now_add=True, null = True)
#     cancelled_at = models.DateTimeField(blank=True, null = True)
#     interview_round = models.CharField(max_length=255, choices=INTERVIEW_ROUND_CHOICES, null =True)
#     status = models.CharField(max_length=22,choices=INTERVIEW_STATUS_CHOICE)


class InterviewsAdmin(admin.ModelAdmin):
    # form = ScheduleForm
    model = Interviews
    list_display = ('req_id', 'Interview_date_time', 'interviewer', 'candidate', 'created_at','cancelled_at', 'interview_round', 'status')
    list_filter = ('req_id', 'Interview_date_time', 'interviewer', 'candidate', 'created_at','cancelled_at', 'interview_round', 'status')
    def add_view(self, request, form_url='', extra_context=None):
        # Use custom form
        # self.form = ScheduleForm
        query_copy = request.GET.copy()
        panelist_id = query_copy.pop('pid')
        panelist_id = panelist_id[0]
        request.GET = query_copy
        self.session_obj = request.session['schedule']["pobj"] = panelist_id
        return super().add_view(request, form_url, extra_context)
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     # if candidate_id:
    #         # Filter panelists based on candidate ID
    #         # qs = qs.filter(candidate__id=candidate_id)
    #     return qs

    # def add_view(self, request, form_url='', extra_context=None):
    # # try:
    #     query_copy = request.GET.copy()
    #     panelist_id = query_copy.pop('pid')
    #     panelist_id = panelist_id[0]
    #     request.GET = query_copy
    #     self.session_obj = request.session['schedule']['pobj'] = str(panelist_id)
    #     print("reqeust")

    #     return super(InterviewForm, self).add_view(
    #         request, form_url, extra_context
    #     )
    # except ValidationError as e:
    #     return handle_exception(self, request, e)

    def get_changeform_initial_data(self, request):
        cobj = request.session['schedule']['cobj']
        pobj = request.session['schedule']['pobj']
        candidate = Candidate.objects.filter(id=cobj).first()
        panelist = GTIPanelist.objects.filter(sid=pobj).first()

        return {
            'req_id': candidate.req_id,
            'Interview_date_time': datetime.now(),
            'interviewer':panelist.sid,
            'candidate':candidate.id,
            'cancelled_at': datetime.now(),
            'interview_round':panelist.prefered_round
            }

 

class RequistionAdmin(admin.ModelAdmin):
    list_display = ('req_id', 'hiring_manager', 'recruiter','start_date', 'last_modified_date', 'lob','grade', 'internal_external','diversity', 'req_status')
    list_filter = ('req_id', 'hiring_manager', 'recruiter','start_date', 'last_modified_date', 'lob','req_status')


admin.site.register(GTIPanelist, GTIPanelsitAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Interviews, InterviewsAdmin)
admin.site.register(Requistion, RequistionAdmin)


