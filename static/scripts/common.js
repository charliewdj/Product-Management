$(document).ready(function() {
	// ログアウトボタン押下処理
	$("#logout_btn").click(function(){
		window.location.href = "/";
	});

	// メニューアコーディオン
	$("[class^='col-sm']").click(function(){
		var targetDiv = $(this).parent().children().children("div:visible[class=text-nowrap]");
		$(this).children("div:last").slideToggle();
		targetDiv.slideUp();
	});
});

// ファイルアップロード画面Submit
function msg(id) {
	switch (id) {
		case "CLERR0001" : return "アップロードファイルを指定してください。"; break;
		case "CLERR0002" : return "検索条件は１つ以上指定してください。"; break;
		case "CLERR0003" : return "対象データを１つ以上選択してください。"; break;
		default          : return "システムエラーが発生しました。"; break;
	}
}
