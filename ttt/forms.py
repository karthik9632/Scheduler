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
	interview_data_time = forms.DateTimeField()
	candidate_name = forms.CharField(required=False)
	candidate_id = forms.CharField(required=False)
	interviewer_name = forms.CharField(required=False)
	interviewer_id = forms.CharField(required=False)
	cancelled_at = forms.DateTimeField(required=False)
	interview_round = forms.ChoiceField()#choices=INTERVIEW_ROUND_CHOICES, required=True)
	status = forms.ChoiceField(choices=INTERVIEW_STATUS_CHOICE, required=True)
	resume = forms.FileField(required=False)