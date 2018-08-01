from rest_framework import serializers
from . import models

class Audit_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Audit_Inspection
        fields = ('audit_type', 'due_date', 'made_by')

class Corrective_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Corrective_Action
        fields = ('action', 'due_date', 'status', 'supervisor', 'other_participants', 'ehhs', 'manager', 'created_by')

class Community_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Employee_Community_Activity
        fields = ('activity_number', 'activity_type', 'community_act', 'name', 'group')

class Environmental_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Environmental_Indicators
        fields = (
            'renewable_electricity_consumed',
            'non_renewable_electricity_consumed',
            'consumed_gas',
            'consumed_water',
            'dangerous_waste_generated',
            'non_dangerous_waste_generated',
            'waste_sold',
            'waste_to_landfield',
            'waste_recycled'
        )

class Report_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Report
        fields = (
            'case_number',
            'clock_number',
            'employee_name',
            'age',
            'gender',
            'regular_job_position',
            'address',
            'regular_department',
            'regular_job_group',
            'shift',
            'location',
            'exact_location',
            'incident_date',
            'date_reported',
            'first_day_lost',
            'total_days_lost',
            'restricted_activity_start_date',
            'total_days_restricted_activity',
            'return_work_date',
            'type_injury',
            'body_part',
            'body_side',
            'local_clinic_name',
            'doctor_name',
            'case_type',
            'major_accident',
            'accident_type',
            'other_results',
            'area',
            'department',
            'at_operation',
            'location_at_event',
            'time_in_position',
            'experience_in_position',
            'date',
            'contact_agent',
            'work_area',
            'exact_area',
            'equipment_involved',
            'activity_being_done',
            'injury_mecahnism',
            'fatal_date',
            'fatality_potential',
            'contributing_actions',
            'contributing_conditions',
            'influenced_actions',
            'influenced_conditions',
            'method',
            'environment',
            'administration',
            'person_responsible',
            'equipment_machinery',
            'people',
            'supervisor',
            'date_time',
            'completion_date',
            'other_participants',
            'approved_by',
            'apporved_date',
            'ehhs_leader',
            'ehhs_approval',
            'incident_description',
            'incident_contributing_actions',
            'incident_contributing_conditions',
            'made_by'
        )
        extra_kwargs = {'case_number': {'write_only': True}}

class Montly_Report_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Monthly_Reports
        fields = (
            'no_employees',
            'no_contractors',
            'worked_employee_hours',
            'worked_contractor_hours',
            'no_reports_overdue',
            'no_reports_closed',
            'no_reports_in_progress',
            'no_reports_open'
        )

class User_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class Safety_Activity_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Safety_Activity
        fields = ('activity_name', 'comments')

class Site_Serializer(serializers.ModelSerializer):

    class Meta:
        model = models.Site
        fields = (
            'name',
            'address',
            'city',
            'state',
            'country',
            'user',
            'activity',
            'environmental_indicator',
            'employee_com_activity'
        )
