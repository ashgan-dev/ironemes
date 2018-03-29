<!DOCTYPE html>
<html lang="fr" xmlns="http://www.w3.org/1999/html">
<head>
    <meta charset="UTF-8">
    <title>ironème</title>
    <script src="js/jquery.min.js"></script>
    <script src="js/kickstart.js"></script> <!-- KICKSTART -->
    <link rel="stylesheet" type="text/css" href="css/kickstart.css" media="all" /> <!-- KICKSTART -->
    <link rel="stylesheet" type="text/css" href="css/style.css" media="all" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body class="elements">
    <div class="grid">
        {%- for i in html_files: %}
        <ul class="alt">
            <li>
                <a href="{{ i.name }}">
                    {{ i | proper_name }}
                </a>
            </li>
        </ul>
        {% endfor %}
    </div>
</body>
</html>
