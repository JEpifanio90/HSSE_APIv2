from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from hsse_api.constants import Constants

class UserManager(BaseUserManager):
    """Manager For User Creation"""

    def create(self, email, name, password, site, contractor):
        """Yup, what it says"""
        if not email:
            raise ValueError("Hey! We need an email")
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, site=site, contractor=contractor)
        user.set_password(password)
        user.save(using=self._db)

        return user

class Site(models.Model):
    """Represents a working site"""
    name = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=70, blank=False)
    state = models.CharField(max_length=50, blank=False)
    country = models.CharField(max_length=70, blank=False)
    created_on = models.DateField(auto_now_add=True)
    objects = models.Manager()

    REQUIRED_FIELDS = ['name', 'city', 'state', 'country']

    def __str__(self):
        """String representation of our working site"""
        return self.name

class EnvironmentalIndicator(models.Model):
    renewable_electricity_consumed = models.IntegerField(blank=False, null=False)
    non_renewable_electricity_consumed = models.IntegerField(blank=False, null=False)
    consumed_gas = models.IntegerField(blank=False, null=False)
    consumed_water = models.IntegerField(blank=False, null=False)
    dangerous_waste_generated = models.IntegerField(blank=False, null=False)
    non_dangerous_waste_generated = models.IntegerField(blank=False, null=False)
    waste_sold = models.IntegerField(blank=False, null=False)
    waste_to_landfill = models.IntegerField(blank=False, null=False)
    waste_recycled = models.IntegerField(blank=False, null=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    objects = models.Manager()

class MonthlyReport(models.Model):
    no_employees = models.IntegerField(blank=False, null=False)
    no_contractors = models.IntegerField(blank=False, null=False)
    worked_employee_hours = models.IntegerField(blank=False, null=False)
    worked_contractor_hours = models.IntegerField(blank=False, null=False)
    no_reports_overdue = models.IntegerField(blank=False, null=False)
    no_reports_closed = models.IntegerField(blank=False, null=False)
    no_reports_in_progress = models.IntegerField(blank=False, null=False)
    no_reports_open = models.IntegerField(blank=False, null=False)
    created_on = models.DateField(auto_now_add=True)
    objects = models.Manager()

class SafetyActivity(models.Model):
    activity_name = models.CharField(max_length=255, blank=False, unique=True)
    comments = models.TextField(blank=True, null=True)
    site = models.ForeignKey(Site, related_name='safety_activities', on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    objects = models.Manager()
    REQUIRED_FIELDS = ['activity_name']

    def __str__(self):
        return self.activity_name

class User(AbstractBaseUser, models.Model):
    """Represents a 'user profile' inside our system"""
    email = models.EmailField(max_length=255, blank=False, unique=True)
    name = models.CharField(max_length=255, blank=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    contractor = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        """String representation of the model"""

        return self.email

class Report(models.Model):
    case_number = models.CharField(max_length=120, unique=True, blank=False, null=False)
    clock_number = models.TimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    employee_name = models.CharField(max_length=120, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    gender = models.CharField(max_length=1, blank=False, null=False, choices=Constants.GENDERS_CHOICES)
    regular_job_position = models.CharField(max_length=120, blank=False, null=False)
    address = models.CharField(max_length=120, blank=False, null=False)
    regular_department = models.CharField(max_length=120, blank=False, null=False)
    regular_job_group = models.CharField(max_length=120, blank=False, null=False)
    status = models.CharField(max_length=11, choices=Constants.STATUS_CHOICES, default="O")
    shift = models.CharField(max_length=3, blank=False, null=False, choices=Constants.COMMON_CHOICES)
    location = models.CharField(max_length=120, blank=False, null=False)
    exact_location = models.CharField(max_length=120, blank=False, null=False)
    incident_date = models.DateField(auto_now=False, auto_now_add=False)
    date_reported = models.DateField(auto_now=False, auto_now_add=False)
    first_day_lost = models.DateField(auto_now=False, auto_now_add=False)
    total_days_lost = models.IntegerField(blank=False, null=False, default=0)
    restricted_activity_start_date = models.DateField(auto_now=False, auto_now_add=False)
    total_days_restricted_activity = models.IntegerField(blank=False, null=False, default=0)
    return_work_date = models.DateField(auto_now=False, auto_now_add=False)
    type_injury = models.CharField(max_length=120, blank=False, null=False)
    body_part = models.CharField(max_length=120, blank=False, null=False)
    body_side = models.CharField(max_length=120, blank=False, null=False)
    local_clinic_name = models.CharField(max_length=120, blank=False, null=False)
    doctor_name = models.CharField(max_length=120, blank=False, null=False)
    case_type = models.CharField(max_length=3, blank=False, null=False, choices=Constants.CASE_TYPES)
    major_accident = models.CharField(max_length=3, blank=False, null=False, choices=Constants.COMMON_CHOICES)
    accident_type = models.CharField(max_length=3, blank=False, null=False, choices=Constants.ACCIDENT_TYPES)
    other_results = models.CharField(max_length=2, blank=False, null=False, choices=Constants.OTHER_RESULTS)
    area = models.CharField(max_length=120, blank=False, null=False)
    department = models.CharField(max_length=120, blank=False, null=False)
    at_operation = models.CharField(max_length=3, blank=False, null=False, choices=Constants.COMMON_CHOICES)
    location_at_event = models.CharField(max_length=120, blank=False, null=False)
    time_in_position = models.IntegerField(blank=False, null=False)
    experience_in_position = models.IntegerField(blank=False, null=False)
    contact_agent = models.CharField(max_length=120, blank=False, null=False)
    work_area = models.CharField(max_length=120, blank=False, null=False)
    exact_area = models.CharField(max_length=120, blank=False, null=False)
    equipment_involved = models.CharField(max_length=120, blank=False, null=False)
    activity_being_done = models.CharField(max_length=120, blank=False, null=False)
    injury_mecahnism = models.CharField(max_length=3, blank=False, null=False, choices=Constants.INJURY_MECHANISMS)
    fatal_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    fatality_potential = models.CharField(max_length=1, blank=False, null=False, choices=Constants.FATALITY_POTENTIAL)
    contributing_actions = models.CharField(max_length=3, blank=False, null=False, choices=Constants.CONTRIBUTING_ACTIONS)
    contributing_conditions = models.CharField(max_length=3, blank=False, null=False, choices=Constants.CONTRIBUTING_CONDITIONS)
    influenced_actions = models.CharField(max_length=4, blank=False, null=False, choices=Constants.INFLUENCE_CONTRIBUTING_ACTIONS)
    influenced_conditions = models.CharField(max_length=3, blank=False, null=False, choices=Constants.INFLUENCE_CONTRIBUTING_CONDITIONS)
    method = models.CharField(max_length=120, blank=False, null=False)
    environment = models.CharField(max_length=120, blank=False, null=False)
    administration = models.CharField(max_length=120, blank=False, null=False)
    person_responsible = models.CharField(max_length=120, blank=False, null=False)
    equipment_machinery = models.CharField(max_length=120, blank=False, null=False)
    people = models.CharField(max_length=120, blank=False, null=False)
    supervisor = models.ForeignKey(User, related_name='report_supervisor', on_delete=models.CASCADE, blank=True, null=True)
    date_time = models.DateTimeField(auto_now=True)
    completion_date = models.DateField(auto_now=True)
    other_participants = models.CharField(max_length=120, blank=False, null=False)
    approved_by = models.ForeignKey(User, related_name='report_approver', on_delete=models.CASCADE, blank=True, null=True)
    approved_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    ehhs_leader = models.ForeignKey(User, related_name='report_leader', on_delete=models.CASCADE, blank=True, null=True)
    ehhs_approval = models.DateField(auto_now=False, auto_now_add=True)
    incident_description = models.TextField(blank=False, null=False)
    incident_contributing_actions = models.TextField(blank=False, null=False)
    incident_contributing_conditions = models.TextField(blank=False, null=False)
    created_by = models.ForeignKey(User, related_name='report_creator', on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    objects = models.Manager()

class Question(models.Model):
    control_type = models.CharField(max_length=50, blank=False, null=False)
    disabled = models.BooleanField()
    error = models.CharField(max_length=150, blank=True, null=True, default='')
    form = models.CharField(max_length=50, blank=False, null=False)
    icon = models.CharField(max_length=50, blank=False, null=False)
    input_type = models.CharField(max_length=20, blank=False, null=False)
    key = models.CharField(max_length=120, blank=False, null=False, unique=False)
    objects = models.Manager()
    label = models.CharField(max_length=120, blank=False, null=False)
    options = models.CharField(max_length=255, blank=True, null=True)
    required = models.BooleanField()
    value = models.CharField(max_length=50, blank=True, null=True)
