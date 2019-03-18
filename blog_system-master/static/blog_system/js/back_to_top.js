// 返回顶部的js文件，当滚动窗口的时候，监控当前文章进度百分比
$(document).on('scroll', showBack);

$('.site-main').on('scroll', showBack);

function showBack(event) {
    let $back = $('#back-to-top');
    let toTop = $(this).scrollTop();

    let articleHeight;
    // 全屏时候的滚动
    if (event.target === document) {
        articleHeight = $(document).innerHeight() - top.innerHeight;
    } else {
        // 分屏时候的滚动
        articleHeight = $('.article-area').innerHeight() - $(this).innerHeight();
    }

    // 计算进度百分比
    let rate = toTop / articleHeight;
    if (!rate) {
        rate = 0;
    }

    let rateNum = parseInt(rate * 100);
    if (rateNum > 100) {
        rateNum = 100;
    } else if (rateNum < 1) {
        $back.addClass('hidden');
        rateNum = 0;
    } else {
        $back.removeClass('hidden');
    }

    // 显示在返回顶部中
    $back.find('span.top-rate').text(rateNum + '%');
    $('.control-top-rate').text(rateNum + '%');

    // 当滚动到一定进度的时候才显示返回顶部
    if (rateNum > 4) {
        $('#control-back-to-top').removeClass('hidden')
    } else {
        $('#control-back-to-top').addClass('hidden')
    }
}


$('#control-back-to-top').bind('click', function () {
    // 当有侧边栏的时候直接返回
    $('.site-main').animate({'scrollTop': 0}, 500);

    // 没有测边栏的时候处理返回
    // 50豪秒下降350px
    let t = 50;
    let gap = 350;

    let index = setInterval(function () {
        let toTop = document.documentElement.scrollTop || document.body.scrollTop;
        if (toTop > 0) {
            toTop = toTop - gap;
            $(document).scrollTop(toTop);
        } else {
            clearInterval(index);
        }
    }, t);
});
