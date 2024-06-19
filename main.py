from fastapi import FastAPI
import teradatasql
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

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
