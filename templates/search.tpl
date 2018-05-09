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
            <li class="breadcrumb-item">
              <a href={{ url_for('start_page') }}>Index</a>
            </li>
            <li class="breadcrumb-item active">
                Recherche
            </li>
        </ol>
        <div class="row">
            <div class="col-12">
                <!-- debut -->
                <div class="card mb-3">
                    <div class="card-header">
                        <h6>
                            {%- if toots: -%}
                                    {{ toots| count }} toots contenant le terme "{{ requested_string }}"
                            {%- else -%}
                                rechercher un ironème
                            {%- endif -%}
                        </h6>
                    </div>
                    <div class="card-body">
                        <form role="form" data-toggle="validator" action="{{ url_for('search') }}" method="POST">
                            <div class="form-group">
                                Entrez votre recherche:
                                <input type="text" name="search">
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
                                        <p>
                                            Utilisez le formulaire pour chercher un mot, une expression ou un groupe de lettre.<br />
                                            Si un ou plusieurs toot contient votre expression, ils s'afficheront.
                                            <br />Pour chercher un user en particulier, cherchez @username.
                                        </p>
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
        {%- endif -%}
    </div>
    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fa fa-angle-up"></i>
    </a>
    <footer>
        <div class="text-left">
            <small>
                <a href="https://github.com/ashgan-dev/ironemes" target="_blank">voir sur Github</a>
            </small>
        </div>
    </footer>
    <!-- Bootstrap core JavaScript-->
    <script src="{{url_for('static', filename='vendor/jquery/jquery.min.js')}}"></script>
    <script src="{{url_for('static', filename='vendor/bootstrap/js/bootstrap.bundle.min.js')}}"></script>
    <!-- Core plugin JavaScript-->
    <script src="{{url_for('static', filename='vendor/jquery-easing/jquery.easing.min.js')}}"></script>
    <!-- Custom scripts for all pages-->
    <script src="{{url_for('static', filename='js/sb-admin.min.js')}}"></script>
</body>

</html>
