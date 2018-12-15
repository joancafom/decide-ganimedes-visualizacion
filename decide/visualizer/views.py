from datetime import date
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods

from .render import Render
from .computations import age_distribution, mean


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
                census = mods.get('census', params={'voting_id': vid})
                voters = get_stub_info('voters', vid)
                no_voters = list(set(census['voters']) - set(voters))
                stats['census_size'] = len(census['voters'])
                stats['voters_turnout'] = get_stub_info('turnout', vid)
                if stats['census_size'] != 0:
                    stats['participation_ratio'] = round((stats['voters_turnout'] / stats['census_size']) * 100, 2)
                else:
                    stats['participation_ratio'] = 0

                sexes = get_stub_info('sexes', vid, census['voters'])
                print("sexes: " + str(sexes))

                voters_ages = get_stub_info('ages', vid, voters)
                no_voters_ages = get_stub_info('ages', vid, no_voters)
                (voters_age_dist, voters_age_mean) = age_distribution(voters_ages)
                stats['voters_age_dist'] = voters_age_dist
                stats['voters_age_mean'] = voters_age_mean
                stats['no_voters_age_mean'] = mean(no_voters_ages)

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
from store.models import Vote
from authentication.models import User

def get_stub_info(stub_info, vid, id_list = []):

    if stub_info == "turnout":
        return Vote.objects.filter(voting_id=vid).count()

    elif stub_info == 'sexes':
        voters = User.objects.filter(id__in=id_list).all()

        res = {

            User.SEX_OPTIONS[0][0] : 0,
            User.SEX_OPTIONS[1][0] : 0,
            User.SEX_OPTIONS[2][0] : 0

        }

        for v in voters:
            res[v.sex] = res[v.sex] + 1

        return res

    elif stub_info == 'ages':
        voters = User.objects.filter(id__in=id_list).all()

        res = {}
        today = date.today()

        for v in voters:
            years = today.year - v.birthdate.year - ((today.month, today.day) < (v.birthdate.month, v.birthdate.day))

            if years in res.keys():
                res[years] = res[years] + 1
            else:
                res[years] = 1

        return res
    elif stub_info == 'voters':
        voters = Vote.objects.filter(voting_id=vid).values_list('voter_id', flat=True).all()
        res = list(voters)

        return res
    else:
        return None

