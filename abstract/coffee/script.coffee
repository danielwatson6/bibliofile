##
## Client-side js (CoffeeScript)
##

# Document-ready function
ready = ->
	
	
# Getter for all of the allowed extensions
get_extensions = ->
	['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']
	
# Method called in template on submit
validate_upload = ->
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

validate_extension = (s) ->
	if s isnt ''
		extension = s.split('.').pop()
		return extension isnt s and get_extensions().indexOf(extension) isnt -1
	return false


# Call the document-ready function
$(document).ready(ready)

# Global
root = exports ? this
root.validate_upload = -> validate_upload()
