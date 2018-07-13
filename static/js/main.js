$('.totop').click(function () {
    $('html,body').animate({scrollTop: 0}, 100);
    return false;
});

//顶部个人中心下拉框
$('.personal').hover(function () {
    $('.userdetail').stop(true).show();
}, function () {
    $('.userdetail').stop(true).hide();
});
var msg_show = true,
    msg = +$('#MsgNum').text();
function msgFlash() {
    var $elem = $('#MsgNum');
    if (!msg) {
        clearInterval(m);
    }
    if (msg_show) {
        $elem.text(msg);
        msg_show = false;
    } else {
        $elem.text('');
        msg_show = true;
    }
}
var m = setInterval(msgFlash, 500);
