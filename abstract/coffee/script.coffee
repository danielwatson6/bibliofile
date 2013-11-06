##
## Client-side js (CoffeeScript)
##

# Document-ready function
ready = ->
	#

# Extension collections
book_extensions = ['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']
img_extensions = ['jpg', 'jpeg', 'gif', 'png']


# Method called in template on submit
validate_upload = ->
	
	# Regular fields
	fields = [$('#title'),
			  $('#author'),
			  $('#genre'),
			  $('#description'),
			  $('#info_description'),
			  $('#author_description'),
			  $('#blob')]
	
	# Special fields
	blob = $('#blob')
	
	# Check if the regular fields are empty
	range = [0...fields.length]
	errors = []
	for i in range
		if fields[i].val() == ''
			errors[i] = "This field is empty."
		else
			errors[i] = ''
	
	# Check if blob is okay
	valid_extension = validate_extension(blob.val(), book_extensions)
	
	# Go if no errors are found
	return true if errors == ['' for i in range] and valid_extension
	
	
	# If not, send errors back
	$('#error'+i).html(errors[i]) for i in range
	
	if blob.val() isnt ''
		$('.blob-error').html('')
		unless valid_extension
			$('.blob-error').html("Please select a file with a valid extension.")
	
	return false


# Given a string and a list of extensions,
# return if it is considered a valid file
validate_extension = (s, extension_list) ->
	return false if s == ''
	extension = s.split('.').pop()
	return extension isnt s and extension_list.indexOf(extension) isnt -1


# Call the document-ready function
$(document).ready(ready)

# Global variables
root = exports ? this
root.validate_upload = -> validate_upload()

