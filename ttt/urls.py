# from django.urls import path
# from .views import InterviewCreateView

# app_name = 'app'

# urlpatterns = [
#     # ... other URL patterns ...
#     path('interview/add/', InterviewCreateView.as_view(), name='interview_add'),
# ]


from django.urls import path
from .views import all_panelists

urlpatterns = [
    path('all_panelists/<int:candidate_id>/', all_panelists, name='all_panelists'),
    # ... other URL patterns ...
]

