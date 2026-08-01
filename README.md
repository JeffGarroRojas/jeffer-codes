# jeffer.codes — Servicio freelance de automatización y scraping

Landing profesional + API propia + herramienta demo para vender servicios de automatización/scraping en Python.

**Objetivo de ganancia: $200 USD mínimo por cliente.** El paquete "Automatización" está fijado en `desde $200`, así que **un solo cliente** cubre el mínimo.

---

## 📁 Qué hay en este proyecto

```
freelance-service/
├── app.py          → Servidor FastAPI: sirve la landing, guarda leads, crea checkout de pago
├── index.html      → Landing (hero, servicios, muestra, precios, formulario)
├── styles.css      → Diseño
├── script.js       → Conecta formulario y botón de pago a la API
├── requirements.txt → Dependencias
├── tools/
│   └── scraper.py  → Herramienta demo REAL (requests + BeautifulSoup), probada
```

Todo funciona y está probado: la landing responde 200, los leads se guardan en SQLite y el scraper extrajo 10 registros de una API real a CSV.

---

## 🚀 Ejecutar local (ya verificado)

```bash
cd ~/freelance-service
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app:app --port 8123
# Abre http://localhost:8123
```

---

## 🌍 Publicar gratis

### Render (recomendado, servidor Python gratis)
1. Sube esta carpeta a un repo de GitHub (ver abajo).
2. En `render.com` → *New* → *Web Service* → conecta tu repo.
3. Build command: `.venv/bin/pip install -r requirements.txt` · Start command: `uvicorn app:app --port $PORT`
4. Listo. Te dan una URL pública.

### GitHub Pages (solo si no quieres backend)
1. `cd ~/freelance-service && git init && git add . && git commit -m "landing"`
2. Crea repo en github.com, sube con `git push`.
3. Repo → Settings → Pages → source: main.
4. (En este modo el formulario no guarda leads: usa el email directo.)

---

## 💸 Cobrar los $200

La API ya tiene el endpoint `/api/checkout` que crea una sesión de pago de **$200** con Stripe. Solo falta tu clave:

1. Crea cuenta gratis en `dashboard.stripe.com` (Stripe te pide tu identidad — solo tú puedes hacerlo).
2. Dashboard → Developers → API keys → copia la *Secret key*.
3. En Render: *Environment Variables* → `STRIPE_SECRET_KEY = sk_live_...`
4. El botón "Empezar" del paquete Automatización abre el checkout de $200 automáticamente.

Para ver los leads recibidos: en Render añade `ADMIN_TOKEN = algo-secreto` y `LEADS_TOKEN = lo-mismo`, luego visita `/api/leads`.

Alternativa sin Stripe: crea un *Payment Link* en Stripe o un invoice de PayPal y pásalo al cliente directamente.

---

## 🎯 Cómo conseguir el primer cliente ($200)

1. **Publica la app** (pasos de arriba).
2. **Crea perfil en 1-2 portales freelance**: Workana, Upwork, Freelancer.
3. **Mensaje de venta** para negocios locales con tareas repetitivas:
   > "Hola, automatizo tareas manuales en Python (reportes, descargas, extracción de datos). Un script te ahorra X horas a la semana. Te mando una demo gratis de 15 min. ¿Te interesa?"
4. Muestra `tools/scraper.py` en la demo — es trabajo real funcionando.
5. Cierra con el **link de pago de $200** → cobras antes de empezar.

---

## ⚙️ La herramienta demo

```bash
.venv/bin/python tools/scraper.py URL -o datos.csv
# --paginar  sigue la paginación del sitio
# --delay 2  respeta el sitio (evita bloqueos)
```

Ejemplo ya probado:
```bash
.venv/bin/python tools/scraper.py https://jsonplaceholder.typicode.com/users -o users.csv
```

---

## ✅ Checklist final
- [ ] App publicada en Render
- [ ] `STRIPE_SECRET_KEY` configurada
- [ ] Link de pago de $200 verificado
- [ ] Perfil en 1-2 portales freelance
- [ ] 10 mensajes de venta enviados
- [ ] Primer cliente → $200 recibido
