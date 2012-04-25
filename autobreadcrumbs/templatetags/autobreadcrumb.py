# -*- coding: utf-8 -*-
"""
Template tags

They requires that the context process is enabled
"""
from django import template
from django.utils.safestring import mark_safe

from autobreadcrumbs.settings_local import AUTOBREADCRUMBS_HTML_LINK, AUTOBREADCRUMBS_HTML_SEPARATOR

register = template.Library()

@register.tag(name="currentwalkthroughto")
def do_current_walkthrough(parser, token):
    """
    Lecture de préparation du Tag *currentwalkthroughto*
    
    Renvoi le contenu donné entre les balises si la ressource courante passe par la 
    ressource ciblée (par son urlname).
    
    Arguments :
    
    urlname
        Nom d'url de la ressource ciblée
        
    Exemple d'utilisation par une instance Insert : ::
    
        {% currentwalkthroughto 'index' %}Ma page courante passe par l'index{% endcurrentwalkthroughto %}
    
    Si le test échoue (aka la ressource ne passe pas par un chemin au nom d'url ciblé), 
    le contenu entre les balises n'est pas renvoyé mais une chaine vide à la place.
    
    :type parser: object ``django.template.Parser``
    :param parser: Objet du parser de template.
    
    :type token: object ``django.template.Token``
    :param token: Objet de la chaîne découpée du tag capturé dans le template.
    
    :rtype: object ``CurrentWalkthroughRender``
    :return: L'objet du générateur de rendu du tag.
    """
    nodelist = parser.parse(('endcurrentwalkthroughto',))
    parser.delete_first_token()
    
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError, "You need to specify an url name to compare with"
    else:
        return CurrentWalkthroughRender(nodelist, *args[1:])

class CurrentWalkthroughRender(template.Node):
    def __init__(self, nodelist, urlname):
        self.nodelist = nodelist
        self.urlname = urlname
        
    def render(self, context):
        output = self.nodelist.render(context)
        urlname = template.resolve_variable(self.urlname, context)
        if 'autobreadcrumbs_elements' in context:
            if len(filter(lambda x: (x.name == urlname), context['autobreadcrumbs_elements'])):
                return output
        return ''

@register.simple_tag(takes_context=True)
def current_title_from_breadcrumbs(context):
    """
    Renvoi le titre de l'élément courant
    """
    title = ''
    if 'autobreadcrumbs_current' in context and context['autobreadcrumbs_current']:
        tpl = template.Template(context['autobreadcrumbs_current'].title)
        title = tpl.render(template.Context(context))
    return title

@register.inclusion_tag('autobreadcrumbs_tag.html', takes_context=True)
def autobreadcrumbs_tag(context):
    """
    Génère la liste des miettes du chemin d'accès à partir d'un 
    template "autobreadcrumbs_tag.html" à la racine de "templates/"
    """
    if 'autobreadcrumbs_elements' in context:
        elements = []
        for item in context['autobreadcrumbs_elements']:
            tpl = template.Template(item.title)
            title = tpl.render(template.Context(context))
            
            elements.append(dict(zip(
                ('url','title','name','view_args','view_kwargs'), 
                (item.path,title,item.name,item.view_args,item.view_kwargs)
            )))
        return {'elements': elements}
    return {}

@register.simple_tag(takes_context=True)
def autobreadcrumbs_links(context):
    """
    Génère directement le html de la liste des miettes du chemin d'accès
    """
    if 'autobreadcrumbs_elements' in context:
        elements = []
        for item in context['autobreadcrumbs_elements']:
            tpl = template.Template(item.title)
            title = tpl.render(template.Context(context))
            
            elements.append(AUTOBREADCRUMBS_HTML_LINK.format(link=item.path, title=title))
        return mark_safe(AUTOBREADCRUMBS_HTML_SEPARATOR.join(elements))
    return ''
autobreadcrumbs_links.is_safe = True
