from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from database import get_connection, init_db

app = FastAPI(
    title="StructScan API — Inspeção Predial e Patologias (Lei 9.913/2012)",
    description="Backend REST com banco de dados SQLite para vistorias prediais, catálogo de patologias civis e elétricas e emissão de laudos.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

class VistoriaUpdate(BaseModel):
    edificacao: str
    endereco: str
    uso_edificacao: str
    idade_imovel: int
    periodicidade_cip: str
    data_vistoria: str
    engenheiro: str
    crea_art: str
    estado_geral: str

class AnomaliaCreate(BaseModel):
    vistoria_id: int = 1
    area: str
    sistema: str
    titulo: str
    local: str
    risco: str
    tipo_manutencao: str
    prazo_conclusao: str
    requer_laudo_especifico: int = 0
    diagnostico: str
    recomendacao: str
    foto_base64: Optional[str] = None

@app.get("/api/catalogo")
def listar_catalogo(area: Optional[str] = None):
    conn = get_connection()
    cur = conn.cursor()
    if area and area in ("Civil", "Elétrica"):
        cur.execute("SELECT * FROM catalogo_patologias WHERE area = ? ORDER BY codigo", (area,))
    else:
        cur.execute("SELECT * FROM catalogo_patologias ORDER BY area, codigo")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

@app.get("/api/vistoria/{vistoria_id}")
def obter_vistoria(vistoria_id: int = 1):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vistorias WHERE id = ?", (vistoria_id,))
    v = cur.fetchone()
    if not v:
        conn.close()
        raise HTTPException(status_code=404, detail="Vistoria não encontrada")
    cur.execute("SELECT * FROM anomalias_registradas WHERE vistoria_id = ? ORDER BY id DESC", (vistoria_id,))
    anomalias = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"vistoria": dict(v), "anomalias": anomalias}

@app.put("/api/vistoria/{vistoria_id}")
def atualizar_vistoria(vistoria_id: int, payload: VistoriaUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE vistorias
        SET edificacao=?, endereco=?, uso_edificacao=?, idade_imovel=?, periodicidade_cip=?, data_vistoria=?, engenheiro=?, crea_art=?, estado_geral=?
        WHERE id=?
    """, (
        payload.edificacao, payload.endereco, payload.uso_edificacao, payload.idade_imovel,
        payload.periodicidade_cip, payload.data_vistoria, payload.engenheiro, payload.crea_art,
        payload.estado_geral, vistoria_id
    ))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.post("/api/anomalias")
def criar_anomalia(payload: AnomaliaCreate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO anomalias_registradas
        (vistoria_id, area, sistema, titulo, local, risco, tipo_manutencao, prazo_conclusao, requer_laudo_especifico, diagnostico, recomendacao, foto_base64)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        payload.vistoria_id, payload.area, payload.sistema, payload.titulo, payload.local,
        payload.risco, payload.tipo_manutencao, payload.prazo_conclusao, payload.requer_laudo_especifico,
        payload.diagnostico, payload.recomendacao, payload.foto_base64
    ))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return {"id": new_id, "status": "created"}

@app.delete("/api/anomalias/{anomalia_id}")
def deletar_anomalia(anomalia_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM anomalias_registradas WHERE id = ?", (anomalia_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}
