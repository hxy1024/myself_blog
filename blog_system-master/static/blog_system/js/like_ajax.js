// 当喜欢或者不喜欢被点击的时候，发起ajax请求更新服务器端数据
// 并获取服务端返回的数据，更新至页面dom树
$('.like-span, .dislike-span').bind('click', function (event) {
    // 处理颜色切换
    switchColor($(this));

    // 判断用户点击
    let like = $(this).hasClass('like-span');

    let nid = $('#article-nid').text();
    // 发起ajax请求
    $.ajax({
        url: '/query/like/' + nid + '/',
        type: 'GET',
        data: {'like': like},
        success: function (data) {
            handleLike(data);
        }
    })
});

function handleLike(response_data) {
    // 如果服务端发送了下一跳，则跳转
    let next = response_data['next'];
    if (next) {
        location.href = next;
        return false;
    }
}

function switchColor($cur) {
    // 获取当前点击元素  判断用户点击
    let like = $cur.hasClass('like-span');
    if (like) {
        // 点击了赞同
        $other = $('.dislike-span');
        $cur.toggleClass('click-like');
        $other.removeClass('click-dislike')
    } else {
        // 点击了反对
        $other = $('.like-span');
        $cur.toggleClass('click-dislike');
        $other.removeClass('click-like');
    }
}
