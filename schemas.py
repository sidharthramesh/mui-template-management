from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class BaseTemplate(BaseModel):
    class Config:
        orm_mode = True


class TemplateOut(BaseTemplate):
    id: int
    webtemplate: dict
    created_at: datetime
    last_updated: datetime

class TemplateIn(BaseTemplate):
    opt: Optional[str] = None
    webtemplate: Optional[dict]
    

class ConfigurationOut(BaseTemplate):
    id: int
    data: dict
    created_at: datetime
    last_updated: datetime

class ConfigurationIn(BaseTemplate):
    data: dict


class FormPost(BaseTemplate):
    name: str


class FormPut(BaseModel):
    name: str
    template_id: Optional[int]
    configuration_id: Optional[int]


class FormOut(BaseTemplate):
    id: int
    name: str
    template: Optional[TemplateOut] = None
    configuration: Optional[ConfigurationOut] = None
    created_at: datetime
    last_updated: datetime