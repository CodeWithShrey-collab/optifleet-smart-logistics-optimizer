(() => {
    const logoutButton = document.getElementById("logoutButton");
    if (!logoutButton || !window.OptiFleetAuth) {
        return;
    }

    logoutButton.addEventListener("click", async () => {
        try {
            const result = await window.OptiFleetApi.request(window.OptiFleetAuth.logoutUrl, { method: "POST" });
            window.location.href = result.redirect_url;
        } catch (error) {
            window.OptiFleetApi.showToast(error.payload?.message || error.message, "danger");
        }
    });
})();
