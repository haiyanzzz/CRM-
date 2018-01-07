 // 方式一
$(function () {
        $(".item-title").click(function () {
              $(this).next().toggleClass("hide")
        })
    });
// 方式二：
//  $(function () {
//     $('.item-title').click(function () {
//         if($(this).next().hasClass('hide')){
//             $(this).next().removeClass('hide')
//         }else{
//             $(this).next().addClass('hide')
//         }
//     })
//  });