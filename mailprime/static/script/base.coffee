$ ->
	checkfornotice()
	loaddatepicker()
	check_for_message_report()
	check_for_campaign_graph()
	auto_adjust_iframe()
	toggle_iframe()
	check_campaign_link()
	check_for_slick()
	check_read_event_map()

checkfornotice = ->
	if $("#notice_wrapper").length
		$("#notice_wrapper").hide()
		setTimeout (->
			$("#notice_wrapper").slideToggle('3500',"easeOutBounce")
			return
			), 300

		setTimeout (->
			$("#notice_wrapper").slideToggle('3500',"easeOutBounce")
			return
			), ($(".notice").length * 2500)

check_for_campaign_graph = ->
	if $('#generate_campaign_graph').length
		google.load "visualization", "1",
			packages: ["corechart",]
			callback: populate_campaign_graph

populate_campaign_graph = ->
	if $("#trend_chart").length

		campaign = $("#trend_chart").attr('camp-data')
		username = $("#trend_chart").attr('user-data')

		$.ajax
			type: "GET"
			url: "/api/#{username}/c-#{campaign}/campaign_data.json"
			success: (results) ->

				if results.hasOwnProperty('ERROR')
					$("#trend_chart").css('background-color', '#C00000')
					$("#percent_response_chart").css('background-color', '#C00000')
					$("#weekday_chart").css('background-color', '#C00000')
					$("#geo_region_map").css('background-color', '#C00000')
					$("#coord_map").css('background-color', '#C00000')

					$(".solid_bg:first").prepend("<h1 id='data_error'>ERROR, No Tracking Data Available Yet</h1>")

				else

					trend_options = {
						curveType: 'function',
						legend: {
							position: 'bottom',
							alignment: 'center',
							textStyle: {
								color: '#525453',
							}
						}
					}

					event_data = google.visualization.arrayToDataTable(results['read_by_day_data'])
					adjust_chart_width()
					trend_chart = new google.visualization.LineChart(document.getElementById('trend_chart'))
					trend_chart.draw(event_data, trend_options)

loaddatepicker = ->
	if $("#id_deploy_date").length
		$("#id_deploy_date").datepicker( { dateFormat: 'yy-mm-dd', })

check_for_message_report = ->
	if $("#generate_message_report").length
		google.load "visualization", "1",
			packages: ["geochart", "map", "corechart"]
			callback: populate_message_report_maps

check_read_event_map = ->
	if $("#read_event_map_canvas").length

		google.load "visualization", "1",
			packages: ["map"]
			callback: populate_read_event_map

populate_read_event_map = ->
	message = $("#read_event_map_canvas").attr('mess-data')
	username = $("#read_event_map_canvas").attr('user-data')
	campaign = $("#read_event_map_canvas").attr('camp-data')

	$.ajax
		type: "GET"
		url: "/api/#{username}/c-#{campaign}/m-#{message}/region_data.json"
		success: (results) ->

			if results.hasOwnProperty('ERROR')

				$("#read_event_map_canvas").css('background-color', '#C00000')
				$(".solid_bg").prepend("<h1 id='data_error'>ERROR, No Tracking Data Available Yet</h1>")

			else

				coord_options = {
					showTip: true
					enableScrollWheel: false
					mapType: 'normal'
				}

				coord_data = google.visualization.arrayToDataTable(results['coordinate_data'])
				coord_map = new google.visualization.Map(document.getElementById('read_event_map_canvas'))

				coord_map.draw(coord_data, coord_options)






