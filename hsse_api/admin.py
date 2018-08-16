from django.contrib import admin
from hsse_api import models

# Register your models here.
admin.site.register(models.AuditInspection)
admin.site.register(models.CorrectiveAction)
admin.site.register(models.EmployeeCommunityActivity)
admin.site.register(models.EnvironmentalIndicator)
admin.site.register(models.MonthlyReport)
admin.site.register(models.Report)
admin.site.register(models.SafetyActivity)
admin.site.register(models.Site)
admin.site.register(models.User)