$.ajax({
    url: 'http://127.0.0.1:5000/text-to-speech',  // Local Flask URL
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ text: text, language: language }),
    success: function(response) {
        $('#response-message').html('<p>Text-to-Speech processing complete!</p>');
    },
    error: function(xhr, status, error) {
        let errorMessage = 'An unexpected error occurred.';
        if (xhr.responseJSON && xhr.responseJSON.error) {
            errorMessage = xhr.responseJSON.error;
        }
        console.error("Error Details:", xhr.responseJSON);  // Log detailed error info to console
        $('#response-message').html('<p style="color: red;">Error: ' + errorMessage + '</p>');
    }
});
