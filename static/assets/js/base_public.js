//<div class="hiding"><div><ul><li><a>......显示隐藏文本
function showText(button_hidden){
    $($(button_hidden).parent().parent()).prevAll().removeClass("hiding");
    $(button_hidden).parent().remove()
}
//依据ID跳转article
function blink_to_acticle(blink_block,link_url){
    var url = '/'+link_url+'/'+$(blink_block).attr('id')
    // alert(url)
    window.location.href=url;
}