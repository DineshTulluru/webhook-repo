function fetchEvents() {
    fetch('/events')
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("event-list");
            list.innerHTML = "";
            data.forEach(e => {
                const li = document.createElement("li");
                li.textContent = e.message;
                list.appendChild(li);
            });
        });
}

fetchEvents();
setInterval(fetchEvents, 15000);