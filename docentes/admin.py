from django.contrib import admin

from docentes.models import Actividad, Comentario, Favorito, Planeacion, Rating

# Register your models here.

class PlaneacionAdmin(admin.ModelAdmin):
    list_display= ('pk','titulo','fecha_de_inicio','fecha_de_finalizacion')
    list_filter=('titulo','grado')
    search_fields=['titulo']

class ActividadesAdmin(admin.ModelAdmin):
   list_display=('titulo','fecha_de_inicio') 
   search_fields=['titulo']




class ComentarioAdmin(admin.ModelAdmin):
    list_display=('pk','comentario')

admin.site.register(Planeacion,PlaneacionAdmin)
admin.site.register(Actividad,ActividadesAdmin)
admin.site.register(Comentario,ComentarioAdmin)
admin.site.register(Rating)
admin.site.register(Favorito)
