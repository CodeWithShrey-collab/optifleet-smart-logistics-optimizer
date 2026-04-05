(() => {
    const { formId, endpoint } = window.OptiFleetPage || {};
    const form = document.getElementById(formId);
    if (!form || !endpoint) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            const payload = window.OptiFleetApi.formToJson(form);
            const result = await window.OptiFleetApi.request(endpoint, {
                method: "POST",
                body: JSON.stringify(payload),
            });
            window.location.href = result.redirect_url;
        } catch (error) {
            window.OptiFleetApi.showToast(window.OptiFleetApi.formatErrors(error.payload), "danger");
        }
    });
})();
