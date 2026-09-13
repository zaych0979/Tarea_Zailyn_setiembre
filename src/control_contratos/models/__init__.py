from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from control_contratos.models.area import Area  # noqa: E402,F401
from control_contratos.models.contrato import Contrato  # noqa: E402,F401
