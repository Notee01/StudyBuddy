function liveSearchAndFilter() {
    var input, filter, table, tr, td, i, txtValue, categoryFilter, typeFilter;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("materialsTable");
    tr = table.getElementsByTagName("tr");
    categoryFilter = document.getElementById("categoryFilter").value;
    typeFilter = document.getElementById("typeFilter").value;
    var visibleRowCount = 0; // Variable to count visible rows
    var totalRowHeight = 0; // Variable to accumulate total row height
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1]; // Index 1 for title column, adjust as needed
        var category = tr[i].getAttribute("data-category");
        var type = tr[i].getAttribute("data-type");
        if (td) {
            txtValue = td.textContent || td.innerText;
            if ((txtValue.toUpperCase().indexOf(filter) > -1) &&
                (categoryFilter == "" || category == categoryFilter) &&
                (typeFilter == "" || type == typeFilter)) {
                tr[i].style.display = ""; // Show row if it matches filter
                visibleRowCount++; // Increment visible row count
                totalRowHeight += tr[i].offsetHeight; // Accumulate row height
            } else {
                tr[i].style.display = "none"; // Hide row if it doesn't match filter
            }
        }
    }

    // Adjust the height of the table container div
    var tableContainer = document.getElementById("tableContainer");
    var resultsContainer = document.querySelector(".md\\:inset-y-15");
    if (visibleRowCount > 0) {  
        resultsContainer.classList.remove('hidden');
        resultsContainer.classList.add('md:inset-y-auto'); // Show results container
        var rowHeight = totalRowHeight / visibleRowCount;
        var maxHeight = Math.min(500, rowHeight * visibleRowCount);
        resultsContainer.style.maxHeight = maxHeight + "px"; // Set max height of results container
    } else {
        resultsContainer.classList.add('hidden'); // Hide results container if no rows are visible
    }
}

// Attach keyup event listener to search input
document.getElementById("searchInput").addEventListener("keyup", liveSearchAndFilter);

// Attach change event listeners to category and type filters
document.getElementById("categoryFilter").addEventListener("change", liveSearchAndFilter);
document.getElementById("typeFilter").addEventListener("change", liveSearchAndFilter);
