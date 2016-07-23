from django.contrib import admin

from django.apps import apps

from .models import Assignment

# See http://stackoverflow.com/questions/9443863/register-every-table-class-from-an-app-in-the-django-admin-page for inspiration on how to auto-add all models to the admin for me.
app = apps.get_app_config('workbook')

for model_name, model in app.models.items():
    if not model_name == "assignment":
        admin.site.register(model)

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "office", "section", "ordering")
    list_editable = ("ordering",)
    list_filter = ("office", "section")
    search_fields = ['title']

admin.site.register(Assignment, AssignmentAdmin)
