/**
 * Javascript is wrapped in this
 * self-calling function to avoid
 * external tampering with the
 * undefined value.
 **/
!function (window, undefined) {
	
	$(document).ready(function () {
		// jQuery and continous methods
	});
	
	// Normal javascript

}(window.jQuery);

// Validation on front-side
function validate_upload() {
	
	var title = $('#title');
	var blob = $('#blob');
	
	if (title.val() != '' && blob.val() != '') {
		return true;
	}
	
	// Add error messages
	if (!title.val()) {
		$('#titleError').html("Please add a title.");
	} else {
		$('#titleError').html("");
	}
	if (!blob.val()) {
		$('#blobError').html("Please upload a file.");
	} else {
		$('#blobError').html("");
	}
	
	return false;
}
