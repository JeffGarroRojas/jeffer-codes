document.getElementById("year").textContent = new Date().getFullYear();

const form = document.getElementById("contact-form");
const status = document.getElementById("form-status");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  status.className = "";
  status.textContent = "Enviando...";

  const body = {
    nombre: form.nombre.value.trim(),
    email: form.email.value.trim(),
    mensaje: form.mensaje.value.trim(),
  };

  try {
    const res = await fetch("/api/lead", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await res.json();
    if (res.ok) {
      status.className = "ok";
      status.textContent = data.mensaje;
      form.reset();
    } else {
      status.className = "err";
      status.textContent = data.detail || "No se pudo enviar. Escribe a hola@jeffer.codes";
    }
  } catch {
    status.className = "err";
    status.textContent = "Sin conexión al servidor. Escribe a hola@jeffer.codes";
  }
});

document.querySelectorAll("[data-checkout]").forEach((btn) => {
  btn.addEventListener("click", async () => {
    btn.textContent = "Abriendo pago...";
    try {
      const res = await fetch("/api/checkout");
      const data = await res.json();
      if (res.ok && data.url) {
        window.location.href = data.url;
      } else {
        btn.textContent = "Pago no disponible aún — escríbeme";
      }
    } catch {
      btn.textContent = "Pago no disponible aún — escríbeme";
    }
  });
});