populate_message_report_maps = ->
	message = $("#geo_region_map").attr('mess-data')
	username = $("#geo_region_map").attr('user-data')
	campaign = $("#geo_region_map").attr('camp-data')

	$.ajax
		type: "GET"
		url: "/api/#{username}/c-#{campaign}/m-#{message}/region_data.json"
		success: (results) ->

			if results.hasOwnProperty('ERROR')
				$("#trend_chart").css('background-color', '#C00000')
				$("#percent_response_chart").css('background-color', '#C00000')
				$("#weekday_chart").css('background-color', '#C00000')
				$("#geo_region_map").css('background-color', '#C00000')
				$("#coord_map").css('background-color', '#C00000')

				$(".solid_bg").prepend("<h1 id='data_error'>ERROR, No Tracking Data Available Yet</h1>")

			else

				trend_options = {
					curveType: 'function',
					legend: {
						position: 'bottom',
						alignment: 'center',
						textStyle: {
							color: '#525453',
						}
					}
				}

				region_options = {
					width: 670,
					height: 500,
					colorAxis: {minValue: 0, colors: ['#578EA9']}
				}

				coord_options = {
					showTip: true
					enableScrollWheel: false
					mapType: 'normal'
				}

				response_options = {
					pieHole: 0.5,
					legend: {
						position: 'top',
						alignment: 'center',
						maxLines: 2,
						textStyle: {
							color: '#525453',
						}
					}
					chartArea: {
						left: 55,
						top: 65,
					}
					colors: [
						'#7CCBF2', '#BED9E6', '#DDE8EE', '#3E6679', '#00FF99', '#FF6666', '#FF9933'
					]
				}

				weekday_options = {
					pieHole: 0.5,
					legend: {
						position: 'top',
						alignment: 'center',
						maxLines: 2,
						textStyle: {
							color: '#525453',
						}
					}
					chartArea: {
						left: 55,
						top: 65,
					}
					colors: [
						'#7CCBF2', '#BED9E6', '#DDE8EE', '#3E6679', '#00FF99', '#FF6666', '#FF9933'
					]
				}

				trend_data = google.visualization.arrayToDataTable(results['read_by_day_data'])
				adjust_chart_width()
				trend_chart = new google.visualization.LineChart(document.getElementById('trend_chart'))

				weekday_data = google.visualization.arrayToDataTable(results['weekday_data'])
				weekday_graph = new google.visualization.PieChart(document.getElementById('weekday_chart'))

				response_data = google.visualization.arrayToDataTable(results['response_data'])
				response_graph = new google.visualization.PieChart(document.getElementById('percent_response_chart'))

				region_data = google.visualization.arrayToDataTable(results['region_data'])
				region_map = new google.visualization.GeoChart(document.getElementById('geo_region_map'))

				coord_data = google.visualization.arrayToDataTable(results['coordinate_data'])
				coord_map = new google.visualization.Map(document.getElementById('coord_map'))

				trend_chart.draw(trend_data, trend_options)
				weekday_graph.draw(weekday_data, weekday_options)
				response_graph.draw(response_data, response_options)
				region_map.draw(region_data, region_options)
				coord_map.draw(coord_data, coord_options)

auto_adjust_iframe = ->
	if $(".sample_message").length
		$(".sample_message").each ->
			$(this).load ->
				frame_height = $(this).contents().find("html").height()
				$(this).height(frame_height)

toggle_iframe = ->
	if $(".sample_message").length
		$("#sample_message_toggle").click ->
			$(".sample_message").slideToggle('3500',"easeOutBounce")

check_campaign_link = ->
	if $(".campaign_wrapper").length
		$(".campaign_wrapper").each ->
			link = $(this).attr("data-link")
			$(this).click ->
				window.location.href = link
				
	if $("#add_campaign_button").length
		check_new_campaign_link()

check_new_campaign_link = ->
	if $("#add_campaign_button").length
		$("#add_campaign_button").each ->
			link = $(this).attr("data-link")
			$(this).click ->
				window.location.href = link

adjust_chart_width = ->
	$("#trend_chart").width('100%')

check_for_slick = ->
	if $("#slick_wrapper").length
		$("#slick_wrapper").slick(
			centerMode: true,
			centerPadding: '25px',
			dots: true,
			slidesToShow: 3,)