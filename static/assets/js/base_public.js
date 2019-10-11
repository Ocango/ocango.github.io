//<div class="hiding"><div><ul><li><a>......显示隐藏文本
function showText(button_hidden){
    $($(button_hidden).parent().parent()).prevAll().removeClass("hiding");
    $(button_hidden).parent().remove()
}