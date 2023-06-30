$(document).ready(function() {
	// Searchボタン押下処理
	$("#search").click(function(){
		if ($("#part_code").val() == "" &&
			$("#dept_name").val() == "" &&
			$("#part_name").val() == "" &&
			$("#user_name").val() == "" &&
			$("#eos_from").val() == "" &&
			$("#eos_to").val() == "" )
		{
			alert(msg("CLERR0002"));
			return false;
		} else {
			$("#action_type").val("search");
			$("#search_form").submit();
		}
	});

	// applyボタン押下処理
	$("#apply").click(function(){
		if($('input[name="applyChk"]:checked').length == 0) {
			alert(msg("CLERR0003"));
			return false;
		}
		$("#action_type").val("apply");
		$("#search_form").submit();
	});

	// Checkボタン押下処理
	$("#allCheck").click(function() {
		$('input[name="applyChk"]').prop("checked",true);
	});

	// UnCheckボタン押下処理
	$("#allUncheck").click(function() {
		$('input[name="applyChk"]').prop("checked",false);
	});

	// 参照ボタン（担当部門横）押下処理
	$("#browes_dept").click(function() {
		window.open();
	});

	// クリアボタン（担当部門横）押下処理
	$("#clear_dept").click(function() {
		$('#dept_name').val("");
	});

	// 参照ボタン（担当者横）押下処理
	$("#browes_user").click(function() {
		window.open();
	});

	// クリアボタン（担当者横）押下処理
	$("#clear_user").click(function() {
		$('#user_name').val("");
	});

	$(document).on('click', '.date-picker', function(){
		$(this).datepicker({
			dateFormat: 'yy/mm/dd',
			autoclose: true
		});
		$(this).datepicker('show');
	});

});

