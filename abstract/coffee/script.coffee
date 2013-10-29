##
## Client-side js (CoffeeScript)
##


# Allowed extensions for uploads
EXTENSIONS = ['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']


# Upload validation for client-side
validate_upload = () ->
	title = $('#title')
	blob  = $('#blob')
	
	valid_title = title.val() isnt ''
	valid_blob = blob.val() isnt ''
	valid_extension = validate_extension(blob.val())
	
	return true if valid_title and valid_blob and valid_extension
	
	unless valid_title
		$('#titleError').html("Please add a title.")
	else
		$('#titleError').html("")
	
	unless valid_blob
		$('#blobError').html("Please upload a file.")
	else
		unless valid_extension
			$('#blobError').html("Please select a file with a valid extension.")
		else
			$('#blobError').html("")
	
	return false;

# Check if the extension in the path is valid
validate_extension = () ->
	if s isnt ''
		extension = s.split('.').pop()
		return extension isnt s and EXTENSIONS.indexOf(extension) isnt -1
	return false


# Document-ready
ready = () ->

# Main script
main = (window) ->
	$(document.ready(ready))
	return		# Void

# Call
main(window.jQuery)
