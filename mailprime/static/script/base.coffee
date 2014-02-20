$ ->
	checkfornotice()

checkfornotice = ->
	if $("#error_wrapper").length
		setTimeout (->
			$("#error_wrapper").slideToggle "fast"
			return
			), 3500