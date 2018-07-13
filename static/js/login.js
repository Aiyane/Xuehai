/**
 * Created by Administrator on 2017/4/22.
 */
$(function () {
    $("#login_form").validate(
        {
            /*自定义验证规则*/
            rules: {
                username: {
                    required: true,
                    rangelength: [2, 10]
                },
                password: {
                    required: true,
                    rangelength: [5, 16]
                }
            },
            /*错误提示位置*/
            // errorPlacement: function (error, element) {
            //     error.appendTo(".tip")
            // }
        }
    );
});
$("#forget_password").click(function () {
    alert("请登录邮箱完成密码重置。");
});
