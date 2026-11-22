# StructScan — Plataforma Inteligente de Inspeção Predial e Laudos Técnicos (CIP)

Sistema web full-stack desenvolvido para automatizar vistorias de engenharia diagnóstica (Civil e Elétrica) e emissão de Laudos Técnicos em conformidade com a **Lei Ordinária Municipal nº 9.913/2012 (Fortaleza/CE)** e a **ABNT NBR 16747:2020**.

**Integrantes do Grupo (AV2 — Inovação e Startups):**
- Edvaldo Queiroz
- Luana
- Felipe
- Samuel

---

## Arquitetura e Tecnologias

- **Banco de Dados:** SQLite (`structscan.db`) com 3 tabelas relacionais (`catalogo_patologias`, `vistorias` e `anomalias_registradas`), pré-populado com **18 patologias normativas** (10 de Engenharia Civil e 8 de Engenharia Elétrica).
- **Backend:** Python 3 + **FastAPI** + Uvicorn (API RESTful com endpoints GET, POST, PUT e DELETE).
- **Frontend:** HTML5, CSS3 (Design System responsivo) e JavaScript Vanilla com geração nativa de Laudo Técnico em PDF e modo de contingência offline automático.

---

## Estrutura de Pastas

```text
structscan-fullstack/
├── backend/
│   ├── database.py         # Criação das tabelas SQLite e seed de patologias Civil/Elétrica
│   ├── main.py             # API REST FastAPI
│   └── requirements.txt    # Dependências Python
├── frontend/
│   └── index.html          # Interface web completa + Gerador de Laudo PDF
└── README.md
```

---

## Como Instalar e Rodar Localmente

### 1. Rodar o Backend + Banco de Dados (Python / FastAPI)
Abra o terminal na pasta `backend/` e execute:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
O servidor iniciará em `http://localhost:8000` e criará automaticamente o arquivo de banco de dados `structscan.db` com todas as patologias civis e elétricas cadastradas.
- Documentação interativa da API (Swagger): `http://localhost:8000/docs`

### 2. Abrir o Frontend
Abra o arquivo `frontend/index.html` diretamente no navegador (Google Chrome ou Edge). O sistema conectará automaticamente ao backend em `http://localhost:8000` (e caso o servidor esteja desligado, funciona em modo demonstração local).
