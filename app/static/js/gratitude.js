/**
 * Created by max on 18/4/17.
 */

$(document).ready(function() {

    namespace = '/gratitude';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('my_event', {data: true});
    });
    socket.on('my_response', function(msg) {
        var item = document.createElement('li');
        var text = document.createTextNode('Message: ' + msg.message + ' - ' + msg.datetime);
        item.appendChild(text);
        $('#log').prepend(item);
    });
    $('form#gratitude').submit(function(event) {
        socket.emit('add_gratitude', {data: $('#gratitude_data').val()});
        return false;
    });
});