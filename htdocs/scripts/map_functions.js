//credit to user joQuery for String.format
String.format = function(){
	
	var string_arg = arguments[0];
	
	for(var i = 1; i < arguments.length; i++){
		var regEx = new RegExp("\\{" + (i - 1) + "\\}", "gm");
		string_arg = string_arg.replace(regEx, arguments[i]);
	}
	return string_arg;
}

function city(id){
	this.name = "";
	this.id = id;
	this.map_id = String.format("map{0}",id); 
	this.map = null;
	this.station_layers = new L.LayerGroup();
	this.trip_layers = new L.LayerGroup();
	this.stations = {};
	this.trips = {};	
}

function changeCity(city){

	var newCity = document.getElementById(String.format('city{0}_options',city['id'])).value;
	if(newCity != ""){
		updateMap(city, cities[newCity]);
	}
}

function updateMap(city, city_info){
	city['name'] = city_info['name'];
	document.getElementById(String.format('city{0}_filters_msg',city['id'])).innerHTML = "Filters: " + city_info["print_filters"];
	city['map'].setView(city_info['LatLng'], city_info['zoom']);
	city['map'].addLayer(new L.StamenTileLayer("terrain-lines"));
	var start_datepicker = String.format('#start-date{0}',city['id']);
	var end_datepicker = String.format('#end-date{0}',city['id']);
	var start_date = city_info['start-date'], end_date = city_info['end-date'];

	$(start_datepicker).datepicker("option", {minDate: start_date, maxDate : end_date});
	$(start_datepicker).datepicker("setDate", start_date);
	$(end_datepicker).datepicker("option", {minDate: start_date, maxDate: end_date});
	$(end_datepicker).datepicker("setDate", end_date);
	
	var stations = {};

	$.getJSON(city_info['stations'],function(){
	})
	  .done(function(data) {
		  $.each(data, function(i, station){
			  stations[station.st_id] = station;
			  stations[station.st_id]['startTotal'] = 0;
			  stations[station.st_id]['endTotal'] = 0;
		  });
		  city['stations'] = stations;
		  updateTrips(city);
		  drawStations(city); 
	  })
	  .fail(function() {
	    console.log( "error getting station/trip information" );
	  });
	
}


function viewTrips(){
	updateTrips(city1);
	drawStations(city1); 
	updateTrips(city2);
	drawStations(city2); 
}


function drawStations(city){
	var stations = city['stations'];
	city['station_layers'].clearLayers();
	var station_layers = new L.LayerGroup();
	var maxWeight = 0;
	var stationColor = '#000000';
	var colorScale = d3.scale.linear()
    .domain([0, 1])
    .range(["red", "blue"]);
	$.each(stations, function(i){
		var station = stations[i];
		maxWeight += station.startTotal + station.endTotal;
	})
	// console.log("maxWeight: " + maxWeight);
	if(maxWeight > 0){
		var weightRange = d3.scale.log().clamp(true).domain([0.1,maxWeight]).range([5,120]);
		$.each(stations, function(i){
		   var station = stations[i];
		   var totalTrips = station.startTotal + station.endTotal;
		   if(totalTrips > 0){
				stationColor = colorScale(station.startTotal / totalTrips);
				}
		   else{
			   stationColor = '#000000';
		   }
		   var circle = L.circle([station.st_lat, station.st_long], weightRange(totalTrips), {
		       color: stationColor,
		       fillColor: stationColor,
		       opacity: 0.8,
		       fillOpacity: 1
		    });
			circle.bindPopup(station.st_name + "<br/># Incoming Trips: " + station.endTotal + "<br/># Outgoing Trips: " + station.startTotal);
			station_layers.addLayer(circle);
		});
		
	}
	else{
		$.each(stations, function(i){
			   var station = stations[i];
			   var circle = L.circle([station.st_lat, station.st_long], 10, {
			       color: '#000000',
			       fillColor: '#000000',
			       opacity: 0.8,
			       fillOpacity: 1
			   });	
			   circle.bindPopup(station.st_name + "<br/># Incoming Trips: 0<br/># Outgoing Trips: 0");
			   station_layers.addLayer(circle);
		});
	}
	city['station_layers'] = station_layers;
	station_layers.addTo(city['map']);
}
    
/*function drawTrips(city, maxWeight){
	city['trip_layers'].clearLayers();
	var trips = city['trips'];
	var trip_layers = new L.LayerGroup();
	var stations = city['stations'];
	var num_trips = Object.keys(trips).length;	
	var lowBound = 50 / num_trips;
	var highBound = 500 / num_trips;
	var weightRange = d3.scale.log()
						.domain([0,maxWeight])
						.range([lowBound, highBound]);
	var tripColors = d3.scale.ordinal()
	.domain([0,maxWeight])
    .range(colorbrewer.Blues[9]);
	
	$.each(trips, function(start_st_id, end_st_ids){
		if(start_st_id != ""){
			var start_station = stations[start_st_id];
			var st_latlong = L.latLng(start_station.st_lat, start_station.st_long);
			$.each(end_st_ids, function(end_st_id, weight){
				if(end_st_id != ""){
					var end_station = stations[end_st_id];
					var end_latlong = L.latLng(end_station.st_lat, end_station.st_long);
					var tripWeight = trips[start_st_id][end_st_id];
					var trip = L.polyline([st_latlong, end_latlong], 
							{color: tripColors(tripWeight),
							weight: weightRange(tripWeight)});
					trip_layers.addLayer(trip);
				}
			})
		}
	});
	city['trip_layers'] = trip_layers;
	trip_layers.addTo(city['map']);
}
*/