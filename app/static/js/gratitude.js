/**
 * Created by max on 18/4/17.
 */
$(document).ready(function(){
	$("#title, #verse, #gratitude, #log").hide().each(function(i){
		$(this).delay(i*500).fadeIn('slow');
	});
});
$(document).ready(function() {


    namespace = '/gratitude';
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
        twemoji.parse(document.body)
    });
    $('form#gratitude').submit(function(event) {
        socket.emit('add_gratitude', {data: $('#gratitude_data').val()});
        $('#gratitude_data').val('');
        return false;
    });
    twemoji.parse(document.body);
});