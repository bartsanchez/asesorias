# Cabecera necesaria para exportar a PDF.
import cStringIO as StringIO
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape

# Funcion para exportar a PDF.
def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()

	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result, encoding='UTF-8')
	if not pdf.err:
		final = HttpResponse(result.getvalue(), mimetype='application/pdf')
		final['Content-Disposition'] = 'attachment; filename=%(filename)s.pdf' % {'filename': context_dict.__getitem__('name')}
		return final
	return HttpResponse('Se produjeron errores. <pre>%s</pre>' % escape(html))
