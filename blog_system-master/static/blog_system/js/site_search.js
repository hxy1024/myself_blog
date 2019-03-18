// 文章页面的搜索功能
// 处理搜索关键字中的特殊字符
let specialPattern = new RegExp(/[\(\)\[\]\{\}\*\.\?\\\~\^\$\+\!]/, 'g');

// 处理搜索框输入内容时，对文章面板进行title搜索
$('#search-input').bind('input', function () {
    let $search = $(this);
    let searchKey = $search.val().trim();

    let $tree = $('#article-panel-tree');
    // 如果文章面板树中没有节点，则不搜索
    if ($tree[0].childElementCount === 0) {
        return false;
    }

    // 处理输入的关键字中的特殊符号并转换成re对象
    let reObj = handleSpecial(searchKey);
    // 否则进行遍历，遍历每一个节点，执行filterTitle函数
    $.each($tree.children(), function (index, panelObj) {
        filterTitle(index, panelObj, reObj);
    });
});

function handleSpecial(searchKey) {
    // 将用户输入的内容转换成re对象，并处理特殊符号
    let validKey = searchKey.replace(specialPattern, function (result) {
        // 对搜索关键字中的特殊字符进行转义
        return '\\' + result;
    });

    // 安全的字符串转换成re对象用于搜索
    return new RegExp(validKey, 'ig');
}

// 对文章标题内容进行过滤
function filterTitle(index, panelObj, reObj) {
    /*
    *
    * 参数index是遍历文章面板树时的序号，panelObj是每一个dom节点
    * reObj是经过特殊字符处理的re对象
    *
    * */

    // 用原始内容进行re过滤
    let $panel = $(panelObj);
    let originTitle = $panel.data('originTitle');
    let newTitle = originTitle.replace(reObj, function (result) {
        // result就是匹配到的字符串，要加上搜索成功的样式
        return '<span class="search-target">' + result + '</span>';
    });
    // 设置节点的title内容为过滤后的内容,因为搜索成功字符串有html标签，所以要以html设置
    $panel.find('span.article-panel-title').html(newTitle);

    // 如果搜索不成功，则隐藏当前节点
    if (newTitle === originTitle) {
        $panel.addClass('hidden');
    } else {
        $panel.removeClass('hidden');
    }
}
