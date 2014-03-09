$ ->
	checkfornotice()
	loaddatepicker()

checkfornotice = ->
	if $("#notice_wrapper").length
		$("#notice_wrapper").hide()
		setTimeout (->
			$("#notice_wrapper").slideToggle "fast"
			return
			), 300

		setTimeout (->
			$("#notice_wrapper").slideToggle "fast"
			return
			), ($(".notice").length * 2500)

loaddatepicker = ->
	if $("#id_deploy_date").length
		$("#id_deploy_date").datepicker()