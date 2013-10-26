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
	
	valid_title = title.val() !== ''
	valid_blob = blob.val() !== ''
	valid_extension =  validate_extension(blob.val())
	
	if (valid_title && valid_blob && valid_extension) {
		return true;
	}
	
	// Add error messages
	if (!valid_title) {
		$('#titleError').html("Please add a title.");
	} else {
		$('#titleError').html("");
	}
	if (!valid_blob) {
		$('#blobError').html("Please upload a file.");
	} else {
		if (!valid_extension) {
			$('#blobError').html("Please select a file with a valid extension.");
		} else {
			$('#blobError').html("");
		}
	}
	
	return false;
}

// Check if the extension in the path is valid
function validate_extension(s) {
	if (s !== '') {
		extension = s.split('.').pop()
		return extension !== s && EXTENSIONS.indexOf(extension) !== -1;	
	} else {
		return false;
	}
}
