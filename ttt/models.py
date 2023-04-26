from django.db import models

TOWER_CHOICES = [
        ('CNS', 'CNS'),
        ('EIS', 'EIS'),
        ('EWP','EWP'),
        ('PS', 'PS')
    ]

INTERVIEW_ROUND_CHOICES = [
        ('SDLC','SLDC'),
        ('Architecture', 'Architecture'),
        ('Coding', 'Coding')
    ]

REQUISTION_STATUS_CHOICES =[
    ('Approved', 'Approved'),
    ('Cancelled', 'Cancelled'),
    ('Completed', 'Completed'),
    ('On-hold', 'On-hold'),
    ('In-progress', 'In-progress')
    ]

GRADE_CHOICES=[
    ('601', '601'),
    ('602', '602'),
    ('603', '603'),
    ('604', '604')
]

INTERNAL_EXTERNAL_CHOICES=[
    ('Internal', 'Internal'),
    ('External', 'External')
]

DIVERSITY_CHOICES=[
    ('Diversity', 'Diversity'),
    ('Non-Diversity', 'Non-Diversity'),
]

CANDIDATE_STATUS_CHOICE= [
        ('In-Process', 'In-process'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
        ('Offered', 'Offered') 
    ]

INTERVIEW_STATUS_CHOICE= [
        ('In-Process', 'In-process'),
        ('Scheduled', 'Scheduled'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
        ('On-hold', 'On-hold') 
    ]

LOCATION_CHOICES= [
    ('Bengaluru', 'Bengaluru'),
    ('Hyderabad', 'Hyderabad'),
    ('Mumbai', 'Mumbai')
    ]


class Requistion(models.Model):

    '''Requisition ID is the ID associated with one particular job position in JPMC , Identified from a unique 9 digit REQ-ID'''
    '''set up a model on requistion '''


    req_id = models.CharField(primary_key =True,max_length=9, unique=True)
    recruiter = models.CharField(max_length=255)
    hiring_manager  = models.CharField(max_length= 255)
    start_date = models.DateField(auto_now=True, null = True)
    last_modified_date = models.DateField(null=True)
    job_title = models.CharField(max_length=255, default="")
    lob = models.CharField(max_length=4, null=False, choices=TOWER_CHOICES)
    grade = models.CharField(max_length=3, null=False, choices= GRADE_CHOICES, default="603")
    internal_external = models.CharField(max_length=20, null=False, choices=INTERNAL_EXTERNAL_CHOICES , default="External")
    diversity = models.CharField(max_length=20, null=False, choices=DIVERSITY_CHOICES , default="Diversity")
    req_status = models.CharField(max_length=50, choices=REQUISTION_STATUS_CHOICES)

    class meta:
        db_table = "Requisition"
        verbose_name_plural = "Requisition"

    def __str__(self) -> str:
        return f'{self.req_id}'


class Candidate(models.Model):

    '''setup a model with Interview_candidate info'''

    req_id = models.ForeignKey(Requistion, related_name='candidate', on_delete=models.CASCADE, null = True)
    candidate_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    lob = models.CharField(max_length=255, choices= TOWER_CHOICES)
    available_date = models.DateTimeField(null = True)
    interview_status = models.CharField(max_length=25, choices= CANDIDATE_STATUS_CHOICE)
    resume = models.FileField(upload_to='resumes/', blank = True, null= True)

    class Meta:
        db_table = 'Available Candidates'
        verbose_name_plural = 'Available Candidates'

    def __str__(self) -> str:
        return self.candidate_name
    
    def get_all_details(self):
        return self.candidate_name


class GTIPanelist(models.Model):

    """set up a model with Information of Interviewer"""

    sid = models.CharField(primary_key=True,max_length=7,unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    lob = models.CharField(max_length=25, choices=TOWER_CHOICES)
    prefered_round = models.CharField(max_length=255, choices=INTERVIEW_ROUND_CHOICES)
    number_of_interviews_in_a_month = models.PositiveIntegerField()
    location = models.CharField(max_length= 255, choices=LOCATION_CHOICES, null= True)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'Available Panelist'
        verbose_name_plural = 'Available Panelist'

    def __str__(self):
        return self.name
    
    def table_data(self):
        return GTIPanelist.objects.all()
  

class Interviews(models.Model):

    '''now gather all the data required to setup an Interview accordingly'''

    req_id = models.ForeignKey(Requistion, related_name="interviews", on_delete=models.CASCADE, null=True)
    Interview_date_time = models.DateTimeField(auto_now_add=True)
    interviewer = models.ForeignKey(GTIPanelist, related_name = 'Interviews',on_delete=models.CASCADE, null =True)
    candidate = models.ForeignKey(Candidate, related_name = 'Interviews', on_delete=models.CASCADE, null =True)
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    cancelled_at = models.DateTimeField(blank=True, null = True)
    interview_round = models.CharField(max_length=255, choices=INTERVIEW_ROUND_CHOICES, null =True)
    status = models.CharField(max_length=22,choices=INTERVIEW_STATUS_CHOICE)

    class Meta:
        db_table = "Scheduled Interviews"
        verbose_name_plural = "Scheduled Interviews"

    def __str__(self) -> str:
        return f'{self.candidate.candidate_name}-{self.interviewer.name}- {self.Interview_date_time}'




   

    