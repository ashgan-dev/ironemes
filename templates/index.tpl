{%- extends "layout.tpl" -%}
{%- block breadcrumb -%}
        <ol class="breadcrumb">
            <li class="breadcrumb-item active">
              Index
            </li>
            <li class="breadcrumb-item">
                <a href={{ url_for('search') }}>Recherche</a>
            </li>
        </ol>
{%- endblock -%}
{%- block content -%}
                <div class="card mb-3">
                    <div class="card-header">
                        <h6>
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
                        </h6>
                    </div>
                    <div class="card-body">
                        <form role="form" data-toggle="validator" action="{{ url_for('start_page') }}" method="POST">
                            <div class="form-group">
                                Instance:
                                <select class="form-control" name="instance">
                                    <option value="0">--Toutes--</option>
                                    {% for h in instances_names: -%}
                                        <option value="{{ h.id }}">{{ h.domain }}</option>
                                    {% endfor -%}
                                </select>
                            </div>
                            <div class="form-group">
                                Du:
                                <input type="date" name="date_debut">
                            </div>
                            <div class="form-group">
                                Au:
                                <input type="date" name="date_fin">
                            </div>
                            <div class="form-group">
                                <button type="submit" class="btn btn-default">envoyer</button>
                            </div>
                        </form>
                        <small data-toggle="modal" data-target="#myModal">
                            <i class="fa fa-support text-danger"></i> un peu d'aide?
                        </small>
                        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                    </div>
                                    <div class="modal-body">
                                        <p>Utilisez le formulaire pour filtrer les toots.<br />Quelques exemples:</p>
                                        <ul>
                                            <li>
                                                Pour consulter tous les toots, sélectionnez "toutes" dans le choix d'instance, ne saisissez aucune date.
                                            </li>
                                            <li>
                                                Pour consulter tous les toots d'une instance en particulier, sélectionnez la dans le menu déroulant sans saisir de date.
                                            </li>
                                            <li>
                                                Pour consulter tous les toots d'une date en particulier, saisissez la date choisie et sélectionner "toutes" dans le choix d'instance.
                                            </li>
                                            <li>
                                                Je vous raconte même pas ce qu'il se passe quand on mixe la sélection des dates avec le choix des instances ;)
                                            </li>
                                        </ul>
                                        <p>Après un (parfois long) moment, les toots choisis s'affichent.</p>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% if get == 1: -%}
        <div class="alert alert-warning alert-dismissable col-6 offset-3">
            <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
            <p class="text-center">Voici les 30 derniers ironèmes.<br />Pour en voir plus, utilisez le formulaire au dessus ou utilisez la recherche.</p>
        </div>
        {% endif -%}
        {% if toots: -%}
            {%- for i in toots: -%}
                <div class="row">
                    <div class="col-12">
                        <div class="card mb-3">
                            <div class="card-header">
                                <h6>
                                    <a href="{{ i.account.url }}" target="_blank">
                                        <img src="{{ i.account.avatar }}" height="24" width="24">
                                    </a>
                                    <a href="{{ i.account.url }}" target="_blank">
                                        {%- if i.account.display_name != '': -%}
                                            {{ i.account.display_name }}
                                        {%- else: -%}
                                            {{ i.account.username }}
                                        {%- endif -%}
                                    </a>
                                </h6>
                            </div>
                            <div class="card-body">
                                <div class="table-responsive">
                                    {{ i.content }}
                                </div>
                            </div>
                            <div class="card-footer small text-muted">
                                <span id="{{ i.id }}"></span>
                                Tooté le <a href="{{ i.url }}" target="_blank">{{ i.creation_date | datetimeformat }}</a> - favoris:
                                {%- if i.favourite_count == 0: -%}
                                    {{ i.favourite_count }} <i class="fa fa-star-o"></i>
                                {%- else: -%}
                                    {{ i.favourite_count }} <i class="fa fa-star"></i>
                                {%- endif -%}
                                 - retoots: {{ i.reblog_count }} <i class="fa fa-refresh"></i>
                            </div>
                        </div>
                    </div>
                </div>
            {%- endfor -%}
        {%- else -%}
            <div class="row">
                <div class="col-12">
                    Aucun toot trouvé 😞
                </div>
            </div>
        {%- endif -%}
    </div>
{%- endblock -%}