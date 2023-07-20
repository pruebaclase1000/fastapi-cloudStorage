from fastapi import FastAPI, UploadFile, HTTPException
from google.cloud import storage
import os
import io
from fastapi.middleware.cors import CORSMiddleware

#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service.json'

app = FastAPI()
cliente = storage.Client()
bucketname = 'chatmine-388722-storage'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def obtenerbucket(blob_name):
    bucket = cliente.get_bucket(bucketname)
    blob = bucket.blob(blob_name)
    return blob

@app.get("/")
async def bienvienida():
    return {"mensaje": "Bienvenido a mi aplicación"}

@app.post("/archivos")
async def subir_archivos(file: UploadFile):
    filename = os.path.basename(file.filename)
    file_type = os.path.splitext(filename)[1]
    blob = obtenerbucket(filename)
    
    contenido = await file.read()

    if file_type == '.pdf':
        byte_contenido = io.BytesIO(contenido)
        blob.upload_from_file(byte_contenido)
    else:
        blob.upload_from_string(contenido)
    
    return {"Nombre de archivo": file.filename, "bucket": bucketname}

@app.put("/actualizar")
async def actualizar_archivos(file: UploadFile):
    filename = os.path.basename(file.filename)
    file_type = os.path.splitext(filename)[1]
    blob = obtenerbucket(filename)

    # Verificar que el archivo exista en el bucket
    if blob.exists():
        blob.delete()

        contenido = await file.read()

        if file_type == '.pdf':
            byte_contenido = io.BytesIO(contenido)
            blob.upload_from_file(byte_contenido)
        else:
            blob.upload_from_string(contenido)
        
        return {"Nombre de archivo": file.filename, "bucket": bucketname}
    
    else:
        raise HTTPException(status_code=404, detail="El archivo solicitado no existe")

@app.delete("/eliminar")
def eliminar_archivo(filename: str):
    blob = obtenerbucket(filename)

    # Eliminar archivo si existe
    if blob.exists():
        blob.delete()

        return {"Nombre de archivo": filename, "bucket": bucketname}
    
    else:
        raise HTTPException(status_code=404, detail="El archivo solicitado no existe")

@app.get("/leer")
async def leer_archivos(filename: str):
    blob = obtenerbucket(filename)

    if not blob.exists():
        raise HTTPException(status_code=404, detail="El archivo solicitado no existe")
    
    contenido = blob.download_as_text()

    return {"Nombre de archivo": filename, "Contenido": contenido}
