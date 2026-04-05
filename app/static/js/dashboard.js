(() => {
    const config = window.OptiFleetDashboard;
    if (!config) {
        return;
    }

    const chartContext = document.getElementById("dashboardChart");
    let chart;

    const renderChart = (rows) => {
        if (!chartContext) {
            return;
        }

        if (chart) {
            chart.destroy();
        }

        chart = new Chart(chartContext, {
            type: "bar",
            data: {
                labels: rows.map((row) => row.status),
                datasets: [{
                    label: "Orders",
                    data: rows.map((row) => row.count),
                    backgroundColor: ["#2563eb", "#0f766e", "#ea580c", "#7c3aed"],
                    borderRadius: 8,
                }],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
            },
        });
    };

    const loadDashboard = async () => {
        try {
            const result = await window.OptiFleetApi.request(config.summaryUrl);
            const { kpis, status_breakdown } = result.data;
            document.getElementById("kpiTotalOrders").textContent = kpis.total_orders;
            document.getElementById("kpiPendingOrders").textContent = kpis.pending_orders;
            document.getElementById("kpiAvailableVehicles").textContent = kpis.available_vehicles;
            document.getElementById("kpiTotalProfit").textContent = `${kpis.total_profit.toFixed(2)}`;
            renderChart(status_breakdown);
        } catch (error) {
            window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
        }
    };

    loadDashboard();
})();
