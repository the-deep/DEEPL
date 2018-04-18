from django.contrib import admin
from clustering.models import ClusteringModel, Doc2VecModel


class ClusteringModelAdmin(admin.ModelAdmin):
    exclude = (' _data',)


admin.site.register(ClusteringModel, ClusteringModelAdmin)
admin.site.register(Doc2VecModel)
