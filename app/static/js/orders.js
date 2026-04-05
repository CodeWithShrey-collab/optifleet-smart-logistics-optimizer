(() => {
    const config = window.OptiFleetOrders;
    if (!config) {
        return;
    }

    const form = document.getElementById("orderForm");
    const tableBody = document.querySelector("#ordersTable tbody");
    const resetButton = document.getElementById("orderResetButton");

    const normalizeDateTime = (value) => value ? value.slice(0, 16) : "";

    const resetForm = () => {
        form.reset();
        document.getElementById("orderId").value = "";
        form.status.value = "pending";
        form.priority.value = "1";
    };

    const renderRows = (orders) => {
        tableBody.innerHTML = orders.map((order) => `
            <tr>
                <td>${order.id}</td>
                <td>${order.customer_name}</td>
                <td>${order.package_name}</td>
                <td>${order.weight}</td>
                <td>${order.profit}</td>
                <td>${order.source} -> ${order.destination}</td>
                <td>${new Date(order.delivery_start).toLocaleString()}<br>${new Date(order.delivery_end).toLocaleString()}</td>
                <td><span class="badge text-bg-secondary">${order.status}</span></td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary me-2" data-action="edit" data-id="${order.id}">Edit</button>
                    <button class="btn btn-sm btn-outline-danger" data-action="delete" data-id="${order.id}">Delete</button>
                </td>
            </tr>
        `).join("");
    };

    const loadOrders = async () => {
        const result = await window.OptiFleetApi.request(config.baseUrl);
        renderRows(result.data);
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const payload = window.OptiFleetApi.formToJson(form);
        const orderId = payload.id;
        delete payload.id;

        try {
            await window.OptiFleetApi.request(orderId ? `${config.baseUrl}/${orderId}` : config.baseUrl, {
                method: orderId ? "PUT" : "POST",
                body: JSON.stringify(payload),
            });
            window.OptiFleetApi.showToast(orderId ? "Order updated." : "Order created.");
            resetForm();
            await loadOrders();
        } catch (error) {
            window.OptiFleetApi.showToast(window.OptiFleetApi.formatErrors(error.payload), "danger");
        }
    });

    tableBody.addEventListener("click", async (event) => {
        const button = event.target.closest("button[data-action]");
        if (!button) {
            return;
        }

        const { action, id } = button.dataset;
        if (action === "edit") {
            try {
                const result = await window.OptiFleetApi.request(`${config.baseUrl}/${id}`);
                const order = result.data;
                document.getElementById("orderId").value = order.id;
                form.customer_name.value = order.customer_name;
                form.package_name.value = order.package_name;
                form.weight.value = order.weight;
                form.profit.value = order.profit;
                form.priority.value = order.priority;
                form.source.value = order.source;
                form.destination.value = order.destination;
                form.delivery_start.value = normalizeDateTime(order.delivery_start);
                form.delivery_end.value = normalizeDateTime(order.delivery_end);
                form.status.value = order.status;
                window.scrollTo({ top: 0, behavior: "smooth" });
            } catch (error) {
                window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
            }
        }

        if (action === "delete") {
            try {
                await window.OptiFleetApi.request(`${config.baseUrl}/${id}`, { method: "DELETE" });
                window.OptiFleetApi.showToast("Order deleted.");
                await loadOrders();
            } catch (error) {
                window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
            }
        }
    });

    resetButton.addEventListener("click", resetForm);
    resetForm();
    loadOrders();
})();
