from django.contrib import admin
from hsse_api import models

# Register your models here.
admin.site.register(models.Audit_Inspection)
admin.site.register(models.Corrective_Action)
admin.site.register(models.Employee_Community_Activity)
admin.site.register(models.Environmental_Indicators)
admin.site.register(models.Monthly_Reports)
admin.site.register(models.Report)
admin.site.register(models.Safety_Activity)
admin.site.register(models.Site)
admin.site.register(models.User)