$ ->
	checkfornotice()

checkfornotice = ->
	if $("#notice_wrapper").length
		setTimeout (->
			$("#notice_wrapper").slideToggle "fast"
			return
			), 2500