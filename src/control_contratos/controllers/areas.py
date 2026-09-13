from flask import Blueprint, flash, redirect, render_template, request, url_for

from control_contratos.models import db
from control_contratos.models.area import Area

bp = Blueprint("areas", __name__, url_prefix="/areas")


@bp.route("/", methods=["GET", "POST"])
def listado():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        existe = Area.query.filter_by(nombre=nombre).first()
        if nombre and not existe:
            db.session.add(Area(nombre=nombre))
            db.session.commit()
            flash("Área creada correctamente.", "success")
        else:
            flash("El nombre del área es inválido o ya existe.", "error")
        return redirect(url_for("areas.listado"))

    areas = Area.query.order_by(Area.nombre).all()
    return render_template("areas/listado.html", areas=areas)
