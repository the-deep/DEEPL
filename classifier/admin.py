from django.contrib import admin
from classifier.models import (
    ClassifierModel,
    ClassifiedDocument,
    ClassifiedExcerpt,
    Recommendation
)


class ClassifierModelAdmin(admin.ModelAdmin):
    exclude = ('_data',)


admin.site.register(ClassifierModel, ClassifierModelAdmin)
admin.site.register(ClassifiedDocument)
admin.site.register(ClassifiedExcerpt)
admin.site.register(Recommendation)



