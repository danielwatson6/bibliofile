# RESTful methods
$ ->
	$('[data-method]').click ->
		$('body').append(
			$('<form></form>')
			.attr('method', 'POST')
			.attr('id', '_form')
			.attr('action', $(this).data('action'))
			.append($('<input>')
	  	    	.attr('type', 'hidden')
	        	.attr('name', '_method')
	        	.attr('value', $(this).data('method'))
			)
		)
		$('#_form').submit()
