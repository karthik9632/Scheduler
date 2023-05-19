from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.db.models.query import QuerySet, Q
from django.http.request import HttpRequest
from django.utils.html import format_html
from datetime import datetime
from .models import *
from urllib.parse import parse_qs
from django.http import HttpResponse
from django.contrib import admin


class HiringManagerCustomFilter(admin.SimpleListFilter):
    '''customized hiring manager filter'''.
    title = _('Hiring Manager')
    parameter_name= "hiring manager"

    def lookups(self, request, model_admin):
        hiring_managers = Requistion.objects.values('hiring_manager').distinct()
        result = [(x['hiring_manager'],_x(['hiring_manager'])) for x in hiring_managers]
        return result
    
    def queryset(self, request, queryset):
        value = self.value()
        if value:
            for candidate in queryset:
                if candidate.req_id.hiring_manager != value:
                    queryset= queryset.exclude(id = candidate.id)
            return queryset
        else:
            return queryset
        
class CandidateAdmin(admin.ModelAdmin):

    def view_panelist(self,obj):
       all_lob = GTIPanelist.objects.values_list('lob', flat = True).distinct()
       other_lob = ','.join([lob for lob in all_lob if lob != obj.req_id.lob])
       link = f'<a href= "/admin/ttt/gtipanelist/?lob__in={other_lob}&num_of_rounds__lt=2&candidate_id={obj.id}" class = "default"> View Panelist </a>'
       return format_html(link)

    @admin.display(description='Grade')
    def get_candidate_grade(self, obj):
        return obj.req_id.grade
    
    @admin.display(description='Job Title')
    def get_candidate_job_title(self, obj):
        return obj.req_id.job_title 
    
    @admin.display(description='LOB')
    def get_candidate_lob(self, obj):
        return obj.req_id.lob

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

    
    list_display = ('req_id','candidate_name','available_date', 'get_candidate_job_title','get_candidate_lob', 'get_candidate_grade', 'get_candidate_hiring_manager','get_candidate_recruiter','get_candidate_internal_external',  'get_candidate_diversity','resume', 'view_panelist')
    list_filter = ('req_id',HiringManagerCustomFilter)
    model = Candidate
admin.site.register(Candidate, CandidateAdmin)    


class GTIPanelsitAdmin(admin.ModelAdmin):
   
    def schedule(self,obj):
        return format_html(f'<a href= "/admin/ttt/interviews/add/?pid={obj.sid}" class = "default"> Schedule </a>' )
    
    def get_changelist(self, request, **kwargs):

        if request.session['schedule'].get('cobj'):
            self.list_display=('sid', 'name', 'lob', 'is_available', 'num_of_rounds', 'prefered_round', 'location', 'schedule')
        else:
            self.list_display=('sid', 'name', 'lob', 'is_available', 'num_of_rounds', 'prefered_round', 'location')
        
        return super().get_changelist(request, **kwargs) 
    
    def get_queryset(self, request):

        qs = super().get_queryset(request)
        query_copy = request.GET.copy()
        query_string = request.META.get('QUERY_STRING')
        parsed_query_string = parse_qs(query_string)

        if parsed_query_string.get('candidate_id'):
            candidate_id = parsed_query_string['candidate_id']
            if "candidate_id" in list(query_copy):
                query_copy.pop('candidate_id')
            candidate_id = candidate_id[0]
            request.GET = query_copy
            self.session_obj = request.session['schedule'] = {'cobj':str(candidate_id), 'pobj': " "}
        else:
            request.session['schedule']= {}

        if request.session.get('schedule').get('cobj') and parsed_query_string.get('lob_in'):
            cand = Candidate.objects.filter(id = request.session.get('schedule').get('cobj')).first()
            candidate_scheduled_round = list(set([i.interview_round for i in list(Interviews.objects.filter(candidate=cand))]))
            qs = GTIPanelist.objects.filter(~Q(lob_in=parsed_query_string['lob__in='])&(~Q(prefered_round_in = candidate_scheduled_round)))
        
            if RuleEngine.objects.filter(variable = 'panelist num of Interviews').first().is_active:

                for panelist.obj in qs:
                    if run(panelist_obj.num_of_rounds, [RoundRule()]).result==False:
                        qs = qs.exclude(sid =panelist_obj.sid)

            if RuleEngine.objects.filter(variable = 'panelist last interview date').first().is_active:

                if len(qs) == 0 and len(list(request._message))==0:
                    messages.warning(request, "All the panelist have completed two interview rounds, here's the list of panelist who isn't active from long time")
                    qs = GTIPanelist.objects.all()
                    for panelist_obj in qs:
                        if run(panelist_obj.last_interview_date, [PanelistLastRoundInterviewDate()]).result == False:
                            qs= qs.exclude(sid = panelist_obj.sid)
        return qs     

    list_display = ('sid','name', 'lob', 'is_available','number_of_interviews_in_a_month','prefered_round', 'location', 'schedule')
    list_filter = ('prefered_round','number_of_interviews_in_a_month')
    model = GTIPanelist

