(() => {
    const config = window.OptiFleetWarehouses;
    if (!config) {
        return;
    }

    const form = document.getElementById("warehouseForm");
    const tableBody = document.querySelector("#warehousesTable tbody");
    const resetButton = document.getElementById("warehouseResetButton");

    const resetForm = () => {
        form.reset();
        document.getElementById("warehouseId").value = "";
    };

    const renderRows = (warehouses) => {
        if (!warehouses.length) {
            tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-secondary">No warehouses added yet.</td></tr>';
            return;
        }

        tableBody.innerHTML = warehouses.map((warehouse) => `
            <tr>
                <td>${warehouse.id}</td>
                <td>${warehouse.name}</td>
                <td>${warehouse.city}</td>
                <td>${warehouse.latitude}</td>
                <td>${warehouse.longitude}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary me-2" data-action="edit" data-id="${warehouse.id}">Edit</button>
                    <button class="btn btn-sm btn-outline-danger" data-action="delete" data-id="${warehouse.id}">Delete</button>
                </td>
            </tr>
        `).join("");
    };

    const loadWarehouses = async () => {
        const result = await window.OptiFleetApi.request(config.baseUrl);
        renderRows(result.data);
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const payload = window.OptiFleetApi.formToJson(form);
        const warehouseId = payload.id;
        delete payload.id;

        try {
            await window.OptiFleetApi.request(warehouseId ? `${config.baseUrl}/${warehouseId}` : config.baseUrl, {
                method: warehouseId ? "PUT" : "POST",
                body: JSON.stringify(payload),
            });
            window.OptiFleetApi.showToast(warehouseId ? "Warehouse updated." : "Warehouse created.");
            resetForm();
            await loadWarehouses();
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
                const warehouse = result.data;
                document.getElementById("warehouseId").value = warehouse.id;
                form.name.value = warehouse.name;
                form.city.value = warehouse.city;
                form.latitude.value = warehouse.latitude;
                form.longitude.value = warehouse.longitude;
                window.scrollTo({ top: 0, behavior: "smooth" });
            } catch (error) {
                window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
            }
        }

        if (action === "delete") {
            try {
                await window.OptiFleetApi.request(`${config.baseUrl}/${id}`, { method: "DELETE" });
                window.OptiFleetApi.showToast("Warehouse deleted.");
                await loadWarehouses();
            } catch (error) {
                window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
            }
        }
    });

    resetButton.addEventListener("click", resetForm);
    resetForm();
    loadWarehouses();
})();
