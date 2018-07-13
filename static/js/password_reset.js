/**
 * Created by Administrator on 2017/4/23.
 */
$(function () {
    $("#reset_password_form").validate(
        {
            /*自定义验证规则*/
            rules: {
                username: {
                    required: true,
                    rangelength: [2, 10]
                },
                password1: {
                    required: true,
                    rangelength: [5, 16]
                },
                password2: {
                    required: true,
                    rangelength: [5, 16],
                    equalTo: "#password1"
                }
            }
        }
    );
});