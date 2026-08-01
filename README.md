# jeffer.codes — Automatización & Scraping en Python

Sitio web de servicios freelance de Jeffer Garro (Pérez Zeledón, Costa Rica).
Live: https://jeffer-codes.onrender.com

---

## Servicios

| Servicio | Precio |
|----------|--------|
| Scraping puntual (1 sitio, entrega CSV/Excel) | desde $75 |
| Automatización de tareas (scripts, bots, reportes) | desde $200 |
| Bot de WhatsApp para negocios | desde $150 |
| Paquete pro (varias tareas + dashboard + soporte 1 mes) | desde $350 |

---

## Stack

- **Backend:** Python 3 + FastAPI + Uvicorn
- **Base de datos:** SQLite (leads de clientes)
- **Pagos:** Stripe Checkout (configurable via env var)
- **Deploy:** Render.com (free tier)
- **Repo:** github.com/JeffGarroRojas/jeffer-codes

---

## Estructura

```
jeffer-codes/
├── app.py           # FastAPI: sirve landing, guarda leads, crea checkout Stripe
├── index.html       # Landing page en español
├── styles.css       # Diseño
├── script.js        # Conecta formulario y botón de pago a la API
├── requirements.txt # Dependencias
└── tools/
    └── scraper.py   # Demo real: scraping con requests + BeautifulSoup
```

---

## Correr local

```bash
pip install -r requirements.txt
uvicorn app:app --port 8123
# Abre http://localhost:8123
```

---

## Variables de entorno (Render)

| Variable | Descripción |
|----------|-------------|
| `STRIPE_SECRET_KEY` | Secret key de Stripe para activar pagos (sk_live_...) |
| `ADMIN_TOKEN` | Token para ver leads en /api/leads |
| `LEADS_TOKEN` | Mismo valor que ADMIN_TOKEN |
| `LEAD_PRICE_CENTS` | Precio en centavos (default: 20000 = $200) |

---

## API endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/api/lead` | POST | Guarda un lead (nombre, email, mensaje) |
| `/api/checkout` | GET | Crea sesión de pago Stripe de $200 |
| `/api/leads` | GET | Lista leads (requiere ADMIN_TOKEN) |

---

## Estrategia de venta

**Target principal:** negocios locales en Pérez Zeledón y zona sur de CR que hacen trabajo manual repetitivo.

**Segmentos con más potencial:**
- Barberías y salones — agendan citas por WhatsApp manualmente
- Sodas y restaurantes con delivery propio
- Ferreterías medianas
- Veterinarias
- Academias y clases particulares

**Mensaje de venta (WhatsApp):**
> "Hola, automatizo tareas manuales en Python — reportes, bots, scraping de datos. Un script te ahorra horas a la semana. Demo gratis de 15 min. ¿Te interesa? jeffer-codes.onrender.com"

**Para bot de WhatsApp específicamente:**
> "Hola, ¿atienden citas por WhatsApp? Les podría instalar un bot que responde automático 24/7 — preguntas frecuentes, horarios, agendamiento. $150, listo en una semana. ¿Les cuento más?"

---

## Próximos pasos

- [ ] Configurar `STRIPE_SECRET_KEY` en Render para activar pagos
- [ ] Crear perfil en Workana / Upwork
- [ ] Contactar 20 negocios locales en Google Maps (barberías PZ)
- [ ] Agregar servicio de bot de WhatsApp en la landing
- [ ] Primer cliente → $200

---

## Cómo popularizar el sitio

### Gratis y rápido (esta semana)
- **Google My Business** — crear perfil en business.google.com, aparecés en Maps cuando buscan "programador freelance pérez zeledón" o "automatización python costa rica". Requiere verificación por postal o teléfono.
- **LinkedIn** — publicar que ofrecés el servicio con el link del sitio. Alcance orgánico alto para servicios B2B.
- **Grupos de Facebook locales** — buscar "emprendedores pérez zeledón", "negocios san isidro general" y publicar el servicio.

### Gratis pero tarda (1-3 meses)
- **Workana / Upwork** — crear perfil, tomar primeros proyectos baratos para conseguir reseñas. Con 3-5 reseñas los clientes llegan solos.
- **SEO** — el sitio ya tiene meta description. Con el tiempo aparece en Google para búsquedas como "scraping python costa rica" o "bot whatsapp negocio cr".

### La secuencia que funciona
1. Primeros 2 clientes → contacto directo por WhatsApp/Maps
2. Pedirles reseña en Google → aparecés en Maps
3. Reseñas traen más clientes → ciclo se repite

### Pendiente de hacer
- [ ] Crear perfil en Google My Business (business.google.com)
- [ ] Publicar en LinkedIn con link del sitio
- [ ] Publicar en grupos de Facebook de PZ
- [ ] Crear perfil en Workana con primeros servicios listados
