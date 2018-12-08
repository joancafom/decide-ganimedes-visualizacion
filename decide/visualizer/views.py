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

            else:
                
                #Votación terminada
                self.template_name = "visualizer/ended.html"

        except:
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
