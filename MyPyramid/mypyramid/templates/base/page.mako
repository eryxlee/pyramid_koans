## -*- coding: utf-8 -*-
<%namespace name="navigation" file="../component/navigation.html" import="*" /><%namespace name="footer" file="../component/footer.html" import="*" />
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Steel Trade System</title>

    <!-- CSS styles -->
    <link href="${request.registry.settings['static.url.bootstrap.css']}" rel="stylesheet">
    <style type="text/css">
        body {
            padding-top: 60px;
            padding-bottom: 40px;
        }
        .sidebar-nav {
            padding: 9px 0;
        }
            /*!
            * make twitter bootstrap dropdown-menu on hover rather than click
            * from http://stackoverflow.com/questions/8878033/how-to-make-twitter-bootstrap-menu-dropdown-on-hover-rather-than-click
            */
        ul.nav li.dropdown:hover ul.dropdown-menu{
            display: block;
        }
        a.menu:after, .dropdown-toggle:after {
            content: none;
        }
    </style>
    <link href="${request.registry.settings['static.url.bootstrap-responsive.css']}" rel="stylesheet"><%if hasattr(next, 'current_css_link'): next.current_css_link()%>
    <!-- Le HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
    <script src="${request.static_path('steeltrade:static/js/html5.js')}"></script>
    <![endif]-->

    <!-- fav icons -->
    <link rel="shortcut icon" href="${request.static_path('steeltrade:static/favicon.ico')}">

    <!-- js included -->
    <script src="${request.registry.settings['static.url.jquery.js']}" type="text/javascript"></script>
    <script src="${request.registry.settings['static.url.bootstrap.js']}" type="text/javascript"></script><%if hasattr(next, 'current_js_link'): next.current_js_link()%>
</head>

<body>${navigation.nav_menu()}${next.body()}${footer.copyright()}
</body>
</html>
