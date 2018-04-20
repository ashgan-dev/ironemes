<!DOCTYPE html>
<html lang="fr">

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">
  <title>ironème</title>
  <!-- Bootstrap core CSS-->
  <link href="{{url_for('static', filename='vendor/bootstrap/css/bootstrap.min.css')}}" rel="stylesheet">
  <!-- Custom fonts for this template-->
  <link href="{{url_for('static', filename='vendor/font-awesome/css/font-awesome.min.css')}}" rel="stylesheet" type="text/css">
  <!-- Custom styles for this template-->
  <link href="{{url_for('static', filename='css/sb-admin.css')}}" rel="stylesheet">
</head>

<body id='page-top'>
    <div class="container-fluid">
        <ol class="breadcrumb">
        </ol>
        <div class="row">
            <div class="col-12">
                <!-- debut -->
                <div class="card mb-3">
                    <div class="card-header">
                        <h6>
                            {%- if chosen_instance == 0: -%}
                                {%- if requested_date != '': -%}
                                    {{ toots| count }} toots repertoriés sur toutes les instances le {{ requested_date | datetimeformat2 }}
                                {%- else -%}
                                    {{ toots| count }} toots repertoriés sur toutes les instances
                                {%- endif -%}
                            {%- else -%}
                                {%- if requested_date != '': -%}
                                    {{ toots| count }} toots repertoriés sur {{ chosen_instance }} le {{ requested_date | datetimeformat2 }}
                                {%- else -%}
                                    {{ toots| count }} toots repertoriés sur {{ chosen_instance }}
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
                                Date:
                                <input type="date" name="date">
                            </div>
                            <div class="form-group">
                                <button type="submit" class="btn btn-default">envoyer</button>
                            </div>
                        </form>
                        <small data-toggle="modal" data-target="#myModal"><i class="fa fa-support text-danger"></i> un peu d'aide?</small>
                        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                                    </div>
                                    <div class="modal-body">
                                        <p>Utilisez le formulaire pour filtrer les toots.</p>
                                        <p>quelques exemples:</p>
                                        <ul>
                                            <li>
                                                pour consulter tous les toots, choisissez "toutes" dans le choix d'instance, ne rentrez aucune date.
                                            </li>
                                            <li>
                                                pour consulter tous les toots d'une instance en particulier, sélectionnez la dans le menu déroulant sans rentrer de date.
                                            </li>
                                            <li>
                                                pour consulter tous les toots d'une date en particulier, rentrez la date choisie et sélectionner "toutes" dans le choix d'instance.
                                            </li>
                                            <li>
                                                je vous raconte même pas ce qu'il se passe quand on mixe la selection des dates et les instances ;)
                                            </li>
                                        </ul>
                                        après un (parfois long) moment, les toots choisis s'affichent.
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
        {% if toots: -%}
            {%- for i in toots: -%}
                <div class="row">
                    <div class="col-12">
                        <!-- debut -->
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

    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fa fa-angle-up"></i>
    </a>
    <!-- Bootstrap core JavaScript-->
    <script src="{{url_for('static', filename='vendor/jquery/jquery.min.js')}}"></script>
    <script src="{{url_for('static', filename='vendor/bootstrap/js/bootstrap.bundle.min.js')}}"></script>
    <!-- Core plugin JavaScript-->
    <script src="{{url_for('static', filename='vendor/jquery-easing/jquery.easing.min.js')}}"></script>
    <!-- Custom scripts for all pages-->
    <script src="{{url_for('static', filename='js/sb-admin.min.js')}}"></script>
</body>

</html>
