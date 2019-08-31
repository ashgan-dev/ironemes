{%- extends "layout.tpl" -%}
{%- block activemenu2 -%}
class="dropdown active"
{%- endblock -%}
{%- block content -%}

<div class="contact-us-container">
    <div class="container">
        <div class="row">
            <div class="col-sm-5 contact-address wow fadeInUp">
                <p>Utilisez le formulaire pour chercher un mot, une expression ou un groupe de lettres.</p>
                <p>Si un ou plusieurs toots contiennent votre expression, ils s'afficheront.</p>
                <p>Pour chercher un utilisateur en particulier, cherchez @username.</p>
                <p>Attention, la recherche est sensibile à la casse (différence majucule/minuscule).</p>
            </div>
            <div class="col-sm-7 contact-form wow fadeInRight">
                <form role="form" data-toggle="validator" action="{{ url_for('search') }}" method="POST">
                    <div class="form-group">
                        <label for="search">Entrez votre recherche:</label>
                        <input type="text" name="search">
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
    </div>
</div>
{%- endblock -%}