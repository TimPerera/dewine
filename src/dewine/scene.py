from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey

from config.connection import Base


class ScenePlus(Base):
    __tablename__ = 'scene_plus'
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id:Mapped[int] = mapped_column(ForeignKey('customer.id'))
    customer:Mapped["Customer"] = relationship(back_populates="scene_plus")
