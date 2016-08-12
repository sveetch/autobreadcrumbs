from autobreadcrumbs.registry import breadcrumbs_registry
from django.utils.translation import ugettext_lazy


breadcrumbs_registry.update({
    'bar': ugettext_lazy('Bar'),
    'bar-ometer': ugettext_lazy("O'meter"),
})