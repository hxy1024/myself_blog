// 请求指定文章的属性数据
$(function () {
    // 页面加载成功的时候，请求article id的属性数据
    let nid = $('#article-nid').text();
    $.ajax({
        url: '/query/article_attrs/' + nid + '/',
        type: 'GET',
        success: handle,
    });
});

function handle(response) {

    let comment_count = response.comment_count;
    let like_count = response.like_count;
    let dislike_count = response.dislike_count;
    let view_count = response.view_count;

    let $attrsSpan = $('.article-attrs-span');
    // 渲染一个文章面板中的数据
    $attrsSpan.find('span.article-panel-comment-count').text(comment_count);
    $attrsSpan.find('span.article-panel-like-count').text(like_count);
    $attrsSpan.find('span.article-panel-dislike-count').text(dislike_count);
    $attrsSpan.find('span.article-panel-view-count').text(view_count);
}
