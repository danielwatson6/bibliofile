# Extension collections
book_extensions = ['azw', 'azw1', 'azw4', 'epub', 'kf8', 'mobi', 'pdb', 'pdf', 'prc', 'tpz']
img_extensions = ['jpg', 'jpeg', 'gif', 'png']


# Method called in template on submit
validate_upload = ->
	
	# Default fields
	fields = ['#title',
			  '#author',
			  '#genre',
			  '#description',
			  '#author_description',
			  '#blob']
	
	# Special fields
	blob_field = '#blob'
	
	# Check if the default fields are empty
	errors = []
	
	for f in fields
		errors.push(validate_field(f))
	
	# Check if blob is okay
	valid_extension = validate_extension(blob_field, book_extensions)
	
	# Go if no errors are found
	if (e == '' for e in errors) and valid_extension
		return true 
	
	# If not, continue
	$(f + '-error').html(errors.shift()) for f in fields 
	
	# Blob error
	if $(blob_field).val() isnt ''
		$('#blob-error').html('')
		unless valid_extension
			$('#blob-error').html("Please select a file with a valid extension.")
	
	return false


# Given an id and a list of extensions,
# return if it is considered a valid file
validate_extension = (b, extension_list) ->
	s = $(b).val()
	extension = s.split('.').pop()
	return s != '' and extension isnt s and extension_list.indexOf(extension) isnt -1


# Given an id, return error message if necessary
validate_field = (f) ->
	if $(f).val() == ''
		return "This field is empty"
	return ''

# Global variables
root = exports ? this
root.validate_upload = -> validate_upload()
