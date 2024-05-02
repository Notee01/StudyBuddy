window.addEventListener("DOMContentLoaded", (event) => {
    const surveyForm = document.getElementById("surveyForm");
    const url = window.location.href;
    surveyForm.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevents the default form submission behavior

        // Serialize form data
        var formData = $(this).serializeArray();
        console.log(url)
        // Send form data using AJAX
        $.ajax({
            type: "POST",
            url: `${url}submit`,// Replace with your URL endpoint
            data: formData,
            success: function(response) {
                // Handle successful response
                console.log(response);
            },
            error: function(xhr, status, error) {
                // Handle errors
                console.error(xhr.responseText);
            }
        });
    });
});
