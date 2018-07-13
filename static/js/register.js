/**
 * Created by Administrator on 2017/4/23.
 */
$(function () {
    $("#register_form").validate(
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
                },
                email: {
                    required: true,
                    email: true,
                },
                birth: {
                    date: true,
                },
                up_password: {
                    equalTo: "#password",
                },
            },
        }
    );
});
