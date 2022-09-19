// burgerメニュー
$(".burger").click(function(){
    $(".burger").toggleClass("is-active")
    $(".menu").toggleClass("is-active");
});

// 作成ボタン生成
$(function(){
    // 初期状態のボタンは無効
    $("#btn1").prop("disabled", true);
      // チェックボックスの状態が変わったら（クリックされたら）
        $("input[type='checkbox']").on('change', function () {
            // チェックされているチェックボックスの数
            if ($(".chk:checked").length > 2) {
                // ボタン有効
                $("#btn1").prop("disabled", false);
            } else {
                // ボタン無効
                $("#btn1").prop("disabled", true);
                $('p').text('3つ以上選択してください');
            }
        });
    });

// ボタンの値を取得
const lesson = [];
$("#btn1").click(function () {
    lesson.length = 0;
    $(':checkbox[class="chk"]:checked').each(function () {
        lesson.push($(this).val());
        $("#span3").text(lesson);
        });
    });

// チェックボックスを含む td 要素をクリックしたときに、チェックボックスをクリック
$('td:has(input[type=checkbox])').on('click', function(e){
    $(this).find('input[type=checkbox]').click();
});
// バブリングを防止
$('td input[type=checkbox]').on('click', function(e){
    e.stopPropagation();
});
