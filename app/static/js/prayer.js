/**
 * Created by max on 19/4/17.
 */

$(document).ready(function() {

    namespace = '/prayer';
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
    $('form#prayer').submit(function(event) {
        socket.emit('add_prayer', {data: $('#prayer_data').val()});
        return false;
    });
});