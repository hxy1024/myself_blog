// 当访问某一篇文章的时候，在文章面板列表中找到此文章面板，并渲染对应的样式
targetArticlePanelClass = 'selected-article-panel';

function renderArticlePanel() {
    // 当页面加载完毕的时候，找到对应的文章面板
    let nid = $('#article-nid').text();
    let condition = `div[target-article-nid=${nid}]`;
    let $targetPanel = $(condition);
    if ($targetPanel.length === 0) {
        return false;
    }

    // 配置对应的样式
    $targetPanel.addClass(targetArticlePanelClass);

    // 滚动面板列表至选中的面板位置
    let toTop = $targetPanel.offset().top;
    $('.site-list').scrollTop(toTop - 300);
}
