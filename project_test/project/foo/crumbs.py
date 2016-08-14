from autobreadcrumbs.registry import breadcrumbs_registry
from django.utils.translation import ugettext_lazy


breadcrumbs_registry.update({
    'foo:index': 'Foo',
    'foo:date': 'Year month',
    'foo:pika': 'Pika',
    'foo:pika-chu': ugettext_lazy('Chu'),
    'foo:subfoo:index': ugettext_lazy('Sub'),
    'foo:subfoo:plop': ugettext_lazy('Plop'),
    'foo:slug': ugettext_lazy('Sluggy'),
    'foo:invisible-chu': 'Chu',
    'foo:controlled-true': (ugettext_lazy('Controlled true'), lambda x,y: True),
    'foo:controlled-true-endpoint': 'Control Yep',
    'foo:controlled-false': (ugettext_lazy('Controlled false'), lambda x,y: False),
    'foo:controlled-false-endpoint': 'Control Nope',
})
