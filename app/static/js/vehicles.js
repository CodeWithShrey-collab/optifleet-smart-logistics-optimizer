(() => {
    const config = window.OptiFleetVehicles;
    if (!config) {
        return;
    }

    const form = document.getElementById("vehicleForm");
    const tableBody = document.querySelector("#vehiclesTable tbody");
    const resetButton = document.getElementById("vehicleResetButton");

    const resetForm = () => {
        form.reset();
        document.getElementById("vehicleId").value = "";
        form.current_load.value = "0";
        form.status.value = "available";
    };

    const renderRows = (vehicles) => {
        tableBody.innerHTML = vehicles.map((vehicle) => `
            <tr>
                <td>${vehicle.id}</td>
                <td>${vehicle.truck_name}</td>
                <td>${vehicle.capacity}</td>
                <td>${vehicle.current_load}</td>
                <td><span class="badge text-bg-secondary">${vehicle.status}</span></td>
                <td>${vehicle.location}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary me-2" data-action="edit" data-id="${vehicle.id}">Edit</button>
                    <button class="btn btn-sm btn-outline-danger" data-action="delete" data-id="${vehicle.id}">Delete</button>
                </td>
            </tr>
        `).join("");
    };

    const loadVehicles = async () => {
        const result = await window.OptiFleetApi.request(config.baseUrl);
        renderRows(result.data);
    };

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const payload = window.OptiFleetApi.formToJson(form);
        const vehicleId = payload.id;
        delete payload.id;

        try {
            await window.OptiFleetApi.request(vehicleId ? `${config.baseUrl}/${vehicleId}` : config.baseUrl, {
                method: vehicleId ? "PUT" : "POST",
                body: JSON.stringify(payload),
            });
            window.OptiFleetApi.showToast(vehicleId ? "Vehicle updated." : "Vehicle created.");
            resetForm();
            await loadVehicles();
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
                const vehicle = result.data;
                document.getElementById("vehicleId").value = vehicle.id;
                form.truck_name.value = vehicle.truck_name;
                form.capacity.value = vehicle.capacity;
                form.current_load.value = vehicle.current_load;
                form.status.value = vehicle.status;
                form.location.value = vehicle.location;
                window.scrollTo({ top: 0, behavior: "smooth" });
            } catch (error) {
                window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
            }
        }

        if (action === "delete") {
            try {
                await window.OptiFleetApi.request(`${config.baseUrl}/${id}`, { method: "DELETE" });
                window.OptiFleetApi.showToast("Vehicle deleted.");
                await loadVehicles();
            } catch (error) {
                window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
            }
        }
    });

    resetButton.addEventListener("click", resetForm);
    resetForm();
    loadVehicles();
})();
