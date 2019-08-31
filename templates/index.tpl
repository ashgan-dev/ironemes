{%- extends "layout.tpl" -%}
{%- block activemenu1 -%}
class="dropdown active"
{%- endblock -%}
{%- block content -%}
<!-- Presentation -->
<div class="presentation-container">
    <div class="container">
        <div class="row">
            <div class="col-sm-12 wow fadeInLeftBig">
                <h1 class="to-animate text-center">#ironème</h1>
                <div class="col-md-10">
                    <p class="text-left">c'est un jeu de mots, mais reposant sur:</p>
                    <ul class="text-left">
                        <li class="left-border to-animate">certaines figures préférentiellement
                        <li class="left-border to-animate">une vocation poétique & imaginaire
                        <li class="left-border to-animate">une fréquence, une itération
                        <li class="left-border to-animate">une prétention de rupture discursive (c'est un anti discours)
                        <li class="left-border to-animate">un horizon de composition d'un autre monde, le monde d'à côté
                        <li class="left-border to-animate">une certaine retenue pour éviter les gros effets
                        <li class="left-border to-animate">une recherche d'économie linguistique (on réduit l'ironème à
                            sa plus brève expression)
                    </ul>
                    <p class="text-right">&ldquo;Ébauche, épure, esquisse poétique de subversion langagière.&rdquo;</p>
                    <p class="text-right"><a href=" https://framapiaf.org/@etienne_cdl/2831975" target="_blank">Etienne
                        C.</a></p>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="contact-us-container">
    <div class="container">
        <div class="row">
            <div class="col-sm-5 contact-address wow fadeInUp">
                <p>Utilisez le formulaire pour filtrer les toots.<br/>Quelques exemples:</p>
                <ul>
                    <li>
                        Pour consulter tous les toots, sélectionnez "toutes" dans le choix d'instance, ne saisissez
                        aucune date.
                    </li>
                    <li>
                        Pour consulter tous les toots d'une instance en particulier, sélectionnez la dans le menu
                        déroulant sans saisir de date.
                    </li>
                    <li>
                        Pour consulter tous les toots d'une date en particulier, saisissez la date choisie et
                        sélectionner "toutes" dans le choix d'instance.
                    </li>
                    <li>
                        Je vous raconte même pas ce qu'il se passe quand on mixe la sélection des dates avec le choix
                        des instances ;)
                    </li>
                </ul>
                <p>Après un (parfois long) moment, les toots choisis s'affichent.</p>
            </div>
            <div class="col-sm-7 contact-form wow fadeInRight">
                <form role="form" data-toggle="validator" action="{{ url_for('start_page') }}" method="POST">
                    <div class="form-group">
                        <label for="instance">Instance</label>
                        <select class="form-control" name="instance">
                            <option value="0">--Toutes--</option>
                            {% for h in instances_names: -%}
                            <option value="{{ h.id }}">{{ h.domain }}</option>
                            {% endfor -%}
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="date_debut">Du </label>
                        <input type="date" name="date_debut">
                    </div>
                    <div class="form-group">
                        <label for="date_fin">Au </label>
                        <input type="date" name="date_fin">
                    </div>
                    <button type="submit" class="btn">Envoyer</button>
                </form>
            </div>
        </div>
    </div>
</div>

<!-- Services -->
<div class="services-container">
    <div class="container">
        <p>
            {%- if chosen_instance == 0: -%}
            {%- if requested_date != '': -%}
            {{ toots| count }} toots répertoriés sur toutes les instances le {{ requested_date | datetimeformat2 }}
            {%- else -%}
            {{ toots| count }} toots répertoriés sur toutes les instances
            {%- endif -%}
            {%- else -%}
            {%- if requested_date != '': -%}
            {{ toots| count }} toots répertoriés sur {{ chosen_instance }} le {{ requested_date | datetimeformat2 }}
            {%- else -%}
            {{ toots| count }} toots répertoriés sur {{ chosen_instance }}
            {%- endif -%}
            {%- endif -%}
        </p>
        {% if toots: -%}
        <div class="row">
            {%- for i in toots: -%}
            <div class="col-sm-3">
                <div class="service wow fadeInUp">
                    <div class="service-icon"><img src="{{ i.account.avatar }}" class="img-circle" width="64"></div>
                    <h4>
                        {{ i.content | removetag }}
                    </h4>
                    <p>{{ i.account.username }}, le <a href="{{ i.url }}" target="_blank">{{ i.creation_date |
                        datetimeformat }}</a></p>
                </div>
            </div>
            {%- endfor -%}
        </div>
        {%- else -%}
        <div class="row">
            Aucun toot trouvé 😞
        </div>
        {%- endif -%}
    </div>
</div>
{%- endblock -%}