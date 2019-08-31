<!DOCTYPE html>
<html lang="fr">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ironemes.eu.org</title>

    <!-- CSS -->
    <link rel="stylesheet" href="{{url_for('static', filename='css/fonts.css')}}">
    <link rel="stylesheet" href="{{url_for('static', filename='bootstrap/css/bootstrap.min.css')}}">
    <link rel="stylesheet" href="{{url_for('static', filename='font-awesome/css/font-awesome.min.css')}}">
    <link rel="stylesheet" href="{{url_for('static', filename='css/animate.css')}}">
    <link rel="stylesheet" href="{{url_for('static', filename='css/magnific-popup.css')}}">
    <link rel="stylesheet" href="{{url_for('static', filename='flexslider/flexslider.css')}}">
    <link rel="stylesheet" href="{{url_for('static', filename='css/form-elements.css')}}">
    <link rel="stylesheet" href="{{url_for('static', filename='css/style.css')}}">
    <link rel="stylesheet" href="{{url_for('static', filename='css/media-queries.css')}}">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="{{url_for('static', filename='js/html5shiv.js')}}"></script>
    <script src="{{url_for('static', filename='js/respond.min.js')}}"></script>
    <![endif]-->

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

</head>

<body>

<!-- Top menu -->
<nav class="navbar" role="navigation">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#top-navbar-1">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <h1><a href="{{ url_for('start_page') }}">ironemes.eu.org</a></h1>
        </div>
        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="top-navbar-1">
            <ul class="nav navbar-nav navbar-right">
                <li {% block activemenu1 -%} {%- endblock -%}>
                    <a href="{{ url_for('start_page') }}"><i class="fa fa-home"></i><br>Home</a>
                </li>
                <li {% block activemenu2 -%} {%- endblock -%}>
                    <a href="{{ url_for('search') }}"><i class="fa fa-search"></i><br>Recherche</a>
                </li>
            </ul>
        </div>
    </div>
</nav>

{%- block content -%}
{%- endblock -%}
<!-- Footer -->
<footer>
    <div class="container">
        <div class="row">
            <div class="col-sm-7 footer-copyright wow fadeIn">
                <p>
                    Template by <a href="http://azmind.com/free-bootstrap-themes-templates/">Azmind</a>
                </p>
            </div>
            <div class="col-sm-5 footer-social wow fadeIn">
                <p>
                    <a href="https://github.com/ashgan-dev/ironemes" target="_blank"><i class="fa fa-github"></i> voir sur Github</a>
                </p>
            </div>
        </div>
    </div>
</footer>

<!-- Javascript -->
<script src="{{url_for('static', filename='js/jquery-1.11.1.min.js')}}"></script>
<script src="{{url_for('static', filename='bootstrap/js/bootstrap.min.js')}}"></script>
<script src="{{url_for('static', filename='js/bootstrap-hover-dropdown.min.js')}}"></script>
<script src="{{url_for('static', filename='js/jquery.backstretch.min.js')}}"></script>
<script src="{{url_for('static', filename='js/wow.min.js')}}"></script>
<script src="{{url_for('static', filename='js/retina-1.1.0.min.js')}}"></script>
<script src="{{url_for('static', filename='js/jquery.magnific-popup.min.js')}}"></script>
<script src="{{url_for('static', filename='flexslider/jquery.flexslider-min.js')}}"></script>
<script src="{{url_for('static', filename='js/jflickrfeed.min.js')}}"></script>
<script src="{{url_for('static', filename='js/masonry.pkgd.min.js')}}"></script>
<script src="{{url_for('static', filename='js/jquery.ui.map.min.js')}}"></script>
<script src="{{url_for('static', filename='js/scripts.js')}}"></script>

</body>

</html>