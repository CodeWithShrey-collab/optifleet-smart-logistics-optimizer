(() => {
    const config = window.OptiFleetOptimizer;
    if (!config) {
        return;
    }

    const form = document.getElementById("optimizerForm");
    const vehicleSelect = document.getElementById("optimizerVehicle");
    const orderList = document.getElementById("optimizerOrders");
    const tableBody = document.querySelector("#optimizerTable tbody");
    const totalValueEl = document.getElementById("totalValue");
    const remainingCapacityEl = document.getElementById("remainingCapacity");

    const renderOrders = (orders) => {
        orderList.innerHTML = orders.map((order) => `
            <label class="optimizer-order-item">
                <input class="form-check-input mt-1" type="checkbox" name="order_ids" value="${order.id}">
                <span>
                    <strong>${order.package_name}</strong><br>
                    <span class="text-secondary small">${order.customer_name} | ${order.destination} | ${order.weight}kg | profit ${order.profit}</span>
                </span>
            </label>
        `).join("") || '<div class="text-secondary small">No pending orders available.</div>';
    };

    const renderVehicles = (vehicles) => {
        vehicleSelect.innerHTML = '<option value="">Select a vehicle</option>' + vehicles.map((vehicle) => `
            <option value="${vehicle.id}">${vehicle.truck_name} (${(vehicle.capacity - vehicle.current_load).toFixed(2)} free capacity)</option>
        `).join("");
    };

    const renderResult = (result) => {
        remainingCapacityEl.textContent = `${result.remaining_capacity.toFixed(2)} kg`;
        totalValueEl.textContent = `Projected value: ${result.total_value.toFixed(2)}`;
        tableBody.innerHTML = result.selected_items.map((item) => `
            <tr>
                <td>${item.package_name}</td>
                <td>${item.customer_name}</td>
                <td>${item.destination}</td>
                <td>${item.selected_weight}</td>
                <td>${item.fraction}</td>
                <td>${item.value_gained}</td>
            </tr>
        `).join("") || '<tr><td colspan="6" class="text-center text-secondary">No allocation possible for the selected capacity.</td></tr>';
    };

    const loadContext = async () => {
        try {
            const result = await window.OptiFleetApi.request(config.contextUrl);
            renderVehicles(result.data.vehicles);
            renderOrders(result.data.orders);
        } catch (error) {
            window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
        }
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const orderIds = [...orderList.querySelectorAll('input[name="order_ids"]:checked')].map((input) => input.value);
        try {
            const result = await window.OptiFleetApi.request(config.runUrl, {
                method: "POST",
                body: JSON.stringify({
                    vehicle_id: vehicleSelect.value,
                    order_ids: orderIds,
                }),
            });
            renderResult(result.data);
            window.OptiFleetApi.showToast("Optimization completed.");
        } catch (error) {
            window.OptiFleetApi.showToast(window.OptiFleetApi.formatErrors(error.payload), "danger");
        }
    });

    loadContext();
})();
