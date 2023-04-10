from django import forms

INTERVIEW_ROUND_CHOICES = [
        ('SDLC','SLDC'),
        ('Architecture', 'Architecture'),
        ('Coding', 'Coding')
    ]

INTERVIEW_STATUS_CHOICE= [
        ('In-Process', 'In-process'),
        ('Scheduled', 'Scheduled'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
        ('On-hold', 'On-hold') 
    ]


class ScheduleForm(forms.Form):
    req_id = forms.IntegerField(required=True, label="Requisition ID:")
    interviewer = forms.CharField(required=False,)
    candidate = forms.CharField(required=False)
    interview_round = forms.ChoiceField(choices=INTERVIEW_ROUND_CHOICES, required=True)
    status = forms.ChoiceField(choices=INTERVIEW_STATUS_CHOICE, required=True)