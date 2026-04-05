(() => {
    const config = window.OptiFleetDispatch;
    const runButton = document.getElementById("runDispatch");
    if (!config || !runButton) {
        return;
    }

    const selectedTableBody = document.querySelector("#dispatchSelectedTable tbody");
    const routeText = document.getElementById("dispatchRouteText");
    const routeMeta = document.getElementById("dispatchRouteMeta");
    const routeList = document.getElementById("dispatchRouteList");
    const profitText = document.getElementById("dispatchProfitText");
    const profitWindow = document.getElementById("dispatchProfitWindow");

    const pendingCountEl = document.getElementById("dispatchPendingCount");
    const selectedCountEl = document.getElementById("dispatchSelectedCount");
    const routeStopsEl = document.getElementById("dispatchRouteStops");
    const profitMaxEl = document.getElementById("dispatchProfitMax");

    const formatDateTime = (value) => new Date(value).toLocaleString();

    const renderSelected = (selected) => {
        if (!selected.length) {
            selectedTableBody.innerHTML = '<tr><td colspan="6" class="text-center text-secondary">No compatible pending deliveries found.</td></tr>';
            return;
        }

        selectedTableBody.innerHTML = selected.map((item) => `
            <tr>
                <td>#${item.id}</td>
                <td>${item.customer_name}</td>
                <td>${item.package_name}</td>
                <td>${item.destination}</td>
                <td>${formatDateTime(item.delivery_start)}<br>${formatDateTime(item.delivery_end)}</td>
                <td>${item.profit.toFixed(2)}</td>
            </tr>
        `).join("");
    };

    const renderRoute = (_route, routeDetails, routeSummary) => {
        if (!routeDetails.length) {
            routeText.textContent = routeSummary || "No route found for the selected dispatch set.";
            routeMeta.textContent = "Add more compatible pending deliveries to build a richer route.";
            routeList.innerHTML = "";
            return;
        }

        if (routeDetails.length === 1) {
            routeText.textContent = routeSummary || `Single-stop dispatch: ${routeDetails[0].destination}`;
            routeMeta.textContent = "Only one compatible delivery was selected, so no multi-stop route was needed.";
        } else {
            const stopNames = routeDetails
                .filter((item) => !item.is_return_to_start)
                .map((item) => item.destination);
            routeText.textContent = routeSummary || stopNames.join(" -> ");
            routeMeta.textContent = routeDetails[routeDetails.length - 1]?.is_return_to_start
                ? "The algorithm found a closed loop and returns to the origin after the listed stops."
                : "Recommended stop sequence for the selected delivery set.";
        }

        routeList.innerHTML = routeDetails.map((item, index) => `
            <div class="list-group-item px-0">
                <div class="fw-semibold">${item.is_return_to_start ? "Return" : `Stop ${index + 1}`}: ${item.destination}</div>
                <div class="small text-secondary">Order #${item.order_id} | ${item.customer_name} | ${item.package_name}</div>
            </div>
        `).join("");
    };

    const renderProfit = (profitAnalysis, profitSet, profitSummary) => {
        if (!profitAnalysis || Object.keys(profitAnalysis).length === 0) {
            profitText.textContent = profitSummary || "No profit analysis available.";
            profitWindow.innerHTML = "";
            return;
        }

        profitText.textContent = profitSummary || `Best profit streak: ${profitAnalysis.max_sum.toFixed(2)}.`;

        profitWindow.innerHTML = profitSet.map((item) => `
            <div class="list-group-item px-0">
                <div class="fw-semibold">Order #${item.id} - ${item.package_name}</div>
                <div class="small text-secondary">${item.destination} | Profit ${item.profit.toFixed(2)}</div>
            </div>
        `).join("");
    };

    runButton.addEventListener("click", async () => {
        runButton.disabled = true;
        runButton.textContent = "Generating...";

        try {
            const result = await window.OptiFleetApi.request(config.runUrl, { method: "POST" });
            const data = result.data;

            pendingCountEl.textContent = data.pending_order_count;
            selectedCountEl.textContent = data.selected.length;
            routeStopsEl.textContent = data.route_details.filter((item) => !item.is_return_to_start).length;
            profitMaxEl.textContent = data.profit_analysis?.max_sum ? data.profit_analysis.max_sum.toFixed(2) : "0";

            renderSelected(data.selected);
            renderRoute(data.route, data.route_details, data.route_summary);
            renderProfit(data.profit_analysis, data.profit_window, data.profit_summary);
            window.OptiFleetApi.showToast("Dispatch plan generated.");
        } catch (error) {
            window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
        } finally {
            runButton.disabled = false;
            runButton.textContent = "Generate Dispatch Plan";
        }
    });
})();
