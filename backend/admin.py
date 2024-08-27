from django.contrib import admin
from django.apps import apps

# Get the models.py module for the current app
models = apps.get_models()

# Dynamically import all the models from the module
for model in models:
    if not admin.site.is_registered(model):
        admin.site.register(model)