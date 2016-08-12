from autobreadcrumbs.registry import breadcrumbs_registry
from django.utils.translation import ugettext_lazy


breadcrumbs_registry.update({
    'foo:index': ugettext_lazy('Foo'),
    'foo:pika': ugettext_lazy('Pika'),
    'foo:pika-chu': ugettext_lazy('Chu'),
    'foo:subfoo:index': ugettext_lazy('Sub'),
    'foo:subfoo:plop': ugettext_lazy('Mip'),
    'foo:slug': ugettext_lazy('Sluggy'),
    'foo:year-month': ugettext_lazy('Year month'),
    'foo:invisible': ugettext_lazy('Invisible'),
    'foo:invisible-chu': ugettext_lazy('Chu'),
})