admin.site.register(GTIPanelist, GTIPanelsitAdmin)


class InterviewsAdmin(admin.ModelAdmin):

        def response_add(self, request, post_url_continue=None):

            pobj = request.session['schedule'].get('pobj')
            panelist = GTIPanelist.objects.filter(sid= pobj)
            if len(panelist):
                print(panelist[0].last_interview_date)
                panelist[0].last_interview_date = datetime.now()
                print(panelist[0].last_interview_date)

            if '_addanother' in request.POST:
                cobj = request.session['schedule'].get('cobj')
                candidate = Candidate.objects.filter(id = cobj).first()
                filter_lob = list(set([panelist.lob for panelist in GTIPanelist.objects.all()]))
                if candidate.req_id.lob in filter_lob:
                    filter_lob.remove(candidate.req_id.lob)
                filter_lob = ','.join(filter_lob)
                temp = f"/admin/ttt/interviews/add/?lob__in={filter_lob}&candidate_id={cobj}"
                return HttpResponseRedirect(temp)
            else:
                return super().response_add(request,obj, post_url_continue=post_url_continue)
            
        def add_view(self, request, form_url='', extra_content =None):
            query_copy = request.GET.copy()
            
            cobj = request.session['schedule']['cobj']
            pobj = request.session['schedule']['pobj']
            candidate = Candidate.objects.filter(id = cobj).first()
            panelist = GTIPanelist.objects.filter(sid = pobj).first() 
            
            return{
                
                'req_id': candidate.req_id,
                'interview_date_time': datetime.now(),
                'interviewer': panelist.sid,
                'candidate': candidate.id,
                'interview_round': panelist.prefered_round
            }


list_display = ('req_id', 'Interview_date_time', 'interviewer', 'candidate', 'created_at','cancelled_at', 'interview_round', 'status')
    # list_filter = ('req_id', 'Interview_date_time', 'interviewer', 'candidate', 'created_at','cancelled_at', 'interview_round', 'status')
admin.site.register(Interviews, InterviewsAdmin)
    

class RequistionAdmin(admin.ModelAdmin):
    list_display = ('req_id', 'hiring_manager', 'recruiter','start_date', 'last_modified_date', 'lob','grade', 'internal_external','diversity', 'req_status')
    # list_filter = ('req_id', 'hiring_manager', 'recruiter','start_date', 'last_modified_date', 'lob','req_status')
admin.site.register(Requistion, RequistionAdmin)


class RuleEngineAdmin(admin.ModelAdmin):
    list_display = ('variable', 'condition', 'value','is_active')
    fields = (
        ('variable', 'condition', 'value','is_active'),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['variable']
        else:
            return []
        
admin.site.register(RuleEngine,RuleEngineAdmin)