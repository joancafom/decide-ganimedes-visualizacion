from rest_framework.views import APIView
from rest_framework.response import Response

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
        def calcular_cocientes(self, escanyos, votos_por_partido):
            cocientes = []
            for i in len(votos_por_partido):
                cocientes.append(votos_por_partido[1] / (escanyos[i] + 1))

            return cocientes

        def obtener_votos(options):
            votos = []
            for opt in options:
                votos.append({
                    **opt,
                    'postproc': opt['votes'],
                })
            return votos

        # Cociente (S) = V/(s+1)   V: Nº total de votos de ese partido. s: Nº de escaños conseguidos, inicialmente es cero.
        escanyos_por_partido = [0] * len(options)
        votos_para_escaños = [0] * len(options)
        votos_por_partido = obtener_votos(options)

        for i in range(sts):
            cocientes = calcular_cocientes(sts, votos_por_partido)

            for i in range(len(votos_por_partido)):
                votos_para_escaños[i] = cocientes[i]

            partido_ganador = votos_por_partido.index(max(votos_para_escaños))
            escanyos_por_partido[partido_ganador] += 1

        return escanyos_por_partido



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

        return Response({})




