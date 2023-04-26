# from django.urls import path
# from .views import InterviewCreateView

# app_name = 'app'

# urlpatterns = [
#     # ... other URL patterns ...
#     path('interview/add/', InterviewCreateView.as_view(), name='interview_add'),
# ]


from django.urls import path
from .views import candidate_list, panelists_list, schedule_list, schedule_interview

urlpatterns = [
    path('', schedule_list, name='schedules'),
    path('candidate', candidate_list, name='candidate'),
    path('panelist', panelists_list, name='panelists'),
    path('schedule', schedule_interview, name='schedule_interview'),
    # path('all_panelists/<int:candidate_id>/', all_panelists, name='all_panelists'),
    # ... other URL patterns ...
]

