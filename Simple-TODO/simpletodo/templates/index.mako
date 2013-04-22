<%inherit file="base.mako"/>
	<div class="box">
		<div class="box todos">
			<h2 class="box">待办事项</h2>
			<ul>

				% for todo in todos:
					<li>
						% if todo.finished==0:
							${ todo.title } &nbsp;
							<a href="/todo/${ todo.id }/finish?status=yes">完成</a>
						% endif
						% if todo.finished==1:
							<del>${ todo.title }</del> &nbsp;
							<a href="/todo/${ todo.id }/finish?status=no">恢复</a>
						% endif
						<a href="/todo/${ todo.id }/edit">修改</a>
						<a href="/todo/${ todo.id }/delete" onclick="return confirm('删除以后不能恢复的，确定？')">删除</a>
					</li>
				% endfor

			</ul>
		</div>


		<div class="box post">
            <h2>新增</h2>
            <form action="/todo/new" method="post" id="post_new" onsubmit="return emptyCheck()">
                <p><input type="text" name="title" class="long_txt" /></p>
                <p><input type="submit" class="submit" value="添加" /></p>
            </form>
        </div>

	</div>


<%def name="bottom()">
<script type="text/javascript">
	function emptyCheck() {
		var title= document.all['title'].value;
		if (title.length == 0) {
			alert("内容不能为空，请输入.")
			return false;
		}
		return true;
	}
</script>
</%def>
