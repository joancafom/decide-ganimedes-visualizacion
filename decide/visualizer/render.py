from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import csv


class Render:

    def render_pdf(path, params):
        plantilla = get_template(path)
        html = plantilla.render(params)

        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        
        else:
            return HttpResponse("Error renderizando el archivo PDF", status=400)

    def render_csv(path, params):
        response = HttpResponse(content_type='text/csv', charset='UTF-8')
        response['Content-Disposition'] = 'attachment; filename="resultados.csv"'

        votacion = params['voting']
        writer = csv.writer(response)

        writer.writerow([votacion['name'], votacion['question']['desc']])

        if path == 'visualizer/ended_export.html':
            
            writer.writerow(['Opción', 'Número de votos'])
            resultados = params['voting']['postproc']

            for r in resultados:
                writer.writerow([r['option'], r['votes']])
        
        elif path == 'visualizer/ongoing_export.html':

            writer.writerow(['Estadísticas'])

        return response