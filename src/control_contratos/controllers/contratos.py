from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from control_contratos.models import db
from control_contratos.models.area import Area
from control_contratos.models.contrato import Contrato

bp = Blueprint("contratos", __name__, url_prefix="/contratos")


def _parse_fecha(valor):
    return datetime.strptime(valor, "%Y-%m-%d").date() if valor else None


def _aplicar_formulario(contrato, form):
    contrato.nombre = form["nombre"].strip()
    contrato.area_id = form["area_id"]
    contrato.contraparte = form.get("contraparte", "").strip() or None
    contrato.fecha_inicio = _parse_fecha(form.get("fecha_inicio"))
    contrato.fecha_vencimiento = _parse_fecha(form["fecha_vencimiento"])
    contrato.monto = form.get("monto") or None
    contrato.responsable = form.get("responsable", "").strip() or None
    contrato.notas = form.get("notas", "").strip() or None


@bp.route("/")
def listado():
    area_id = request.args.get("area_id", type=int)
    estado_filtro = request.args.get("estado") or None

    query = Contrato.query
    if area_id:
        query = query.filter_by(area_id=area_id)
    contratos = query.order_by(Contrato.fecha_vencimiento.asc()).all()

    if estado_filtro:
        contratos = [c for c in contratos if c.estado == estado_filtro]

    areas = Area.query.order_by(Area.nombre).all()
    return render_template(
        "contratos/listado.html",
        contratos=contratos,
        areas=areas,
        area_id=area_id,
        estado_filtro=estado_filtro,
    )


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    areas = Area.query.order_by(Area.nombre).all()
    if request.method == "POST":
        contrato = Contrato()
        _aplicar_formulario(contrato, request.form)
        db.session.add(contrato)
        db.session.commit()
        flash("Contrato creado correctamente.", "success")
        return redirect(url_for("contratos.listado"))
    return render_template("contratos/formulario.html", areas=areas, contrato=None)


@bp.route("/<int:contrato_id>")
def detalle(contrato_id):
    contrato = db.get_or_404(Contrato, contrato_id)
    return render_template("contratos/detalle.html", contrato=contrato)


@bp.route("/<int:contrato_id>/editar", methods=["GET", "POST"])
def editar(contrato_id):
    contrato = db.get_or_404(Contrato, contrato_id)
    areas = Area.query.order_by(Area.nombre).all()
    if request.method == "POST":
        _aplicar_formulario(contrato, request.form)
        db.session.commit()
        flash("Contrato actualizado correctamente.", "success")
        return redirect(url_for("contratos.listado"))
    return render_template("contratos/formulario.html", areas=areas, contrato=contrato)


@bp.route("/<int:contrato_id>/eliminar", methods=["POST"])
def eliminar(contrato_id):
    contrato = db.get_or_404(Contrato, contrato_id)
    db.session.delete(contrato)
    db.session.commit()
    flash("Contrato eliminado.", "info")
    return redirect(url_for("contratos.listado"))
