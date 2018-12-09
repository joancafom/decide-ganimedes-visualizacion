from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods

from .render import Render


class VisualizerView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            context['voting'] = r[0]

            # Elegimos la plantilla a renderizar en base al estado
            # de la votación
            if r[0]['start_date'] is None:
                
                # Votación no comenzada
                self.template_name = "visualizer/not_started.html"

            elif r[0]['end_date'] is None:

                # Votación en proceso
                self.template_name = "visualizer/ongoing.html"

                #Obtenemos las estadísticas de la votación
                stats = {}

                #Estadísticas básicas: tamaño del censo, personas que han
                #votado y participación
                stats['census_size'] = get_stub_info('census_size', vid)
                stats['voters_turnout'] = get_stub_info('turnout', vid)
                stats['participation_ratio'] = round((stats['voters_turnout'] / stats['census_size']) * 100, 2)

                #Añadimos las estadísticas al contexto
                for e,v in stats.items():
                    context['stats_' + str(e)] = v

            else:
                
                #Votación terminada
                self.template_name = "visualizer/ended.html"

        except Exception as e:
            print(str(e))
            raise Http404

        return context

class VisualizerPdf(TemplateView):

    def get(self, request, **kwargs):
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            voting = r[0]

            # Elegimos la plantilla a renderizar en base al estado
            # de la votación

            if r[0]['end_date'] is None:

                # Votación en proceso
                plantilla = "visualizer/ongoing_export.html"

            elif r[0]['start_date'] is not None and r[0]['end_date'] is not None:
                
                #Votación terminada
                plantilla = "visualizer/ended_export.html"
        
        except:
            raise Http404

        return Render.render_pdf(plantilla, {'voting':voting})

class VisualizerCsv(TemplateView):

    def get(self, request, **kwargs):
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            voting = r[0]

            # Elegimos la plantilla a renderizar en base al estado
            # de la votación

            if r[0]['end_date'] is None:

                # Votación en proceso
                plantilla = "visualizer/ongoing_export.html"

            elif r[0]['start_date'] is not None and r[0]['end_date'] is not None:
                
                #Votación terminada
                plantilla = "visualizer/ended_export.html"
        
        except:
            raise Http404

        return Render.render_csv(plantilla, {'voting':voting})

# Stub Methods
# Simulamos la llamada a otros módulos mientras estos implementan sus cambios
from census.models import Census
from store.models import Vote
def get_stub_info(stub_info, vid):

    if stub_info == "census_size":
        return Census.objects.filter(voting_id=vid).count()
    elif stub_info == "turnout":
        return Vote.objects.filter(voting_id=vid).count()
    else:
        return None

