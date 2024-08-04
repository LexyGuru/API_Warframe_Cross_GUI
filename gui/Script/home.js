document.addEventListener("DOMContentLoaded", function() {
    // Function to display the current date and time
    function displayDateTime() {
        const now = new Date();
        const dateTimeString = now.toLocaleString();
        document.getElementById("datetime").textContent = dateTimeString;
    }

    // Display the date and time immediately
    displayDateTime();
    // Update the date and time every second
    setInterval(displayDateTime, 1000);

});

