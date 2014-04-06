$ ->
	checkfornotice()
	loaddatepicker()
	checkforreport()
	checkcampaigngraph()
	autoadjustiframe()
	checkcampaignlink()
	checknewcampaignlink()

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

checkcampaigngraph = ->

	google.load "visualization", "1",
		packages: ["corechart",]
		callback: populate_campaign_graph

populate_campaign_graph = ->

	if $("#trend_chart").length

		campaign = $("#trend_chart").attr('camp-data')
		username = $("#trend_chart").attr('user-data')

		$.ajax
			type: "GET"
			url: "http://127.0.0.1:8000/api/#{username}/c-#{campaign}/campaign_data.json"
			success: (results) ->

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
		$("#id_deploy_date").datepicker()

checkforreport = ->
	if $(".statistical_frame").length
		google.load "visualization", "1",
			packages: ["geochart", "map", "corechart"]
			callback: populate_report_maps

populate_report_maps = ->
	message = $("#geo_region_map").attr('mess-data')
	username = $("#geo_region_map").attr('user-data')
	campaign = $("#geo_region_map").attr('camp-data')

	$.ajax
		type: "GET"
		url: "http://127.0.0.1:8000/api/#{username}/c-#{campaign}/m-#{message}/region_data.json"
		success: (results) ->

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

autoadjustiframe = ->

	if $(".sample_message").length

		$(".sample_message").each ->
			$(this).load ->
				frame_height = $(this).contents().find("html").height()
				$(this).height(frame_height)

checkcampaignlink = ->
	if $(".campaign_wrapper").length
		$(".campaign_wrapper").each ->
			link = $(this).attr("data-link")
			$(this).click ->
				window.location.href = link

checknewcampaignlink = ->
	if $("#add_campaign_button").length
		$("#add_campaign_button").each ->
			link = $(this).attr("data-link")
			$(this).click ->
				window.location.href = link

adjust_chart_width = ->
	$("#trend_chart").width('100%')