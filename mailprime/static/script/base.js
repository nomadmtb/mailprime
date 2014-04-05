// Generated by CoffeeScript 1.6.3
var autoadjustiframe, checkcampaignlink, checkfornotice, checkforreport, checknewcampaignlink, loaddatepicker, populate_report_maps;

$(function() {
  checkfornotice();
  loaddatepicker();
  checkforreport();
  autoadjustiframe();
  checkcampaignlink();
  return checknewcampaignlink();
});

checkfornotice = function() {
  if ($("#notice_wrapper").length) {
    $("#notice_wrapper").hide();
    setTimeout((function() {
      $("#notice_wrapper").slideToggle("fast");
    }), 300);
    return setTimeout((function() {
      $("#notice_wrapper").slideToggle("fast");
    }), $(".notice").length * 2500);
  }
};

loaddatepicker = function() {
  if ($("#id_deploy_date").length) {
    return $("#id_deploy_date").datepicker();
  }
};

checkforreport = function() {
  if ($(".statistical_frame").length) {
    return google.load("visualization", "1", {
      packages: ["geochart", "map", "corechart"],
      callback: populate_report_maps
    });
  }
};

populate_report_maps = function() {
  var campaign, message, username;
  message = $("#geo_region_map").attr('mess-data');
  username = $("#geo_region_map").attr('user-data');
  campaign = $("#geo_region_map").attr('camp-data');
  return $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/api/" + username + "/c-" + campaign + "/m-" + message + "/region_data.json",
    success: function(results) {
      var coord_data, coord_map, coord_options, region_data, region_map, region_options, response_data, response_graph, response_options, trend_chart, trend_data, trend_options, weekday_data, weekday_graph, weekday_options;
      trend_options = {
        curveType: 'function',
        legend: {
          position: 'bottom',
          alignment: 'center',
          textStyle: {
            color: '#525453'
          }
        }
      };
      region_options = {
        width: 670,
        height: 500,
        colorAxis: {
          minValue: 0,
          colors: ['#578EA9']
        }
      };
      coord_options = {
        showTip: true,
        enableScrollWheel: false,
        mapType: 'normal'
      };
      response_options = {
        pieHole: 0.5,
        legend: {
          position: 'top',
          alignment: 'center',
          maxLines: 2,
          textStyle: {
            color: '#525453'
          }
        },
        chartArea: {
          left: 55,
          top: 65
        },
        colors: ['#7CCBF2', '#BED9E6', '#DDE8EE', '#3E6679', '#00FF99', '#FF6666', '#FF9933']
      };
      weekday_options = {
        pieHole: 0.5,
        legend: {
          position: 'top',
          alignment: 'center',
          maxLines: 2,
          textStyle: {
            color: '#525453'
          }
        },
        chartArea: {
          left: 55,
          top: 65
        },
        colors: ['#7CCBF2', '#BED9E6', '#DDE8EE', '#3E6679', '#00FF99', '#FF6666', '#FF9933']
      };
      trend_data = google.visualization.arrayToDataTable(results['read_by_day_data']);
      trend_chart = new google.visualization.LineChart(document.getElementById('trend_chart'));
      weekday_data = google.visualization.arrayToDataTable(results['weekday_data']);
      weekday_graph = new google.visualization.PieChart(document.getElementById('weekday_chart'));
      response_data = google.visualization.arrayToDataTable(results['response_data']);
      response_graph = new google.visualization.PieChart(document.getElementById('percent_response_chart'));
      region_data = google.visualization.arrayToDataTable(results['region_data']);
      region_map = new google.visualization.GeoChart(document.getElementById('geo_region_map'));
      coord_data = google.visualization.arrayToDataTable(results['coordinate_data']);
      coord_map = new google.visualization.Map(document.getElementById('coord_map'));
      trend_chart.draw(trend_data, trend_options);
      weekday_graph.draw(weekday_data, weekday_options);
      response_graph.draw(response_data, response_options);
      region_map.draw(region_data, region_options);
      return coord_map.draw(coord_data, coord_options);
    }
  });
};

autoadjustiframe = function() {
  if ($(".sample_message").length) {
    return $(".sample_message").each(function() {
      return $(this).load(function() {
        var frame_height;
        frame_height = $(this).contents().find("html").height();
        return $(this).height(frame_height);
      });
    });
  }
};

checkcampaignlink = function() {
  if ($(".campaign_wrapper").length) {
    return $(".campaign_wrapper").each(function() {
      var link;
      link = $(this).attr("data-link");
      return $(this).click(function() {
        return window.location.href = link;
      });
    });
  }
};

checknewcampaignlink = function() {
  if ($("#add_campaign_button").length) {
    return $("#add_campaign_button").each(function() {
      var link;
      link = $(this).attr("data-link");
      return $(this).click(function() {
        return window.location.href = link;
      });
    });
  }
};
