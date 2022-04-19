from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import pybase64
import json
import modelIDcard
import modelAlien
import modelPassport

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

class ImageType(BaseModel):
    url: str

@app.get("/")
def main(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


@app.post("/")
async def readFile(request: Request, image_upload: UploadFile = Form(...), cardType: str = Form(...)):
    # file upload
    data = await image_upload.read()
    upload_filename = 'static/' + image_upload.filename

    with open(upload_filename, 'wb') as f:
        f.write(data)

    # call model
    if cardType == 'thaiid':
        template_filename = 'static/idcardTemplate.jpg'
        pre_result = modelIDcard.getMain(upload_filename, template_filename)

    elif cardType == 'alien':
        template_filename = 'static/aliencardTemplate.png'
        pre_result = modelAlien.getMain(upload_filename, template_filename)

    elif cardType == 'passport':
        template_filename = 'static/passportTemplete.png'
        pre_result = modelPassport.getMain(upload_filename, template_filename)

    os.remove(upload_filename)

    return pre_result

if __name__ == '__main__':
    uvicorn.run(app, debug=True)