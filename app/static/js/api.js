window.OptiFleetApi = (() => {
    const showToast = (message, variant = "success") => {
        const container = document.getElementById("toastContainer");
        if (!container) {
            return;
        }

        const toastElement = document.createElement("div");
        toastElement.className = `toast align-items-center text-bg-${variant} border-0`;
        toastElement.role = "alert";
        toastElement.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        container.appendChild(toastElement);
        const toast = new bootstrap.Toast(toastElement, { delay: 3500 });
        toast.show();
        toastElement.addEventListener("hidden.bs.toast", () => toastElement.remove());
    };

    const formToJson = (form) => Object.fromEntries(new FormData(form).entries());

    const request = async (url, options = {}) => {
        const response = await fetch(url, {
            headers: { "Content-Type": "application/json", ...(options.headers || {}) },
            credentials: "same-origin",
            ...options,
        });
        const body = await response.json().catch(() => ({}));
        if (!response.ok) {
            const error = new Error(body.message || "Request failed.");
            error.payload = body;
            throw error;
        }
        return body;
    };

    const formatErrors = (payload) => {
        if (!payload?.errors) {
            return payload?.message || "Something went wrong.";
        }
        return Object.values(payload.errors).join(" ");
    };

    return { showToast, formToJson, request, formatErrors };
})();
