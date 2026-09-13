from control_contratos.models import db


class Area(db.Model):
    __tablename__ = "areas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    contratos = db.relationship("Contrato", back_populates="area")

    def __repr__(self):
        return f"<Area {self.nombre}>"
