$ ->
	checkfornotice()
	loaddatepicker()
	checkformap()

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

checkformap = ->
	if $("#geo_region_map").length
		google.load "visualization", "1",
			packages: ["geochart"]
			callback: populate_region_map

populate_region_map = ->
	message = $("#geo_region_map").attr('mess-data')
	username = $("#geo_region_map").attr('user-data')
	campaign = $("#geo_region_map").attr('camp-data')

	$.ajax
		type: "GET"
		url: "http://127.0.0.1:8000/api/#{username}/c-#{campaign}/m-#{message}/region_data.json"
		success: (results) ->
			options = { width: 500, height: 500}
			data = google.visualization.arrayToDataTable(results)
			chart = new google.visualization.GeoChart(document.getElementById('geo_region_map'))
			chart.draw(data, options)
			return