from autobreadcrumbs import site
from django.utils.translation import ugettext_lazy


site.update({
    'bar': ugettext_lazy('Bar'),
    'bar-ometer': ugettext_lazy("O'meter"),
})
