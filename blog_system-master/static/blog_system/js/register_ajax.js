/*
* 此文件提供了以ajax提交注册数据的功能, 以使得注册行为不需要全局刷新页面。
* 由服务端执行注册信息校验，并返回约定格式的数据, 客户端根据返回的数据内容进行后续操作。
*
*/


// 绑定事件，用户点击提交注册时，执行此函数
$('#register-btn').bind('click', register);

function register() {
    // 1、组织表单数据
    let formData = {
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        'username': $('#id_username').val(),
        'password': $('#id_password').val(),
        're_password': $('#id_re_password').val(),
        'telephone': $('#id_telephone').val(),
        'email': $('#id_email').val(),
    };

    // 2、启动ajax提交表单数据
    $.ajax({
        url: '',
        type: 'POST',
        data: formData,
        success: handle,  // 3、处理返回值
    });
}

// 注册信息提交后，处理服务端返回的数据
function handle(response_data) {
    if (response_data.status) {
        // 注册成功
        location.href = response_data.next;
    } else {
        // 注册失败
        // 1、清空原有错误消息
        $('.field_error_msg').html('&nbsp;');

        // 2、将新的错误信息附加到对应错误区域
        let fields_error = response_data.fields_error;
        for (field_name in fields_error) {
            $('#id_' + field_name).parent().find('span.field_error_msg').text(fields_error[field_name]);
        }
    }
}
