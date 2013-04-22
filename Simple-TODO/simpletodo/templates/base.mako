<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>
			title
		</title>
		<link rel="stylesheet" href="${request.static_path('styles/reset.css')}" type="text/css"/>
		<link rel="stylesheet" href="${request.static_path('styles/index/style.css')}" type="text/css"/>
	</head>

	<body>
		<div class="page">
			<div class="header box">
				<a href="http://www.pylonsproject.org/" target="_blank">
        			<img src="${request.static_path('images/pyramid-small.png')}" alt="powered by pyramid" />
        		</a>
				<a href="/">任务跟踪</a>
			</div>

			<div class="main box">
                ${next.body()}
			</div>

			<div class="foot">
        		Copyright <span>©</span> 任务跟踪
        		作者 <a href="http://simple-is-better.com/">Python.cn(news, jobs)</a>
        		&nbsp;
        		<a href="http://webpy.org/" target="_blank">
        			<img src="${request.static_path('images/webpy_ss.png')}" alt="powered by web.py" />
        		</a>
        		<br>
        		本程序由Eryx Lee使用Pyramid改写
    		</div>
		</div>
        <%if hasattr(next, 'bottom'): next.bottom()%>
	</body>

</html>