from django.contrib import admin
from .models import AnswerQuery, Theme, Question

# Register your models here.
admin.site.register(Theme)
admin.site.register(AnswerQuery)
admin.site.register(Question)
