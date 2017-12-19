from django.contrib import admin
from classifier.models import ClassifierModel, ClassifiedDocument, ClassifiedExcerpt

# Register your models here.

admin.site.register(ClassifierModel)
admin.site.register(ClassifiedDocument)
admin.site.register(ClassifiedExcerpt)
