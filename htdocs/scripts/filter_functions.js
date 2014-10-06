//functions for parameter filtering/sending

//prototype suggestion, function from StackOverflow
/*Number.prototype.SecondstoTime = function(){
	var sec_num = parseInt(this, 10);
	var hours = Math.floor(sec_num/3600);
	var minutes = Math.floor((sec_num - (hours*3600))/60);
	var seconds = sec_num - (hours*3600) - (minutes*60);

	if(hours < 10){hours = "0" + hours;}
	if(minutes < 10){minutes = "0" + minutes;}
	if(seconds < 10){seconds = "0" + seconds;}
	
	var time = hours + ":" + minutes + ":" + seconds;
	return time;
};*/

Number.prototype.SecondstoDuration = function(){
	var sec_num = parseInt(this, 10);
	var days = Math.floor(sec_num/86400);
	var hours = Math.floor((sec_num - (days*86400))/3600);
	var minutes = Math.floor((sec_num - (days*86400) - (hours*3600))/60);
	
	if(hours < 10){hours = " " + hours;}
	if(minutes < 10){minutes = " " + minutes;}
	
	var time = days + "d" + hours + "h" + minutes + "m";
	return time;
};

$.widget( "ui.timespinner", $.ui.spinner, {
    options: {
      // seconds
      step: 60 * 1000,
      // hours
      page: 60
    },
 
    _parse: function( value ) {
      if ( typeof value === "string" ) {
        // already a timestamp
        if ( Number( value ) == value ) {
          return Number( value );
        }
        return +Globalize.parseDate( value );
      }
      return value;
    },
 
    _format: function( value ) {
      return Globalize.format( new Date(value), "t" );
    }
  });

DurationtoSeconds = function(duration){
	duration = duration.replace(/\s+/g, '');
	var duration_array = duration.split(/[dhm]/);
	return parseInt(duration_array[0], 10)*86400 + parseInt(duration_array[1], 10)*3600 + parseInt(duration_array[2], 10)*60;
}

$( "#start-date1").datepicker({dateFormat: "yy-mm-dd", autoSize: true, 
	minDate: "2011-07-28", maxDate: "2012-10-01", defaultDate: "2011-07-28", 
	onClose: function(start_date, datepicker){
		$( "#end-date1" ).datepicker( "option", "minDate", start_date);
	}});

$( "#end-date1").datepicker({dateFormat: "yy-mm-dd", autoSize: true, 
	minDate: "2011-07-28", maxDate: "2012-10-01", defaultDate: "2012-10-01",
	onClose: function(end_date, datepicker){
		$( "#start-date1" ).datepicker( "option", "maxDate", end_date);
	}});

Globalize.culture('de-DE');

$("#time-start1" ).timespinner();
$("#time-start1").timespinner("value", '0:00');
$("#time-end1" ).timespinner();
$("#time-end1").timespinner("value", '23:59');


$( "#start-date2").datepicker({dateFormat: "yy-mm-dd", autoSize: true, 
	minDate: "2011-01-01", maxDate: "2011-12-31", defaultDate: "2011-01-01", 
	onClose: function(start_date, datepicker){
		$( "#end-date2" ).datepicker( "option", "minDate", start_date);
	}});

$( "#end-date2").datepicker({dateFormat: "yy-mm-dd", autoSize: true, 
	minDate: "2011-01-01", maxDate: "2011-12-31", defaultDate: "2011-12-31",
	onClose: function(end_date, datepicker){
		$( "#start-date2" ).datepicker( "option", "maxDate", end_date);
	}});

$("#time-start2").timespinner();
$("#time-start2").timespinner("value", '0:00');
$("#time-end2").timespinner();
$("#time-end2").timespinner("value", '23:59');

$("#duration-range").slider({
	range: true,
	min: 0,
	max: 86400,
	values: [0, 86400],
	slide: function(event, ui) {
		$("#duration-start").val(ui.values[0].SecondstoDuration());
		$("#duration-end").val(ui.values[1].SecondstoDuration());
	}
});

$( "#duration-start" ).val( $( "#duration-range" ).slider( "values", 0 ).SecondstoDuration() );
$( "#duration-end" ).val( $( "#duration-range" ).slider( "values", 1 ).SecondstoDuration() );

$("#birthyear-range").slider({
	range: true,
	min: 1932,
	max: 1995,
	values: [1932, 1995],
	slide: function(event, ui) {
		$("#birthyear-start").val(ui.values[0]);
		$("#birthyear-end").val(ui.values[1]);
}
});
$( "#birthyear-start" ).val( $( "#birthyear-range" ).slider( "values", 0 ));
$( "#birthyear-end" ).val( $( "#birthyear-range" ).slider( "values", 1 ));

$(function() {
    $( "#tabs" ).tabs();
  });

