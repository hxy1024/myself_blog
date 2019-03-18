// 首页的返回顶部
$(document).bind('scroll', function () {
    let toTop = document.documentElement.scrollTop || document.body.scrollTop;
    if (toTop >= 400) {
        $('#index-back-to-top').removeClass('hidden')
    } else {
        $('#index-back-to-top').addClass('hidden')
    }
});


$('#index-back-to-top').bind('click', function () {
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
