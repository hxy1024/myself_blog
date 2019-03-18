// 点击文章概览面板中的X按钮的时候，会隐藏此面板
$('#article-panel-tree').on('click', 'span.article-panel-close', function (event) {
    $(event.target).parents('div.article-panel').slideUp();
    return false;
});
