function createSignal(signalState, countdown) {

    return `
        <div class="light red ${signalState === "RED" ? "active" : ""}"></div>
        <div class="light yellow ${signalState === "YELLOW" ? "active" : ""}"></div>
        <div class="light green ${signalState === "GREEN" ? "active" : ""}"></div>
        <div class="countdown">${signalState === "GREEN" ? countdown + " sec" : ""}</div>
    `;
}

function updateSignals() {
    fetch("/status")
        .then(res => res.json())
        .then(data => {

            for (let i = 0; i < 4; i++) {
                let countdown = (data.active_junction === i) ? data.countdown : "";
                document.getElementById("j" + i).innerHTML =
                    "<h3>Junction " + (i+1) + "</h3>" +
                    createSignal(data.signals[i], countdown);
            }
        });
}

setInterval(updateSignals, 1000);