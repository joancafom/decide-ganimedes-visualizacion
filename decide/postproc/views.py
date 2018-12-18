from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PostProcType


class PostProcView(APIView):

    def identity(self, options):
        out = []
        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            })
        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def weight(self, options):
        return self.identity(options)  # TODO

    def seats(self, options, sts):

        def calcular_cocientes(escanyos, votos_por_partido):
            cocientes = []
            cont = 0
            for i in range(len(votos_por_partido)):
                add = int(votos_por_partido[cont] / (escanyos[cont] + 1))
                cocientes.append(add)
                cont += 1
            return cocientes

        def obtener_votos(options):
            votos = []
            for opt in options:
                votos.append(opt['votes'])
            return votos

        def atribuir_postproc(options):
            out = []
            for opt in options:
                out.append({
                    **opt,
                    'postproc': 0,
                })
            return out

        # Cociente (S) = V/(s+1)   V: Nº total de votos de ese partido. s: Nº de escaños conseguidos, inicialmente es cero.
        escanyos_por_partido = [0] * len(options)
        votos_por_partido = obtener_votos(options)
        opt_con_escanos = atribuir_postproc(options)

        for i in range(sts):
            cocientes = calcular_cocientes(escanyos_por_partido, votos_por_partido)
            indice_ganador = cocientes.index(max(cocientes))
            escanyos_por_partido[indice_ganador] += 1
            partido = opt_con_escanos[indice_ganador]
            partido["postproc"] += 1
        opt_con_escanos.sort(key=lambda x: -x['postproc'])
        return Response(opt_con_escanos)

    def team(self, options):

        def atribuir_votos():
            votes_team = [0] * n_teams
            for opt in options:
                votes_team[opt['team']] = votes_team[opt['team']] + opt['votes']
            return votes_team

        def obtener_n_equipos():
            n_teams = []
            for opt in options:
                n_teams.append(opt['team'])
            return len(set(n_teams))

        def lista_ordenada(lista_votos, votos_ordenados):
            sorted_teams = []
            for i in votos_ordenados:
                listax = []
                ind = lista_votos.index(i)
                for opt in options:
                    if opt['team'] == ind:
                        listax.append(opt)
                listax.sort(key = lambda x: -x['votes'])
                for l in listax:
                    sorted_teams.append(l)
            return sorted_teams

        n_teams = obtener_n_equipos()
        votes_per_team = atribuir_votos()
        equipos_mayor_a_menor = sorted(votes_per_team, key=int, reverse = True)
        equipos = lista_ordenada(votes_per_team, equipos_mayor_a_menor)
        return Response(equipos)

    def parity(self, options):
        return self.identity(options)  # TODO

    def post(self, request):
        t = request.data.get('type', PostProcType.IDENTITY)
        opts = request.data.get('options', [])
        sts = request.data.get('seats', -1)

        if t == PostProcType.IDENTITY:
            return self.identity(opts)
        elif t == PostProcType.WEIGHT:
            return self.weight(opts)
        elif t == PostProcType.SEATS:
            return self.seats(opts, sts)
        elif t == PostProcType.PARITY:
            return self.parity(opts)
        elif t == PostProcType.TEAM:
            return self.team(opts)

        return self.identity(opts)




