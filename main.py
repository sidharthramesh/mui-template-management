from fastapi.params import Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import Session
from database import SessionLocal
from typing import List
from fastapi import FastAPI
import schemas
import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(
    title="Medblocks Helper Services",
    version="0.0.1",
    openapi_tags=[],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/form", response_model=List[schemas.FormOut], tags=["form"])
async def get_forms(db: Session = Depends(get_db)):
    return db.query(models.Form).all()


@app.get("/form/{id}", response_model=schemas.FormOut, tags=["form"])
async def get_form(id: int, db: Session = Depends(get_db)):
    return db.query(models.Form).get(id)


@app.post("/form", response_model=schemas.FormOut, tags=["form"])
async def create_form(form: schemas.FormPost, db: Session = Depends(get_db)):
    db_form = models.Form(name=form.name)
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return db_form


@app.put("/form/{id}", response_model=schemas.FormOut, tags=["form"])
async def update_form(id: int, form: schemas.FormPut, db: Session = Depends(get_db)):
    db_form = db.query(models.Form).get(id)
    db_form.name = form.name
    if form.template_id:
        db_form.template_id = form.template_id
    if form.configuration_id:
        db_form.configuration_id = form.configuration_id
    db.commit()
    db.refresh(db_form)
    return db_form

@app.delete("/form/{id}", tags=["form"])
async def get_form(id: int, db: Session = Depends(get_db)):
    db_form = db.query(models.Form).get(id)
    db.delete(db_form)
    db.commit()
    return {"id": id}

@app.post(
    "/form/{form_id}/template",
    response_model=schemas.TemplateOut,
    tags=["form", "template"],
)
async def create_template(
    form_id: int, template: schemas.TemplateIn, db: Session = Depends(get_db)
):
    db_template = models.Template(**template.dict(), form_id=form_id)
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    if db_template.form.template is None:
        db_template.form.template_id = db_template.id
        db.commit()
    return db_template


@app.get(
    "/form/{form_id}/template",
    response_model=List[schemas.TemplateOut],
    tags=["form", "template"],
)
async def get_templates(form_id: int, db: Session = Depends(get_db)):
    return db.query(models.Template).filter(models.Template.form_id == form_id).all()


@app.post(
    "/form/{form_id}/configuration",
    response_model=schemas.ConfigurationOut,
    tags=["form", "configuration"],
)
async def create_configuration(
    form_id: int, config: schemas.ConfigurationIn, db: Session = Depends(get_db)
):
    db_config = models.Configuration(data=config.data, form_id=form_id)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    if db_config.form.configuration is None:
        db_config.form.configuration_id = db_config.id
        db.commit()
    return db_config


@app.get(
    "/form/{form_id}/configuration",
    response_model=List[schemas.ConfigurationOut],
    tags=["form", "configuration"],
)
async def get_configurations(form_id: int, db: Session = Depends(get_db)):
    return db.query(models.Configuration).filter(form_id == form_id).all()


@app.get(
    "/configuration/{id}",
    response_model=schemas.ConfigurationOut,
    tags=["configuration"],
)
async def get_configuration(id: int, db: Session = Depends(get_db)):
    return db.query(models.Configuration).get(id)


@app.put(
    "/configuration/{id}",
    response_model=schemas.ConfigurationOut,
    tags=["configuration"],
)
async def update_configuration(
    id: int, config: schemas.ConfigurationIn, db: Session = Depends(get_db)
):
    db_config = db.query(models.Configuration).get(id)
    db_config.data = config.data
    db.commit()
    db.refresh(db_config)
    return db_config