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
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes']*opt['weight'],
            })

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)


    def seats(self, options, sts):
        return self.identity(options)  # TODO


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
