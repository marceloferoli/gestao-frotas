
from flask import Flask, render_template, request, redirect, url_for, flash
from models.veiculo import Veiculo
from models.abastecimento import Abastecimento
from models.manutencao import Manutencao
from services.frota_service import FrotaService

app = Flask(__name__)
app.secret_key = "chave_secreta_frota_local"

@app.route("/")
def index():
    veiculos, resumo = FrotaService.obter_dados_dashboard()
    return render_template("index.html", veiculos=veiculos, resumo=resumo)

@app.route("/veiculo", methods=["POST"])
def novo_veiculo():
    v = Veiculo(
        placa=request.form["placa"],
        modelo=request.form["modelo"],
        ano=int(request.form["ano"]),
        km_atual=int(request.form["km_atual"])
    )
    sucesso, msg = FrotaService.cadastrar_veiculo(v)
    flash(msg, "success" if sucesso else "danger")
    return redirect(url_for("index"))

@app.route("/abastecer", methods=["POST"])
def novo_abastecimento():
    try:
        a = Abastecimento(
            veiculo_id=int(request.form["veiculo_id"]),
            tipo_combustivel=request.form["tipo_combustivel"],
            litros=float(request.form["litros"]),
            valor_total=float(request.form["valor_total"]),
            km_abastecimento=int(request.form["km_abastecimento"])
        )
        sucesso, msg = FrotaService.registrar_abastecimento(a)
        flash(msg, "success" if sucesso else "danger")
    except ValueError as e:
        flash(str(e), "danger")
    return redirect(url_for("index"))

@app.route("/manutencao", methods=["POST"])
def nova_manutencao():
    m = Manutencao(
        veiculo_id=int(request.form["veiculo_id"]),
        tipo=request.form["tipo"],
        descricao=request.form["descricao"],
        custo=float(request.form["custo"]),
        km_manutencao=int(request.form["km_manutencao"])
    )
    sucesso, msg = FrotaService.registrar_manutencao(m, novo_status=request.form["status"])
    flash(msg, "success" if sucesso else "danger")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
