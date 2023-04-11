from django.contrib import admin
from django.utils.html import format_html
from .models import *
from django.urls import reverse, path
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse

def get_other_model_data(self, obj):
    return GTIPanelist.table_data()

from django import forms
from django.contrib import admin

from django import forms
from django.utils.safestring import mark_safe

# class CandidateInline(admin.TabularInline):
#     model = Interviews
#     extra = 0

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('req_id','candidate_name', 'lob' ,'interview_status', 'resume', 'view_panelist')
    model = Candidate
    # inlines = [CandidateInline, ]

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
        return format_html('<a href= "/admin/ttt/gtipanelist/?lob__in={}#cobj={}" class = "default"> View Panelist </a>'.format(filter_lob, obj.id))


class GTIPanelsitInline(admin.TabularInline):
    model = Interviews
    extra = 0

class GTIPanelsitAdmin(admin.ModelAdmin):
    list_display = ('sid','name', 'lob', 'is_available','number_of_interviews_in_a_month','prefered_round', 'location', 'schedule_interview')
    model = GTIPanelist
    inlines = [GTIPanelsitInline, ]

    def get_queryset(self, request):
        self.full_path = request.get_full_path()
        self.session_obj = request.session['schedule'] = {"cobj":"","pobj":""}
        return super().get_queryset(request)
    
    def schedule_interview(self,obj):
        return format_html(f'<a href= "/admin/ttt/interviews/add/" class = "default"> Schedule </a>' )


class InterviewsAdmin(admin.ModelAdmin):
    list_display = ('req_id', 'Interview_date_time', 'interviewer', 'candidate', 'created_at','cancelled_at', 'interview_round', 'status')
    list_filter = ('req_id', 'Interview_date_time', 'interviewer', 'candidate', 'created_at','cancelled_at', 'interview_round', 'status')


class RequistionAdmin(admin.ModelAdmin):
    list_display = ('req_id', 'hiring_manager', 'recruiter','start_date', 'last_modified_date', 'lob','grade', 'internal_external','diversity', 'req_status')
    list_filter = ('req_id', 'hiring_manager', 'recruiter','start_date', 'last_modified_date', 'lob','req_status')


admin.site.register(GTIPanelist, GTIPanelsitAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Interviews, InterviewsAdmin)
admin.site.register(Requistion, RequistionAdmin)


