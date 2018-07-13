/**
 * Created by Administrator on 2017/4/29.
 */

// 计算页面的实际高度，iframe自适应会用到
function calcPageHeight(doc) {
    var cHeight = Math.max(doc.body.clientHeight, doc.documentElement.clientHeight)
    var sHeight = Math.max(doc.body.scrollHeight, doc.documentElement.scrollHeight)
    var height = Math.max(cHeight, sHeight)
    return height
}
var ifr = document.getElementById('myiframe')
ifr.onload = function () {
    var iDoc = ifr.contentDocument || ifr.document
    var height = calcPageHeight(iDoc)
    ifr.style.height = height + 'px'
}
