from django.contrib import admin
from django.utils.html import format_html
from datetime import datetime
from .models import *
from urllib.parse import parse_qs
from django.http import HttpResponse
from django.contrib import admin


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
    list_filter = ('req_id',)
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
        return qs     

    list_display = ('sid','name', 'lob', 'is_available','number_of_interviews_in_a_month','prefered_round', 'location', 'schedule')
    list_filter = ('prefered_round','number_of_interviews_in_a_month')
    model = GTIPanelist

admin.site.register(GTIPanelist, GTIPanelsitAdmin)


class InterviewsAdmin(admin.ModelAdmin):

        def save_model(self, request, obj, form, change):
            super(InterviewsAdmin,self).save_model(request, obj, form, change)
            if '_addanother' in request.POST:
                cobj = request.session['schedule'].get('cobj')
                pobj = request.session['schedule'].get('pobj')
                candidate = Candidate.objects.filter(id = cobj).first()
                filter_lob = list(set([panelist.lob for panelist in GTIPanelist.objects.all()]))

                if candidate.req_id.lob in filter_lob:
                    filter_lob = ','.join(filter_lob)
                temp = f"/admin/ttt/gtipanelist/?lob__in={filter_lob}&num_of_rounds__lt=2&candidate_id={cobj}"
                response = HttpResponse()
                response['Location'] = temp
                response.status_code = 302
                return response

        def add_view(self, request, form_url='', extra_content =None):
            query_copy = request.GET.copy()
            if 'pid' in list(query_copy):
                panelist_id = query_copy.pop('pid')
                panelist_id = panelist_id[0]
                request.GET = query_copy
                self.session_obj = request.session['schedule']['pobj'] = panelist_id
            return super().add_view(request, form_url, extra_content) 

        def get_changeform_initial_data(self, request):
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


