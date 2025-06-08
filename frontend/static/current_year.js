function current_year() {
    var thisYear = new Date().getFullYear();
    var element = document.getElementById("current_year");

    if (!element) return;

    if (thisYear > 2025) {
        element.textContent = `2025 - ${thisYear}`;
    } else {
        element.textContent = thisYear;
    }
}

window.addEventListener("DOMContentLoaded", current_year);
