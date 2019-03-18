/*
* 此文件用于以ajax形式提交登录数据，并根据服务端返回的结果展示是否正确登录。
* 此文件还用于以ajax形式请求验证码图片。
*
*/

// 绑定事件， 点击登录按钮的时候，提交登录数据
$('#login-btn').bind('click', login);

function login() {
    // 1、组织表单数据
    let formData = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'username': $('#id_username').val(),
        'password': $('#id_password').val(),
        'validate_code': $('#validate_code').val(),
    };

    // 2、启动ajax提交表单数据
    $.ajax({
        url: '',
        type: 'POST',
        data: formData,
        success: handle,  // 3、处理返回值
    });
}

// 处理登录后服务端的返回值
function handle(response_data) {
    if (response_data.status) {  // 登录成功, 跳转到服务端期望的下一跳地址
        location.href = response_data.next;
    } else {  // 登录失败, 清空历史错误信息并加载当前错误信息
        $('#form_error').text('').text(response_data.form_error);
    }
}

// 当点击验证码图片的时候变化src属性以重新发起获取验证码图片行为
$('#validate_code_img').bind('click', function (event) {
    event.target.src += '?';
});
