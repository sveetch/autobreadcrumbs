from autobreadcrumbs.registry import breadcrumbs_registry
from django.utils.translation import ugettext_lazy


breadcrumbs_registry.update({
    'foo:index': ugettext_lazy('Foo'),
    'foo:date': ugettext_lazy('Year month'),
    'foo:pika': ugettext_lazy('Pika'),
    'foo:pika-chu': ugettext_lazy('Chu'),
    'foo:subfoo:index': ugettext_lazy('Sub'),
    'foo:subfoo:plop': ugettext_lazy('Plop'),
    'foo:slug': ugettext_lazy('Sluggy'),
    'foo:invisible-chu': ugettext_lazy('Chu'),
})
