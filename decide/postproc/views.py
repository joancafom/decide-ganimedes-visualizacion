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

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', PostProcType.IDENTITY)
        opts = request.data.get('options', [])

        if t == PostProcType.IDENTITY:
            return self.identity(opts)

        return Response({})
