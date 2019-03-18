/*
* 此文件功能：
* 1、用于增加根评论、子评论
* 2、发送评论数据给服务器后，在客户端，由js渲染当前页面的评论dom节点
*
* */


// 根评论表单绑定点击发送事件
$('.comment-add-btn').bind('click', function () {
    /*
    * 此函数的执行意味着根评论已经输入完毕，并准备发送
    * 此函数的功能主要是收集评论发送需要的各类数据
    * */

    let article_id = $('#article-nid').text();
    let $input = $('#comment-add-input');
    let content = $input.val().trim();
    let $replyError = $(this).parent().find('span.reply-error');
    // 如果没有输入任何回复内容，就不会提交
    if (!content) {
        $replyError.text('请输入回复内容');
        return false;
    }
    $input.val('');  // 清空输入框的内容
    $replyError.text('');

    let parent_id = null;  // 根评论没有父级元素
    let csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();
    let reply_to = null;
    let root_id = null;

    sendComment(article_id, content, csrfmiddlewaretoken, parent_id, reply_to, root_id);
});


// 子评论输入框绑定点击发送事件
// 必须使用冒泡处理，因为输入框是后期加入到dom树的，无法绑定事件
$('#comment-tree').on('click', 'button.comment-reply-btn', function () {
    /*
    * 此函数的执行意味着子评论已经输入完毕，并准备发送
    * 此函数的功能主要是收集评论发送需要的各类数据
    * */

    let article_id = $('#article-nid').text();
    // 获取当前子评论的输入框内容
    let $input = $(this).parent().find('input');
    let content = $input.val().trim();
    let $replyError = $(this).parent().find('span.reply-error');
    // 如果没有输入任何回复内容，就不会提交
    if (!content) {
        $replyError.text('请输入回复内容');
        return false;
    }
    // 点击发送后，并清空内容
    $input.val('');

    // 子评论必须要有父级元素
    let $parent = $(this).parents('li.comment-item').first();
    let parent_id = $parent.find('span.reply-toggle').attr('parent_id');
    let csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();

    // 获取回复的目标用户
    let reply_to = $parent.find('span.comment-username').first().text();
    let root_id = $parent.find('span.root-id').text();

    sendComment(article_id, content, csrfmiddlewaretoken, parent_id, reply_to, root_id);
    return false;
});


function sendComment(article_id, content, csrfmiddlewaretoken, parent_id, reply_to, root_id) {
    /*
    * 此函数用于发送评论数据，包含根评论和子评论数据
    * 发送的数据格式为：
    * request_data = {
    *     parent_id         评论目标id，为空就是根评论，否则就是指定评论记录
    *     content         评论内容
    *     article_id         所属文章id
    *     csrf               用于csrf验证
    *  }
    *
    *  期望收到的数据格式为：
    *  response_data = {
    *     nid                 当前评论记录id
    *     username            评论人
    *     created_at                 创建时间
    *  }
    * */

    // 1、创建ajax数据
    let data = {
        article_id: article_id,
        content: content,
        parent_id: parent_id,
        csrfmiddlewaretoken: csrfmiddlewaretoken,
        reply_to: reply_to,
        root_id: root_id,
    };

    // 2、启动ajax
    $.ajax({
        url: '/query/add_comment/',  // 硬编码url
        type: 'POST',
        data: data,
        // 3、调用回调
        success: function (data) {
            // 如果有下一跳地址则跳转
            let next = data['next'];
            if (next) {
                location.href = next;
                return false;
            }

            // 更新折叠处的评论数量
            let $count = $('#comment-count');
            let oldCount = parseInt($count.text());
            let newCount = oldCount + 1;
            $count.text(newCount);

            // 更新article top的评论数量
            let $commentCountSpan = $('span.article-panel-comment-count');
            $commentCountSpan.text(parseInt($commentCountSpan.text()) + 1);


            // 创建一个新的评论项目
            let $newLi = buildNewLi(data, article_id, content);

            // 判断是调用根评论dom渲染， 还是子评论dom渲染
            if (!parent_id) {
                // 3、插入dom树
                let $tree = $('#comment-tree');
                let curFlootCount = $tree[0].childElementCount + 1;
                $newLi.find('span.floot-count').text(curFlootCount + '楼  ');
                $tree.append($newLi);

                // 更新评论数量
                $('.article-panel-comment-count').text(newCount);

            } else {
                // 3、寻找此子节点的根节点, 并插入dom树
                let condition = `span[parent_id=${parent_id}]`;
                let $parentLi = $(condition).parents('li.comment-item').first();

                // 3、寻找此子节点的根节点, 并插入dom树
                let root_id = data.root_id;
                let $rootLi = $('#comment-' + root_id);

                // $parentLi.append($newLi);
                $rootLi.append($newLi);
                $parentLi.find('span.reply-toggle').first().trigger('click');
            }
        },
    });
}


