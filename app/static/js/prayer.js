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
        $('#log').prepend($('<li/>').text('Message: ' + msg.message + ' - ' + msg.datetime).html());
    });
    $('form#prayer').submit(function(event) {
        socket.emit('add_prayer', {data: $('#prayer_data').val()});
        return false;
    });
});