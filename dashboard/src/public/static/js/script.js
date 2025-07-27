function timeFormating(timestamp) {
    const time = new Date(timestamp);
    return time.getFullYear() + "-" +
        String(time.getMonth() + 1).padStart(2, "0") + "-" +
        String(time.getDate()).padStart(2, "0") + " " +
        String(time.getHours()).padStart(2, "0") + ":" +
        String(time.getMinutes()).padStart(2, "0") + ":" +
        String(time.getSeconds()).padStart(2, "0");
}

document.addEventListener("DOMContentLoaded", function() {
// ======================= 
// NOTIFICATION AT HEADBAR 
// =======================
    const list = document.querySelector("#notifList");
    const data = {};
    fetch(`http://localhost:9000/api/alert/notif?limit=5`)
    .then(res => res.json())
    .then(result => {
        result.data.forEach((alert, index) => {
            const alertTime = new Date(alert.timestamp); // timestamp dari alert
            const now = new Date();

            const diffMs = now - alertTime; // selisih dalam ms

            const diffSec = Math.floor(diffMs / 1000) % 60;
            const diffMin = Math.floor(diffMs / (1000 * 60)) % 60;
            const diffHours = Math.floor(diffMs / (1000 * 60 * 60));

            let diffTimeText;
            if(diffHours - 24 > 0) {
                const hour = diffHours % 24;
                const diffDay = (Math.floor(diffMs / (1000 * 60 * 60 )) - hour)/24;
                diffTimeText = `${diffDay} Days ago`;
            } else if(diffHours - 24 <= 0) {
                diffTimeText = `${diffHours} Hours ${diffMin} Min ago`;
            } else if (diffHours < 1) {
                diffTimeText = `${diffMin} Min ${diffSec} Sec ago`;
            } 
            const divText = `<div class="text-muted small mt-1"> ${diffTimeText} </div>`;

            list.innerHTML += `
            <a href="alert.html" class="list-group-item">
                <div class="row g-0 align-items-center">
                    <div class="col-2">
                        <i class="text-danger" data-feather="alert-circle"></i>
                    </div>
                    <div class="col-10">
                        <div class="text-dark">${alert.topic} Warning</div>
                        <div class="text-muted small mt-1">${alert.message}</div>
                        ${divText}
                    </div>
                </div>
            </a>`;
        });
        const notifHeader = document.getElementById('notifHeader');
        const indicator = document.getElementById('notifIndicator');
        const header = result.meta.count > 0 ? notifHeader.innerHTML = `${result.meta.count} New Notifications` : notifHeader.innerHTML = `No Notifications`;
        const indi = result.meta.count > 0 ? indicator.innerHTML = `<span class="indicator">${result.meta.count}</span>` : indicator.innerHTML = '';
    })
    .catch(err => {
        console.error("Gagal fetch data log:", err);
    });

    let lineChart;
    function loadChart(topic, time, value) {
        let lineMap = {
            temperature : {
                labels: [],
				datasets: [{
					label: "Temperature (°C)",
					fill: true,
					backgroundColor: gradient,
					borderColor: window.theme.primary,
					data: []
				}],
                yText: "Suhu (°C)"
            },
            ph : {
                labels: [],
				datasets: [{
					label: "pH",
					fill: true,
					backgroundColor: "rgba(40, 167, 69, 0.1)",
					borderColor: "green",
					data: []
				}],
                yText: "pH"
            },
            cod : {
                labels: [],
				datasets: [{
				    labels: "COD (mg/l)",
				    fill: true,
				    backgroundColor: "rgba(255, 193, 7, 0.1)",
				    borderColor: "orange",
				    data: [],
                }]
            },
            volume : {
                labels: [],
                datasets: [{
                    label: "Volume Air (L)",
                    fill: true,
                    backgroundColor: "rgba(0, 123, 255, 0.1)",
                    borderColor: "blue",
                    data: []
                }],
                yText: "lIter"
            }
        }
        let chartData = lineMap[topic];
        chartData.labels.push(time);
		chartData.datasets.data.push(value);
        console.log(chartData);
        lineChart = new Chart(document.getElementById(`chartjs-dashboard-${topic}`), {
            type: "line",
            data: {
                labels: [chartData.labels],
                datasets: [chartData.datasets]
            },
            options: {
                maintainAspectRatio: false,
                tooltips: {
                    intersect: false
                },
                hover: {
                    intersect: true
                },
                plugins: {
                    filler: {
                        propagate: false
                    }
                },
                scales: {
                    x: { display: true, title: { display: true, text: "Waktu" } },
                    y: { display: true, title: { display: true, text: chartData.yText } }
                }
            }
        });
    }
})

