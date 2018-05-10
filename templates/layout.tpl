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
        <!-- Collectif Pépite designed the original image for theses favicons -->
        <link rel="apple-touch-icon" sizes="57x57" href="{{url_for('static', filename='icons/apple-icon-57x57.png')}}">
        <link rel="apple-touch-icon" sizes="60x60" href="{{url_for('static', filename='icons/apple-icon-60x60.png')}}">
        <link rel="apple-touch-icon" sizes="72x72" href="{{url_for('static', filename='icons/apple-icon-72x72.png')}}">
        <link rel="apple-touch-icon" sizes="76x76" href="{{url_for('static', filename='icons/apple-icon-76x76.png')}}">
        <link rel="apple-touch-icon" sizes="114x114" href="{{url_for('static', filename='icons/apple-icon-114x114.png')}}">
        <link rel="apple-touch-icon" sizes="120x120" href="{{url_for('static', filename='icons/apple-icon-120x120.png')}}">
        <link rel="apple-touch-icon" sizes="144x144" href="{{url_for('static', filename='icons/apple-icon-144x144.png')}}">
        <link rel="apple-touch-icon" sizes="152x152" href="{{url_for('static', filename='icons/apple-icon-152x152.png')}}">
        <link rel="apple-touch-icon" sizes="180x180" href="{{url_for('static', filename='icons/apple-icon-180x180.png')}}">
        <link rel="icon" type="image/png" sizes="192x192"  href="{{url_for('static', filename='icons/android-icon-192x192.png')}}">
        <link rel="icon" type="image/png" sizes="32x32" href="{{url_for('static', filename='icons/favicon-32x32.png')}}">
        <link rel="icon" type="image/png" sizes="96x96" href="{{url_for('static', filename='icons/favicon-96x96.png')}}">
        <link rel="icon" type="image/png" sizes="16x16" href="{{url_for('static', filename='icons/favicon-16x16.png')}}">
        <link rel="manifest" href="{{url_for('static', filename='icons/manifest.json')}}">
        <meta name="msapplication-TileColor" content="#ffffff">
        <meta name="msapplication-TileImage" content="{{url_for('static', filename='icons/ms-icon-144x144.png')}}">
        <meta name="theme-color" content="#ffffff">
    </head>

    <body id='page-top'>
        <div class="container-fluid">
            {%- block breadcrumb -%}
            {%- endblock -%}
            <div class="row">
                <div class="col-12">
                    {%- block content -%}
                    {%- endblock -%}
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
