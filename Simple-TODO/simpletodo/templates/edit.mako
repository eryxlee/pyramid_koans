<%inherit file="base.mako"/>
	<div class="box">
		<div class="box post">
            <h2>修改</h2>
            <form action="/todo/${ todo.id }/edit" method="post" id="post_new" onsubmit="return emptyCheck()">
                <p><input type="text" name="title" class="long_txt" value="${ todo.title }"/></p>
                <p><input type="submit" class="submit" value="完成" /></p>
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