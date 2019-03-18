// 页面的控制文件，处理页面隐藏、进度切换、宽度自适应等
let $siteNav = $('.site-nav');
let $siteList = $('.site-list');
let $siteMain = $('.site-main');
// 标志当前是否隐藏侧边栏的标志位
let sideBarIn = null;

$(function () {
    // 首次加载时调整页面高度为浏览器可见区域高度
    adjustHeight();
    adjustArticleTop();
    adjustWidth();
});

// 绑定事件，当高度变化的时候调整
$(window).bind('resize', function () {
    adjustArticleTop();
    adjustHeight();
    adjustWidth();
});

function adjustWidth() {
    // 监测页面宽度，当小于sm宽度的时候，隐藏左边2列
    // 当宽度大于1800的时候，调整左边2列的宽度
    let mdWidth = 992;
    let curWidth = $(window).width();
    if (curWidth < mdWidth) {
        $('.site-nav, .site-list').addClass('hidden')
    } else {
        $('.site-nav, .site-list').removeClass('hidden')
    }
}

function adjustHeight() {
    $('.site-nav, .site-list, .site-main').css('height', top.innerHeight);
    $('.settings').removeClass('hidden');
}

// 当点击缩进按钮的时候，左侧栏切换缩进
$('#sidebar-hide-btn').bind('click', function () {
    let $btn = $(this);
    $btn.toggleClass('side_in');

    if ($btn.hasClass('side_in')) {
        sidebar_in($btn);
    } else {
        sidebar_out($btn);
    }
});

function sidebar_in($btn) {
    sideBarIn = true;
    // 首先获取当前滚动条位置以便隐藏侧栏之后恢复阅读位置
    let curTop = $('.site-main').scrollTop();

    // 当点击缩进的时候，取消侧边栏的展示，恢复主体页面的100%高度
    $siteNav.addClass('hidden');
    $siteList.addClass('hidden');
    $siteMain.removeClass('col-md-7 col-lg-7').addClass('col-md-8 col-md-offset-2');

    $siteMain.css({height: '100%',});
    $(window).off('resize');

    // 设置文章fix的title宽度
    adjustArticleTop();
    let $copySettings = $('div.settings').clone(true);
    $copySettings.find('i.glyphicon-arrow-left').removeClass('glyphicon-arrow-left').addClass('glyphicon-arrow-right').parent().attr('title', '显示');
    let $control = $('.side-left-control');
    $control.text('').removeClass('hidden').append($copySettings);

    // 恢复阅读位置
    $(window).scrollTop(curTop);
}

function sidebar_out($btn) {
    sideBarIn = false;
    // 首先获取当前滚动条位置以便显示侧栏之后恢复阅读位置
    let curTop = $(window).scrollTop();

    // 将缩进按钮展示在页面上，并提示为缩进图标
    $('.side-left-control').html('').addClass('hidden');

    $('#sidebar-hide-btn').removeClass('side_in');
    $siteNav.removeClass('hidden');
    $siteList.removeClass('hidden');
    $siteMain.removeClass('col-md-8 col-md-offset-2').addClass('col-md-7 col-lg-7');

    // 设置文章fix的title宽度
    adjustArticleTop();

    $('.site-nav, .site-list, .site-main').css('height', top.innerHeight);
    $(window).bind('resize', adjustHeight);

    // 恢复阅读位置
    $('.site-main').scrollTop(curTop);
}

function adjustArticleTop() {
    // 设置文章fix的title宽度
    let articleTopWidth = $('.article-area').width();
    $('.article-top').css('width', articleTopWidth)
}
