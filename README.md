# REST API for managing doctor schedules and patient appointments.

## Quick Start

1. **Setup:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Server:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Run Tests:**
   ```bash
   pytest
   ```

## 📖 Documentation
* **Swagger UI:** `http://localhost:8000/docs`
* **Full Specs:** See `docs/doc.pdf`
