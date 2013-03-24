<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <title><%block name="title">kibra</%block></title>

        <link type="text/css" rel="stylesheet" media="all" href="${request.static_url('kibra:static/css/autosuggest.css')}" />
        
        <script type="text/javascript" src="${request.static_url('kibra:static/js/levenshtein.js')}"></script>
        <script type="text/javascript" src="${request.static_url('kibra:static/js/mootools-1.2.4-core-nc.js')}"></script>
        <script type="text/javascript" src="${request.static_url('kibra:static/js/mootools-1.2.4.4-more-nearly-full.js')}"></script>
        <script type="text/javascript" src="${request.static_url('kibra:static/js/outerclick.js')}"></script>
        <script type="text/javascript" src="${request.static_url('kibra:static/js/autosuggest.js')}"></script>
    </head>
    <body>
        %if authenticated_userid(request):
            <div>
                <a href="${request.route_path('logout')}">Logout</a>
            </div>
        %endif
        
        ${next.body()}
    </body>
</html>