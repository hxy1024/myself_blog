// 当点击文章概览面板的时候，访问文章详情页面
$('.site-list').on('click', 'div.article-panel', function (event) {
    if ($(event.target).hasClass('article-panel-close')) {
        return false;
    }
    let $curPanel = $(this);
    location.href = $curPanel.data('article_url');
    return false;
});
