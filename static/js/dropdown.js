document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.getElementById('show-input');
    const dropdown = document.getElementById('dropdown');
    let titles = [];

    // Fetch available anime
    fetch('/get-shows')
        .then(response => response.json())
        .then(data => {
            titles = data.titles;  // Store the available anime
            console.log("Number of titles: " + titles.length); // Log the number of titles available to the dropdown
        })
        .catch(error => console.error('Error fetching shows:', error));

    // Function to filter the available shows based on user input
    function filterShows() {
        const query = inputField.value.toLowerCase();
        dropdown.innerHTML = ''; // Clear previous results

        // Filter the shows based on the input
        const filteredShows = titles.filter(show => show.toLowerCase().includes(query));

        // Display the filtered shows in the dropdown
        filteredShows.forEach(show => {
            const div = document.createElement('div');
            div.textContent = show;
            div.classList.add('dropdown-item');
            div.addEventListener('click', () => {
                // When the user clicks a show, set it to the hidden input and submit the form
                event.preventDefault()
                document.getElementById('watched-show').value = show;
                document.getElementById('showForm').submit();
            });
            dropdown.appendChild(div);
        });

        // Show or hide the dropdown based on results
        dropdown.style.display = filteredShows.length ? 'block' : 'none';
    }

    // Event listener for input field
    inputField.addEventListener('input', filterShows);

    // Hide the dropdown if the input loses focus
    inputField.addEventListener('blur', () => {
        setTimeout(() => { dropdown.style.display = 'none'; }, 200); // Timeout to allow click
    });

    // Show the dropdown when the input gains focus
    inputField.addEventListener('focus', filterShows);
});
