<!DOCTYPE html>
<html lang="fr" xmlns="http://www.w3.org/1999/html">
<head>
    <meta charset="UTF-8">
    <title>ironème</title>
    <script src="js/jquery.min.js"></script>
    <script src="js/kickstart.js"></script> <!-- KICKSTART -->
    <link rel="stylesheet" type="text/css" href="css/kickstart.css" media="all" /> <!-- KICKSTART -->
    <link rel="stylesheet" type="text/css" href="css/style.css" media="all" />
</head>
<body class="elements">
    <div class="grid">
        <style type="text/css">
        #icon-description{border:1px solid #ddd;padding:20px;background:#fff;}
        #icon-description span{color:red;}
        </style>
        <div class="col_9">
            {{ nb_toots }} toots exprimés au {{ now }} UTC
        </div>
        {%- for i in toots: %}
        <div class="col_9">
            <div id="icon-description" class="clearfix">
            <h6><a href="{{ i['account']['url'] }}" target="_blank">
                    <img src="{{ i['account']['avatar'] }}" height="24" width="24">
                </a>

                <a href="{{ i['account']['url'] }}" target="_blank">
                    {{ i['account']['username'] }}
                </a>
            </h6>
            {{ i['content'] }}
            <p>
                <span id="{{ i['id'] }}"></span>
                Tooté le <a href="{{ i['url'] }}" target="_blank">{{ i['created_at'] }}</a> - favoris:
                {% if i['favourites_count'] == 0: %}
                    {{ i['favourites_count'] }} <i class="fa fa-star-o"></i>
                {% else: %}
                    {{ i['favourites_count'] }} <i class="fa fa-star"></i>
                {% endif %}
            </p>
            </div>
        </div>
        {% endfor %}
    </div>
</body>
</html>
