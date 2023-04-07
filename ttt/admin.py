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

class CandidateInline(admin.TabularInline):
    model = Interviews

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('req_id','candidate_name', 'email', 'lob' ,'interview_status', 'resume', 'view_panelist')
    model = Candidate
    inlines = [CandidateInline, ]

    def view_panelist(self,obj):
        filter_lob = list(set([panelist.lob for panelist in GTIPanelist.objects.all()]))
        if obj.lob in filter_lob:
            filter_lob.remove(obj.lob)
        filter_lob=','.join(filter_lob)
        return format_html('<a href= "/admin/ttt/candidate/{}/change/" class = "default"> View Panelist </a>'.format(obj.id) )


class GTIPanelsitInline(admin.TabularInline):
    model = Interviews

class GTIPanelsitAdmin(admin.ModelAdmin):
    model = GTIPanelist
    inlines = [GTIPanelsitInline, ]

class InterviewsAdmin(admin.ModelAdmin):
    list_display = ('req_id', 'Interview_date_time', 'interviewer', 'candidate', 'created_at','cancelled_at', 'interview_round', 'status')
    list_filter = ('req_id', 'Interview_date_time', 'interviewer', 'candidate', 'created_at','cancelled_at', 'interview_round', 'status')


class RequistionAdmin(admin.ModelAdmin):
    list_display = ('req_id', 'hiring_manager', 'recruiter','start_date', 'last_modified_date', 'lob','req_status')
    list_filter = ('req_id', 'hiring_manager', 'recruiter','start_date', 'last_modified_date', 'lob','req_status')


admin.site.register(GTIPanelist, GTIPanelsitAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Interviews, InterviewsAdmin)
admin.site.register(Requistion, RequistionAdmin)


