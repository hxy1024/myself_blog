/*
* 此文件的作用是，当点击查看评论的时候，发起ajax请求获取此文章所有评论数据
* 通过js，将评论数据渲染到评论树中(以多层级方式)
* 1、请求此文章所有评论数据
* 2、创建每一个文章的dom节点并渲染到评论树中,且以多层级的方式
*
* */

// 点击评论折叠按钮后执行请求, 先删除旧评论树，再添加评论树
$('#comment-tree').on('show.bs.collapse', function () {
    $(this).html('');
    getCommentList();
});

function getCommentList() {
    // 获取文章id
    let article_id = $('#article-nid').text();
    let csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();

    // 发起请求
    // 请求当前文章所有评论数据
    $.ajax({
        url: '/query/comment_list/',  // 此处硬编码url
        type: 'POST',
        data: {
            article_id: article_id,
            csrfmiddlewaretoken: csrfmiddlewaretoken,
        },
        success: function (data) {
            renderTree(data);
        },
    });
}

// 渲染评论树
function renderTree(comment_list) {
    /*
    * 此函数的功能是将评论记录数据渲染成多层级的评论树结构
    * 评论记录有根评论和子评论两类，多层级通过不同的缩进来体现
    * 参考如下伪代码：
    *    comment_list
    *    for comment in comment_list:
    *        comment_item = build_item(comment)
    *
    *        if comment is root_comment:
    *            comment_tree.append(comment_item)
    *        else:
    *            parent_comment_item = find_item_with(comment.pid)
    *            parent_comment_item.append(comment_item)
    *
    * comment的数据结构是:  {
    *       content: "666"
    *       created_at: "2018-10-26T12:58:04.711Z"
    *       nid: 14
    *       parent__nid: null
    *       user__username: "zlw
    *  }
    *
    * 1、不论是根评论还是子评论，它们都应该被渲染成同样的dom节点，均从模板clone
    * 2、两类评论的区别在于dom节点位置的不同
    * 3、两类评论的pid不同，
    *
    * */

    // 遍历所有的comment
    let flootCount = 0;
    $.each(comment_list, function (comment_index, comment_obj) {
        // 每一个comment完成各自的dom节点渲染
        let $newLi = renderNode(comment_obj, comment_index);

        // 判断comment的类别
        let pid = comment_obj.parent__nid;
        if (!pid) {
            // 根评论直接加入评论树第一层
            flootCount++;
            $newLi.find('span.floot-count').text(flootCount + '楼  ');
            $('#comment-tree').append($newLi);
        } else {
            // 子评论加入对应的父评论，作为它的子层,子评论全部放在第二层，不形成多层级(最多两层)
            let root_id = comment_obj.root_id;
            let $rootLi = $('#comment-' + root_id);
            let $parentLi = $('#comment-' + pid);
            $rootLi.append($newLi);
        }
    })
}

// 渲染单独一个评论dom节点
function renderNode(comment_obj) {
    // 解析comment对象的数据
    let nickName = comment_obj.user__profile__nick_name;
    let content = comment_obj.content;
    let nid = comment_obj.nid;
    let created_at = comment_obj.created_at;
    // 硬编码media地址
    let avatarUrl = comment_obj.user__profile__avatar;
    let username = comment_obj.user__username;
    let replyToNickName = comment_obj.reply_to_nick_name;
    let replyShow = comment_obj.reply_show;
    let root_id = comment_obj.root_id;

    // clone评论项模板样例
    let $newLi = $('.comment-item-exp').clone().removeClass('comment-item-exp hidden').addClass('comment-item');
    // 渲染数据
    $newLi.find('span.comment-nick-name ').first().text(nickName);
    $newLi.find('span.comment-created-at').first().text(created_at);
    $newLi.find('p.comment-content').first().text(content);
    $newLi.find('span.reply-toggle').first().attr('parent_id', nid);
    $newLi.find('img.comment-avatar').first().attr('src', avatarUrl);
    $newLi.attr('id', 'comment-' + nid);
    $newLi.find('span.comment-username').first().text(username);
    $newLi.find('span.root-id').text(root_id);
    if (replyToNickName) {
        $newLi.find('span.reply-to-nick-name').first().text(' 回复@ ' + replyToNickName + '：');
    }

    // 如果是本人的评论，就不允许再次回复评论
    if (!replyShow) {
        $newLi.find('div.comment-foot').remove();
    }

    // 以jquery对象类型返回dom节点
    return $newLi;
}
