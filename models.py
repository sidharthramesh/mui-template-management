from sqlalchemy import JSON, Integer, Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Form(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    template_id = Column(ForeignKey("templates.id"))
    template = relationship("Template", foreign_keys=[template_id])
    configuration_id = Column(ForeignKey("configurations.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    configuration = relationship("Configuration", foreign_keys=[configuration_id])

class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    opt = Column(String)
    webtemplate = Column(JSON)
    form_id = Column(Integer, ForeignKey("forms.id"))
    form = relationship("Form", backref="templates", foreign_keys=[form_id])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Configuration(Base):
    __tablename__ = "configurations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(JSON)
    form_id = Column(Integer, ForeignKey("forms.id"))
    form = relationship("Form", backref="configurations", foreign_keys=[form_id])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())