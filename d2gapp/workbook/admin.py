from django.contrib import admin

from django.apps import apps

# See http://stackoverflow.com/questions/9443863/register-every-table-class-from-an-app-in-the-django-admin-page for inspiration on how to auto-add all models to the admin for me.
app = apps.get_app_config('workbook')

for model_name, model in app.models.items():
        admin.site.register(model)
