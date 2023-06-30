$(document).ready(function() {
	// アップロードボタン押下処理
	$("#upload_btn").click(function(){
		$("#action_type").val("Upload");
		if ($("#upload_file").val() == "") {
			alert(msg("CLERR0001"));
			return false;
		}
		submitFileUploadForm();
	});

	// 確定ボタン押下処理
	$("#apply_btn").click(function(){
		$("#action_type").val("Apply");
		submitFileUploadForm();
	});
});

// ファイルアップロード画面Submit
function submitFileUploadForm() {
	var path = window.location.pathname;
	var target = path.substring(path.lastIndexOf("/") + 1);
	$("#upload_form").attr("action", target);
	$("#upload_form").submit();
}