// 此函数用于提炼冗余, 根据服务端返回的数据生成一个评论节点
function buildNewLi(response_data, article_id, content) {
    // 1、解析响应数据
    let nid = response_data.nid;
    let created_at = response_data.created_at;
    let nickName = response_data.nick_name;
    let avatarUrl = response_data.avatar;
    let username = response_data.username;
    let replyToNickName = response_data.reply_to_nick_name;
    let root_id = response_data.root_id;

    // 2、准备新的子评论节点
    let $newLi = $('.comment-item-exp').clone().removeClass('comment-item-exp hidden').addClass('comment-item');
    $newLi.attr('id', 'comment-' + nid);
    $newLi.find('span.comment-nick-name').first().text(nickName);
    $newLi.find('span.comment-created-at').first().text(created_at);
    $newLi.find('p.comment-content').first().text(content);
    $newLi.find('img.comment-avatar').first().attr('src', avatarUrl);
    $newLi.find('span.reply-toggle').first().attr('parent_id', nid);
    $newLi.find('span.comment-username').first().text(username);
    $newLi.find('span.root-id').text(root_id);
    if (replyToNickName) {
        $newLi.find('span.reply-to-nick-name').first().text(' 回复@ ' + replyToNickName + '：');
    }
    $newLi.find('div.comment-foot').remove();

    return $newLi;
}


// 评论项中，点击回复的时候，展示子评论输入框, 因为评论数量很多，使用冒泡处理
$('#comment-tree').on('click', 'span.reply-toggle', replyToggle);


function replyToggle() {
    /*
    * 回复输入框在回复被点击的时候，添加到对应回复的下方，通过toggle控制切换展示和隐藏
    * 此函数的功能是，一旦点击回复，执行此函数
    * 此函数会将回复评论输入框复制一份到当前评论项中
    *
    * 注意：当前评论项只有在第一次被点击回复的时候才需要clone
    * */

    let $commentFoot = $(this).parent();
    let clicked = $(this).data('clicked');
    let nickName = $(this).parents('li.comment-item').first().find('span.comment-nick-name').first().text();

    if (!clicked) {
        // 1、复制回复评论输入框
        let $newReplyArea = $('.comment-reply-area-exp').clone().removeClass('comment-reply-area-exp');

        // 让输入框有一个默认显示的内容，展示： 回复给xxx
        $newReplyArea.find('input.comment-reply-input').first().attr('placeholder', '回复给：' + nickName);

        // 2、加入当前评论项
        $commentFoot.append($newReplyArea);

        $(this).data('clicked', true);
    }

    // 3、隐藏除了自己以外的所有回复评论输入库
    let curId = $(this).attr('parent_id');
    let condition = `[parent_id!=${curId}]`;
    $('span.reply-toggle').filter(condition).parent().find('div.comment-reply-area').addClass('hidden');

    // 清除所有子评论输入框的内容(新增), 清除发送错误信息
    $('.comment-reply-input').val('');
    $('.reply-error').text('');

    // 4、toggle切换当前评论输入框
    $commentFoot.find('div.comment-reply-area').first().toggleClass('hidden');

    return false;
}
