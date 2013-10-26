/**
 * Javascript is wrapped in this
 * self-calling function to avoid
 * external tampering with the
 * undefined value.
 **/
 
// Extensions allowed in blob uploads
// These are based on e-book formats
EXTENSIONS = ['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']
 
 
!function (window, undefined) {
	
	$(document).ready(function () {
		// jQuery and continous methods
	});
	
	// Normal javascript

}(window.jQuery);

// Validation on front-side
function validate_upload() {
	
	var title = $('#title');
	var blob  = $('#blob');
	
	title_test = title.val() != ''
	blob_test = blob.val() != ''
	extension_test =  test_extension(blob.val())
	
	if (title_test && blob_test && extension_test) {
		return true;
	}
	
	// Add error messages
	if (!title_test) {
		$('#titleError').html("Please add a title.");
	} else {
		$('#titleError').html("");
	}
	if (!blob_test) {
		$('#blobError').html("Please upload a file.");
	} else {
		if (!extension_test) {
			$('#blobError').html("Please select a file with a valid extension.");
		} else {
			$('#blobError').html("");
		}
	}
	
	return false;
}

function test_extension(s) {
	if (s != undefined && s != '' && s != null) {
		extension = s.split('.')[s.split('.').length-1];
		for (var i = 0; i < EXTENSIONS.length; i++) {
			if (EXTENSIONS[i] == extension) {
				return true;
			}
		}
		return false;
	} else {
		return false;
	}
}
