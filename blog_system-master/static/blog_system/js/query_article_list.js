/*
* 此模块为通过ajax形式获取当前分类的文章目录list。
* 文章目录将会以链接的形式展示在siteNav中，每次
* 点击不同的分类，就会发送ajax获取对应的链接数据
* 并渲染。
* */


// 样式类cssClass，作为当前分类文章列表的样式配置
cssClass = 'article-link';
blog_path = $('#blog-path').text();
categoryName = null;
$('.category-item').bind('click', queryListWithAjax);


// 以获取对应的文章list列表
// 当发起ajax请求的时候，携带当前站点名称+当前点击分类名称，
function queryListWithAjax() {
    $(this).addClass('nav-active').siblings().removeClass('nav-active');
    categoryName = $(this).children('span.category-name').text();
    let curBlogPath = $('#blog-path').text();
    let queryData = {
        categoryName: categoryName,
        curBlogPath: curBlogPath,
    };

    // 启动ajax请求对应文章列表数据
    $.ajax({
        url: '/query/article_list/',
        type: 'GET',
        data: queryData,
        success: function (response) {
            // 清空搜索框的内容
            $('#search-input').val('');
            buildArticlePanelTree(response);

            // 渲染完面板树后，对目标文章面板渲染样式
            renderArticlePanel();
        },
    });

    // 取消冒泡和默认事件
    return false;
}


// 此函数用于根据服务端返回的文章列表数据，生成文章概览面板树
function buildArticlePanelTree(response) {
    let $tree = $('#article-panel-tree');
    $tree.html('');

    $.each(response, function (index, article) {
        let $panelExp = $('.article-panel-exp').clone().removeClass('article-panel-exp hidden').addClass('article-panel');

        // 获取文章数据
        let nid = article.nid;
        let title = article.title;
        let create_time = article.create_time;
        let comment_count = article.comment_count;
        let like_count = article.like_count;
        let dislike_count = article.dislike_count;
        let view_count = article.view_count;

        // 渲染一个文章面板中的数据
        $panelExp.find('span.article-panel-title').text(title);
        $panelExp.find('span.article-panel-create-time').text(create_time);
        $panelExp.find('span.article-panel-comment-count').text(comment_count);
        $panelExp.find('span.article-panel-like-count').text(like_count);
        $panelExp.find('span.article-panel-dislike-count').text(dislike_count);
        $panelExp.find('span.article-panel-view-count').text(view_count);
        $panelExp.attr('target-article-nid', nid);

        // 保存该面板指向的文章url连接
        let articleUrl = '/blog/' + blog_path + '/article/' + categoryName + '/' + nid + '/';
        $panelExp.data('article_url', articleUrl);

        // 面板data中保存文章title内容，以便后续搜索的时候恢复
        $panelExp.data('originTitle', title);

        // 面板绑定移入移出显示关闭按钮的事件
        $panelExp.mouseenter(function () {
            $(this).find('span.article-panel-close').removeClass('hidden')
        });
        $panelExp.mouseleave(function () {
            $(this).find('span.article-panel-close').addClass('hidden')
        });

        $tree.append($panelExp);
    });
}
