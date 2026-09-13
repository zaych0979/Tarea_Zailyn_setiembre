from datetime import date

from dateutil.relativedelta import relativedelta

from control_contratos.models import db

MESES_ADVERTENCIA_RENOVACION = 3

VIGENTE = "Vigente"
POR_VENCER = "Por vencer"
VENCIDO = "Vencido"


class Contrato(db.Model):
    __tablename__ = "contratos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey("areas.id"), nullable=False)
    contraparte = db.Column(db.String(200))
    fecha_inicio = db.Column(db.Date)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    monto = db.Column(db.Numeric(12, 2))
    responsable = db.Column(db.String(150))
    notas = db.Column(db.Text)

    area = db.relationship("Area", back_populates="contratos")

    @property
    def estado(self):
        """Estado derivado de la fecha de vencimiento (RN-01 a RN-04 de la especificación 001)."""
        hoy = date.today()
        if self.fecha_vencimiento < hoy:
            return VENCIDO
        limite_advertencia = self.fecha_vencimiento - relativedelta(
            months=MESES_ADVERTENCIA_RENOVACION
        )
        if hoy >= limite_advertencia:
            return POR_VENCER
        return VIGENTE

    @property
    def requiere_advertencia(self):
        return self.estado in (POR_VENCER, VENCIDO)

    def __repr__(self):
        return f"<Contrato {self.nombre} ({self.estado})>"
