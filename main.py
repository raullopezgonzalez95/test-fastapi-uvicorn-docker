import uvicorn
from fastapi import FastAPI, UploadFile, File
import pandas as pd
from io import StringIO

app = FastAPI()


@app.get("/")
def root():
    return {"hello world"}

@app.post("/rendimiento")
def rendimiento(valor_inicial: float, dias: float, rendimiento: float):
    tasa_diaria = rendimiento / 100 / 365
    valor_final = valor_inicial * (1 + tasa_diaria) ** dias
    ganancia = valor_final - valor_inicial
    return {
        "valor_inicial": valor_inicial,
        "valor_final": round(valor_final, 2),
        "ganancia": round(ganancia, 2),
        "dias": dias,
        "rendimiento_anual": rendimiento
    }

@app.post("/csv")
async def csv(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))
    print(df.head())
    return {"message": "CSV procesado correctamente", "columns": df.columns.tolist()}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)