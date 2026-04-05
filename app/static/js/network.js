(() => {
    const config = window.OptiFleetNetwork;
    const runButton = document.getElementById("runMST");
    if (!config || !runButton) {
        return;
    }

    const warehouseCountEl = document.getElementById("networkWarehouseCount");
    const edgeCountEl = document.getElementById("networkEdgeCount");
    const totalCostEl = document.getElementById("networkTotalCost");
    const summaryEl = document.getElementById("networkSummary");
    const tableBody = document.querySelector("#networkTable tbody");
    const warehouseList = document.getElementById("warehouseList");

    const renderWarehouses = (warehouses) => {
        warehouseCountEl.textContent = warehouses.length;
        if (!warehouses.length) {
            warehouseList.innerHTML = '<div class="text-secondary small">No warehouses available yet.</div>';
            return;
        }

        warehouseList.innerHTML = warehouses.map((warehouse) => `
            <div class="list-group-item px-0">
                <div class="fw-semibold">${warehouse.name}</div>
                <div class="small text-secondary">${warehouse.city} | Lat ${warehouse.latitude}, Lng ${warehouse.longitude}</div>
            </div>
        `).join("");
    };

    const renderEdges = (edges) => {
        edgeCountEl.textContent = edges.length;
        if (!edges.length) {
            tableBody.innerHTML = '<tr><td colspan="3" class="text-center text-secondary">No optimized links available.</td></tr>';
            return;
        }

        tableBody.innerHTML = edges.map((edge) => `
            <tr>
                <td>${edge.from_name} <span class="text-secondary">(${edge.from_city})</span></td>
                <td>${edge.to_name} <span class="text-secondary">(${edge.to_city})</span></td>
                <td>${edge.weight.toFixed(2)}</td>
            </tr>
        `).join("");
    };

    runButton.addEventListener("click", async () => {
        runButton.disabled = true;
        runButton.textContent = "Optimizing...";

        try {
            const result = await window.OptiFleetApi.request(config.runUrl, { method: "POST" });
            const data = result.data;

            renderWarehouses(data.warehouses);
            renderEdges(data.mst);
            totalCostEl.textContent = Number(data.total_cost).toFixed(2);
            summaryEl.textContent = data.summary;

            if (!data.is_connected) {
                window.OptiFleetApi.showToast(data.summary, "warning");
            } else {
                window.OptiFleetApi.showToast("Network optimization completed.");
            }
        } catch (error) {
            window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
        } finally {
            runButton.disabled = false;
            runButton.textContent = "Optimize Network";
        }
    });
})();
