from django.contrib import admin
from .models import Organization, Package , SmsSetting , EmailSetting, MpesaSetting, SystemSetting, SecuritySetting, TemplateSetting

# Register your models here.
admin.site.register(Organization) 
admin.site.register(Package)
admin.site.register(SmsSetting)
admin.site.register(EmailSetting)
admin.site.register(MpesaSetting)
admin.site.register(SystemSetting)
admin.site.register(SecuritySetting)
admin.site.register(TemplateSetting)