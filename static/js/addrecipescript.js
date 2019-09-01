$(document).ready(function() {

    $('#photo_btn').on('click', function() {
        var url = $('#photo_id').val()
        $('#photo-preview img').prop('src', url);
        $('#photo-preview img').prop('alt', 'Please make sure the URL is correct');
    });

});
