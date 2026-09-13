from pathlib import Path

from flask import Flask, redirect, url_for

from control_contratos.models import Area, db

AREAS_INICIALES = [
    "Legal",
    "Recursos Humanos",
    "Tecnología",
    "Finanzas",
    "Operaciones",
    "Compras",
]


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="views/templates",
        static_folder="static",
    )
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{Path(app.instance_path) / 'contratos.db'}"
    )
    app.config["SECRET_KEY"] = "dev"

    db.init_app(app)

    from control_contratos.controllers.areas import bp as areas_bp
    from control_contratos.controllers.contratos import bp as contratos_bp

    app.register_blueprint(contratos_bp)
    app.register_blueprint(areas_bp)

    @app.route("/")
    def index():
        return redirect(url_for("contratos.listado"))

    with app.app_context():
        db.create_all()
        if not Area.query.first():
            for nombre in AREAS_INICIALES:
                db.session.add(Area(nombre=nombre))
            db.session.commit()

    return app


def main() -> None:
    app = create_app()
    app.run(debug=True)
