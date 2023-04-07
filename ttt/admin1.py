from django.contrib import admin

# Register your models here.
from .models1 import Atadmin, Statuses, Book
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter


class StatusListFilter(MultipleChoiceListFilter):
    title = 'Status'
    parameter_name = 'status__in'

    def lookups(self, request, model_admin):
        return Statuses.CHOICES


class PersonAdmin(admin.ModelAdmin):
    list_display = ['name','status','show_firm_url']
    list_filter = ('name',StatusListFilter)


    def get_queryset(self, request):
        self.full_path = request.get_full_path()
        self.session_obj = request.session['schedule'] = {"cobj":"","pobj":""}
        return super().get_queryset(request)
    
    def show_firm_url(self, obj):
        from django.utils.html import format_html
        name = [x.name for x in Atadmin.objects.all()]
        name.remove(obj.name)
        filter_name = ','.join(name)
        print(self.session_obj)
        return format_html('<a href="http://localhost:8001/admin/ttt/atadmin/?name__in={}#cob={}">view books</a>'.format(filter_name, obj.id))

    show_firm_url.allow_tags = True

class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author']

admin.site.register(Atadmin, PersonAdmin)
admin.site.register(Book, BookAdmin)
