from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import teradatasql
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.get("/query/")
async def execute_query(sql: str):
    # Sécurité : Validation basique pour éviter les requêtes potentiellement dangereuses
    if "drop" in sql.lower() or "delete" in sql.lower():
        raise HTTPException(status_code=400, detail="Unsafe SQL statement detected.")

    host = os.getenv("TERADATA_HOST")
    user = os.getenv("TERADATA_USER")
    password = os.getenv("TERADATA_PASSWORD")

    with teradatasql.connect(host=host, user=user, password=password) as connect:
        cur = connect.cursor()
        try:
            cur.execute(sql)
            result = cur.fetchall()
            return {"data": result}
        except Exception as e:
            return {"error": str(e)}
