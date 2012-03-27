Introduction
============

AutoBreadcrumbs est un module permettant le calcul automatique du chemin d'accès d'une page 
(*ou chemin de parcours* ) dans les urls. Par exemple : ::

  Accueil > Mon appli > Ma vue

Chaque élément est une miette (*breadcrumb*) du chemin complet contenant un lien pour pouvoir se déplacer 
rapidement. Le chemins d'accès est une méthode d'ergonomie pour l'utilisateur et lui faciliter sa 
localisation dans un site.

Installation
============

Il suffit de modifier les *settings* de votre projet en rajoutant une ligne pour 
inscrire l'application dans votre projet : ::

    INSTALLED_APPS = (
        ...
        'autobreadcrumbs',
        ...
    )

Puis inscrire aussi son *context processor* : ::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'autobreadcrumbs.context_processors.AutoBreadcrumbsContext',
        ...
    )

Utilisation
===========

Pour fonctionner correctement dans votre projet il vous faudra que toute les urls soit nommées 
correctement (avec leur attribut ``name``).

Mais aussi une solide organisation de la map des urls du site car des ressources différentes 
passant par une même url peuvent provoquer des problèmes. De même pour des parties de 
l'url qui ne sont pas disponibles pour tout les utilisateurs (à cause d'une restriction 
d'accès ou autre) qui s'afficheront dans le chemin d'accès alors qu'elles ne le devraient 
pas (si par exemple n'a pas les permissions pour accéder à une ressource du chemin).

Registre des vues
********************

Inscription
-----------

Le *context processor* effectue une recherche à partir de l'url en cours qu'il découpe en segments 
qui produiront les miettes du chemin.

Pour qu'il reconnaisse une ressource comme une miette de chemin à afficher, votre ressource doit 
posséder un attribut statique ``title`` (*string*) ou ``titles`` (*dict*) définit sur les 
méthodes de vues (*views*) (facilité avec l'usage du décorateur). 

Une entrée dans ``settings.AUTOBREADCRUMBS_TITLES`` sous la forme d'un tuple ``(url-name, title)`` 
fonctionne aussi.

Lors de la recherche par le *context processor*, chaque ressource est classée par le nom d'url qui la 
définit et il les considèrent chacune dans l'ordre suivant :

#. La ressource a t'elle une entrée ``settings.AUTOBREADCRUMBS_TITLES`` si oui l'utilise et passe à la 
   ressource suivante;
#. La ressource a t'elle un attribut ``crumb_titles`` si oui tente d'y récupérer une entrée pour son nom 
   d'url avant de passer à la ressource suivante;
#. La ressource a t'elle un attribut ``crumb_title`` si oui l'utilise et passe à la ressource suivante;
#. Si aucune des conditions suivantes n'ont été remplies, ignore la ressource et passe à la suivante;

L'emplacement du titre peut être un tuple contenant le titre plus une méthode (*function*) de contrôle d'accès 
prenant le *request* en unique argument et renvoyant *True* pour accepter l'entrée ou *False* pour ignorer la 
ressource.

.. NOTE:: Les *Class base views* de Django 1.3.x sont actuellement ignorés par autobreadcrumbs, et les 
          décorateurs ne fonctionnent pas dessus. Il vous faudra les inscrire dans 
          ``settings.AUTOBREADCRUMBS_TITLES``.

Exclusion
---------

On peut aussi utiliser ``@autobreadcrumb_hide`` pour exclure une vue des miettes, de 
même indiquer ``None`` en valeur d'un titre l'exclut aussi des miettes, cela fonctionne aussi lors 
de la déclaration dans ``settings.AUTOBREADCRUMBS_TITLES``.

Exemples
--------

Exemple simple pour une vue : ::

    @autobreadcrumb_add(u"Mon zuper zindex")
    def index(request):
        ....

Avec un titre différent pour plusieurs urls qui utilisent la même vue : ::

    @autobreadcrumb_add({
        "pages-index1": u"Mon zuper zindex",
        "pages-index2": u"My upper index",
    })
    def index(request):
        ....

.. autobreadcrumbs_titles

Dans les settings : ::

    AUTOBREADCRUMBS_TITLES = {
        "pages-index1": u"Mon zuper zindex",
        "pages-index2": u"My upper index",
    }

Templates
*********

Dans vos templates disposant du context global, deux variables supplémentaires 
(`autobreadcrumbs_elements`_ et `autobreadcrumbs_current`_) seront insérées pour chaque page.

autobreadcrumbs_elements
------------------------

Le chemin d'accès sera disponible dans cette variable du contexte de template et contiendra une liste 
d'instances de ``BreadcrumbRessource`` pour chaque miette du chemin. Chaque instance de ``BreadcrumbRessource`` 
contient les attributs suivants :

* ``path`` : le chemin relatif de l'url qui mène à la ressource;
* ``name`` : nom de l'url de la ressource;
* ``title`` : titre à afficher pour la ressource dans le chemin d'accès;
* ``view_args`` : liste d'arguments passés à l'url de la ressource;
* ``view_kwargs`` : liste des arguments nommés passés à l'url de la ressource;

autobreadcrumbs_current
-----------------------

Cette variable contiendra l'instance ``BreadcrumbRessource`` de la ressource en cours, elle est identique au dernier 
élément contenu dans `autobreadcrumbs_elements`_.

Template tags
*************

Pour pouvoir les utiliser il faut les importer dans votre templates via la librairie : ::

  {% load autobreadcrumb %}

current_title_from_breadcrumbs
  Retourne simplement le titre de la ressource en cours.
autobreadcrumbs_tag
  Génère le HTML complet du chemin d'accès à partir du templates ``autobreadcrumbs_tag.html`` déjà fournit. Vous pouvez 
  le supplanter en créant simplement le votre à la racine de vos templates.
autobreadcrumbs_links
  Génère directement le HTML du chemin d'accès en utilisant ``settings.AUTOBREADCRUMBS_HTML_LINK`` comme chaîne de 
  template (elle doit comporter les emplacements de variables nommés correspondant aux attributs disponible dans 
  ``BreadcrumbRessource``) et ``settings.AUTOBREADCRUMBS_HTML_SEPARATOR`` pour le séparateur entre chaque miette.
currentwalkthroughto
  Renvoi le contenu donné entre les balises si la ressource courante passe par la ressource ciblée 
  (par son urlname). Requiert en argument le nom d'url de la ressource ciblée.
      
  Exemple : ::
  
      {% currentwalkthroughto 'index' %}Ma page courante passe par l'index{% endcurrentwalkthroughto %}
  
  Si le test échoue (aka la ressource ne passe pas par un chemin au nom d'url ciblé), 
  le contenu entre les balises n'est pas renvoyé mais une chaine vide à la place.
