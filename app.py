import json
import os
import sqlite3
import threading
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel

import stripe

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "leads.db"
STATIC = {
    "styles.css": "styles.css",
    "script.js": "script.js",
}

app = FastAPI(title="jeffer.codes")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
LEAD_PRICE_CENTS = int(os.environ.get("LEAD_PRICE_CENTS", "20000"))

_lock = threading.Lock()


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                creado TEXT DEFAULT (datetime('now'))
            )
            """
        )


init_db()


class Lead(BaseModel):
    nombre: str
    email: str
    mensaje: str


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/{name}")
def static_file(name: str):
    if name in STATIC:
        return FileResponse(BASE_DIR / STATIC[name])
    raise HTTPException(status_code=404)


@app.post("/api/lead")
async def create_lead(lead: Lead):
    if not lead.nombre.strip() or not lead.email.strip() or not lead.mensaje.strip():
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios")
    with _lock:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO leads (nombre, email, mensaje) VALUES (?, ?, ?)",
                (lead.nombre.strip(), lead.email.strip(), lead.mensaje.strip()),
            )
    return {"ok": True, "mensaje": "Recibido. Respondo en menos de 24 horas."}


@app.get("/api/checkout")
def checkout():
    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe no configurado: define STRIPE_SECRET_KEY para activar pagos",
        )
    stripe.api_key = STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": LEAD_PRICE_CENTS,
                "product_data": {"name": "Automatización en Python (paquete desde $200)"},
            },
            "quantity": 1,
        }],
        success_url="https://jeffer.codes/?pago=ok",
        cancel_url="https://jeffer.codes/?pago=cancelado",
    )
    return {"url": session.url}


@app.get("/api/leads")
def leads():
    if os.environ.get("LEADS_TOKEN") != os.environ.get("ADMIN_TOKEN"):
        raise HTTPException(status_code=401, detail="No autorizado")
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT id, nombre, email, mensaje, creado FROM leads ORDER BY id DESC").fetchall()
    return [
        {"id": r[0], "nombre": r[1], "email": r[2], "mensaje": r[3], "creado": r[4]}
        for r in rows
    ]
