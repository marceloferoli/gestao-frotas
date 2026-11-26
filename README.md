# 🚛 FleetControl | Sistema de Gestão de Frotas e Manutenção

![Dashboard FleetControl](docs/dashboard.jpg)

Sistema Full Stack desenvolvido para controle operacional, financeiro e preventivo de frotas de veículos pesados e leves, unindo práticas de **Logística e Manutenção Eletromecânica** com **Engenharia de Software**.

## 🚀 Funcionalidades
- **Gestão de Veículos:** Cadastro de frota com controle de odômetro e status operacional (`Ativo`, `Em Manutenção`, `Inativo`).
- **Controle de Abastecimento:** Registro de Diesel S10, Diesel S500, Gasolina Comum, Gasolina Aditivada e Etanol, com validação de odômetro e cálculo automático de média de consumo (`km/l`) e valor por litro.
- **Gestão de Manutenções:** Registro de serviços preventivos e corretivos com atualização automática de status e odômetro.
- **Dashboard Financeiro:** Consolidação em tempo real dos custos de combustível, manutenção e custo operacional total por veículo e da frota inteira.

## 🛠️ Tecnologias Utilizadas
- **Back-end:** Python 3 (Programação Orientada a Objetos) e Flask
- **Banco de Dados:** PostgreSQL (`psycopg2`)
- **Front-end:** HTML5, Bootstrap 5 e Jinja2

## ⚙️ Como Executar Localmente
1. Clone o repositório e crie o ambiente virtual:
   ```bash
   git clone https://github.com
   cd gestao-frotas
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Crie o banco `gestao_frotas` no PostgreSQL, ajuste as credenciais em `database/conexao.py` e rode:
   ```bash
   python app.py
   ```

---
Desenvolvido por **Marcelo Oliveira**
