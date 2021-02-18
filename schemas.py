from typing import Optional
from pydantic import BaseModel


class BaseTemplate(BaseModel):
    class Config:
        orm_mode = True


class TemplateOut(BaseTemplate):
    id: int
    webtemplate: dict


class TemplateIn(BaseTemplate):
    opt: Optional[str] = None
    webtemplate: Optional[dict]


class ConfigurationOut(BaseTemplate):
    id: int
    data: dict


class ConfigurationIn(BaseTemplate):
    data: dict


class FormPost(BaseTemplate):
    name: str


class FormPut(BaseModel):
    name: str
    template_id: int
    configuration_id: int


class FormOut(BaseTemplate):
    id: int
    name: str
    template: Optional[TemplateOut] = None
    configuration: Optional[ConfigurationOut] = None
