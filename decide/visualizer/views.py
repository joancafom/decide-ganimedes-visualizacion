from datetime import date
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404, HttpResponseBadRequest
from django.core.cache import cache

from base import mods
from django import template

register = template.Library()

from .render import Render
from .computations import age_distribution, mean, get_sexes_participation, get_sexes_percentages


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

                stats = get_statistics(vid)
                
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

                stats = get_statistics(vid)

                #Añadimos el prefijo stats_
                stats_formatted = {}
                for e,v in stats.items():
                    stats_formatted['stats_' + str(e)] = v

                stats_formatted['voting'] = voting

                return Render.render_pdf(plantilla, stats_formatted)

            elif r[0]['start_date'] is not None and r[0]['end_date'] is not None:
                
                #Votación terminada
                plantilla = "visualizer/ended_export.html"

                return Render.render_pdf(plantilla, {'voting':voting})
        
        except Exception as e:
            print(str(e))
            raise Http404

        return None

        

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

                stats = get_statistics(vid)

                #Añadimos el prefijo stats_
                stats_formatted = {}
                for e,v in stats.items():
                    stats_formatted['stats_' + str(e)] = v

                stats_formatted['voting'] = voting

                return Render.render_csv(plantilla, stats_formatted)

            elif r[0]['start_date'] is not None and r[0]['end_date'] is not None:
                
                #Votación terminada
                plantilla = "visualizer/ended_export.html"

                return Render.render_csv(plantilla, {'voting':voting})
        
        except Exception as e:
            print(str(e))
            raise Http404

        return None

class VisualizerJson(TemplateView):

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        vid = kwargs.get('voting_id', 0)

        try:
            r = mods.get('voting', params={'id': vid})
            voting = r[0]

            # Identificamos el estado de la votación
            if r[0]['start_date'] is None:
                
                return HttpResponseBadRequest()

            elif r[0]['end_date'] is None:

                # Votación en proceso
                voting_status = "ongoing"

                #Obtenemos las estadísticas de la votación
                stats = get_statistics(vid)
                stats['voting'] = voting

                return Render.render_json(voting_status, stats)

            elif r[0]['start_date'] is not None and r[0]['end_date'] is not None:
                
                # Impedir la obtención de resultados de votaciones que no han pasado
                # por tally

                if voting['postproc'] is None:
                    return HttpResponseBadRequest()

                #Votación terminada
                voting_status = 'ended'

                return Render.render_json(voting_status, {'voting':voting})

        except Exception as e:
            print(str(e))
            raise Http404

        return context

STATS_NAMES = [
    'census_size',
    'voters_turnout',
    'participation_ratio',
    'voters_age_dist',
    'voters_age_mean',
    'no_voters_age_mean',
    'women_participation',
    'men_participation',
    'nonbinary_participation',
    'women_percentage',
    'men_percentage',
    'nonbinary_percentage'
]

CACHE_TIMEOUT = 20

def get_statistics(vid, counter=0):
    """ Obtiene o calcula las estadísticas dada una votación vid:int
    como un diccionario con el nombre de la estadística como 
    clave y su dato como valor."""

    #Estadísticas de la votación
    stats = {}

    #Comprobamos si las estadísticas están en caché
    cached_raw_stats = cache.get(str(vid))

    if(cached_raw_stats is None):
        # No existen las estadísticas en caché

        #Estadísticas básicas: tamaño del censo, personas que han
        #votado y participación
        census = mods.get('census', params={'voting_id': vid})
        voters_raw = mods.get('store',entry_point='/users/voting/{}/'.format(vid) )
        voters_id = [v['id'] for v in voters_raw]
        no_voters = list(set(census['voters']) - set(voters_id))

        stats['census_size'] = len(census['voters'])
        stats['voters_turnout'] = len(voters_id)
        if stats['census_size'] != 0:
            stats['participation_ratio'] = round((stats['voters_turnout'] / stats['census_size']) * 100, 2)
        else:
            stats['participation_ratio'] = 0

        voters_ages = get_stub_info('ages', vid, voters_id)
        no_voters_ages = get_stub_info('ages', vid, no_voters)
        (voters_age_dist, voters_age_mean) = age_distribution(voters_ages)
        stats['voters_age_dist'] = voters_age_dist
        stats['voters_age_mean'] = voters_age_mean
        stats['no_voters_age_mean'] = mean(no_voters_ages)

        #Estadísticas avanzadas de votación II
        votantes =  []
        for v_id in voters_id:
            user = User.objects.filter(id = v_id).all()
            votantes.append(user)
        sexes_total = get_stub_info('sexes', vid, census['voters'])
        sexes_empty = {
            User.SEX_OPTIONS[0][0] : 0,
            User.SEX_OPTIONS[1][0] : 0,
            User.SEX_OPTIONS[2][0] : 0
        }

        sexes_participation = get_sexes_participation(votantes, sexes_empty)

        stats['women_participation'] = sexes_participation['W']
        stats['men_participation'] = sexes_participation['M']
        stats['nonbinary_participation'] = sexes_participation['N']

        sexes_percentages = get_sexes_percentages(sexes_participation, sexes_total, sexes_empty)

        stats['women_percentage'] = sexes_percentages['W']
        stats['men_percentage'] = sexes_percentages['M']
        stats['nonbinary_percentage'] = sexes_percentages['N']

        #Cambiamos los valores None por 'None' (str)
        #para poder guardarlos en caché sin problemas
        processed_stats = { k: v if v is not None else 'None' for k,v in stats.items()}

        cache.set(str(vid), processed_stats, timeout=CACHE_TIMEOUT)

    else:
        #Las estadísticas deberían estar en caché...

        #Cambiamos los valores 'None' por None (NoneType)
        stats = { k: v if v != 'None' else None for k,v in cached_raw_stats.items()}

        #Si no se encuentran todas, la caché está corrupta y debemos volver
        #a calcularlas
        if stats is None or len(stats) != len(STATS_NAMES):

            #Borramos el registro actual para proceder al nuevo cálculo
            cache.delete(str(vid))
            get_statistics(vid)
    
    return stats

# Stub Methods
# Simulamos la llamada a otros módulos mientras estos implementan sus cambios
from authentication.models import User

def get_stub_info(stub_info, vid, id_list = []):

    if stub_info == 'sexes':
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
    else:
        return None

