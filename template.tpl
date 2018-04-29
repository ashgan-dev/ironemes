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
  <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <!-- Custom fonts for this template-->
  <link href="vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
  <!-- Custom styles for this template-->
  <link href="css/sb-admin.css" rel="stylesheet">
</head>

<body id='page-top'>
    <div class="container-fluid">
      <!-- Breadcrumbs-->
        <ol class="breadcrumb">
            <li class="breadcrumb-item">
                <a href="index.html">Index</a>
            </li>
            <li class="breadcrumb-item active">
                {{ json_file.stripext() | proper_name }}
            </li>
        </ol>
        <div class="row">
            <div class="col-12">
                <h6 class="page-header">
                    {{ nb_toots }} toots exprimés. <a href="{{ json_file.name }}" target="_blank">données brutes (format JSON)</a>
                </h6>
            </div>
        </div>
        {%- for i in toots: %}
        <div class="row">
            <div class="col-12">
                <!-- debut -->
                <div class="card mb-3">
                    <div class="card-header">
                        <h6>
                            <a href="{{ i['account']['url'] }}" target="_blank">
                                <img src="{{ i['account']['avatar'] }}" height="24" width="24">
                            </a>
                            <a href="{{ i['account']['url'] }}" target="_blank">
                                {% if i['account']['display_name'] != '': %}
                                    {{ i['account']['display_name'] }}
                                {% else: %}
                                    {{ i['account']['username'] }}
                                {% endif %}
                            </a>
                        </h6>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {{ i['content'] }}
                        </div>
                    </div>
                    <div class="card-footer small text-muted">
                        <span id="{{ i['id'] }}"></span>
                        Tooté le <a href="{{ i['url'] }}" target="_blank">{{ i['created_at']|datetimeformat }}</a> - favoris:
                        {% if i['favourites_count'] == 0: %}
                            {{ i['favourites_count'] }} <i class="fa fa-star-o"></i>
                        {% else: %}
                            {{ i['favourites_count'] }} <i class="fa fa-star"></i>
                        {% endif %}
                         - retoots: {{ i['reblogs_count'] }} <i class="fa fa-refresh"></i>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    <!-- /.container-fluid-->

    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fa fa-angle-up"></i>
    </a>
    <!-- Bootstrap core JavaScript-->
    <script src="vendor/jquery/jquery.min.js"></script>
    <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
    <!-- Core plugin JavaScript-->
    <script src="vendor/jquery-easing/jquery.easing.min.js"></script>
    <!-- Custom scripts for all pages-->
    <script src="js/sb-admin.min.js"></script>
</body>

</html>
