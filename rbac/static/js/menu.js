$('.item .title').click(function () {
    // $(this).next().toggleClass('hide')
    $(this).next().removeClass('hide');     // 当前一级标签下的标签显示
    $(this).parent().siblings().find('.body').addClass('hide');     // 其他的二级标签隐藏


});


