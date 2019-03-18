// 一旦选择avatar文件，就预览此图像
$('#avatar_file').bind('change', function () {
    let $img = $('#avatar_img');
    preview(this, $img);
});

// 一旦选择文章题图文件，就预览此图像
$('#article_file').bind('change', function () {
    let $img = $('#article_img');
    preview(this, $img);
});

function preview (file, $img) {
    let fileObj = file.files[0];
    let fileReader = new FileReader();
    fileReader.readAsDataURL(fileObj);
    fileReader.onloadend = function () {
        $img.attr('src', this.result);
    };
}
