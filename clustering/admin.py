from django.contrib import admin
from clustering.models import ClusteringModel


class ClusteringModelAdmin(admin.ModelAdmin):
    exclude = (' _data',)


admin.site.register(ClusteringModel, ClusteringModelAdmin)
