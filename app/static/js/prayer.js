/**
 * Created by max on 19/4/17.
 */
$(document).ready(function(){
	$("#title, #verse, #prayer, #log").hide().each(function(i){
		$(this).delay(i*400).fadeIn(400);
	});
});
$(document).ready(function() {

    namespace = '/prayer';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('my_event', {data: true});
    });
    socket.on('my_response', function(msg) {
        var item = document.createElement('div');
        item.className = "message";
        var content = document.createElement('p');
        content.className = "content";
        var date = document.createElement('p');
        date.className = "date";
        var content_text = document.createTextNode('"' + msg.message + '"');
        content.appendChild(content_text);
        var date_text = document.createTextNode(msg.datetime);
        date.appendChild(date_text);
        item.appendChild(content);
        item.appendChild(date);
        $(item).hide().prependTo('#log').fadeIn('slow');
    });
    $('form#prayer').submit(function(event) {
        socket.emit('add_prayer', {data: $('#prayer_data').val()});
        $('#prayer_data').val('');
        return false;
    });
});