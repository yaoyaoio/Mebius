from django.contrib import admin
# Register your models here.
from member import models

class GroupInline(admin.StackedInline):
    model = models.Group
    exclude = ('memo',)
    readonly_fields = ['name',]

class UserAdmin(admin.ModelAdmin):
    list_display = ('name','email','phone','ip','secret_key','memo',)
    inlines = [GroupInline]

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','owner','memo',)


admin.site.register(models.UserProfile,UserAdmin)
admin.site.register(models.Group,GroupAdmin)