(() => {
    const dataElement = document.getElementById("dashboard-data");
    if (!dataElement) {
        return;
    }

    const data = {
        marksLabels: JSON.parse(dataElement.dataset.marksLabels),
        marksValues: JSON.parse(dataElement.dataset.marksValues),
        performanceLabels: JSON.parse(dataElement.dataset.performanceLabels),
        performanceValues: JSON.parse(dataElement.dataset.performanceValues),
    };

    new Chart(document.getElementById("marksChart"), {
        type: "bar",
        data: {
            labels: data.marksLabels,
            datasets: [{
                label: "Final Marks",
                data: data.marksValues,
            }],
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                },
            },
        },
    });

    new Chart(document.getElementById("performanceChart"), {
        type: "pie",
        data: {
            labels: data.performanceLabels,
            datasets: [{
                data: data.performanceValues,
            }],
        },
        options: {
            responsive: true,
        },
    });
})();
