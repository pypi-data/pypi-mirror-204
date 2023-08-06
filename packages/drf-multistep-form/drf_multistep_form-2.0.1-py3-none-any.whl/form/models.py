from django.db import models
from django.db.models import JSONField
from form.contants import FieldType, FieldValidation


class Form(models.Model):
    form_name = models.CharField(max_length=255)
    form_description = models.TextField()

class Step(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    step_number = models.IntegerField()
    step_title = models.CharField(max_length=255)
    step_description = models.TextField()

class Field(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE)
    field_type = models.CharField(max_length=20, choices=FieldType.choices())
    field_label = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)
    field_placeholder = models.CharField(max_length=255, blank=True)
    field_help_text = models.TextField(blank=True)
    field_attributes = JSONField(blank=True, default=dict)

class Validation(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    validation_type = models.CharField(max_length=20, choices=FieldValidation.choices())
    validation_message = models.TextField()