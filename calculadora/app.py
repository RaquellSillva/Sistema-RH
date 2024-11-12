from flask import Flask, render_template, request, redirect, url_for, send_file, session
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')  # default to production



# Função de cálculo para gerar o relatório
def calcular_salario(salario, horas, atraso, extras, taxa, aliquota_inss, bonus, vavr):
    valorhora = round(salario / horas, 2) if horas > 0 else 0
    valorhoraextra = round(valorhora * extras * (1 + taxa), 2)
    descontoatraso = round(valorhora * atraso, 2)
    dinss = round(salario * aliquota_inss, 2)
    fgts = round(salario * 0.08, 2)
    descontovavr = round(vavr, 2) if vavr else 0
    liquido = round(salario + bonus + valorhoraextra - descontoatraso - dinss - fgts - descontovavr, 2)

    return {
        'valorhora': valorhora,
        'valorhoraextra': valorhoraextra,
        'descontoatraso': descontoatraso,
        'dinss': dinss,
        'fgts': fgts,
        'descontovavr': descontovavr,
        'liquido': liquido
    }

# Função para criar o PDF com layout aprimorado
def gerar_pdf(dados):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    # Título do Relatório
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, altura - 100, "Relatório de Cálculo de Salário")
    
    # Linha divisória abaixo do título
    p.line(80, altura - 110, largura - 80, altura - 110)

    # Subtítulo e espaçamento inicial
    p.setFont("Helvetica-Bold", 12)
    y = altura - 150
    p.drawString(100, y, "Detalhes do Cálculo:")
    y -= 20  # Espaçamento após o subtítulo

    # Adicionar cada item do cálculo com espaçamento adequado e formato melhorado
    p.setFont("Helvetica", 11)
    for key, value in dados.items():
        # Formatação de cada linha com rótulo em negrito
        p.drawString(100, y, f"{key.capitalize()}:")
        p.drawRightString(400, y, f"R$ {value:.2f}")
        y -= 20  # Espaço entre cada linha
    
    # Linha divisória no final do conteúdo
    y -= 10  # Pequeno espaço antes da linha
    p.line(80, y, largura - 80, y)

    # Finalizar o PDF
    p.save()
    buffer.seek(0)
    return buffer

# Rota para a tela de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        # Verifique se o usuário e senha são válidos 
        if usuario == "admin" and senha == "senha123":
            session['usuario'] = usuario  # Armazenar o usuário na sessão
            return redirect(url_for('calculadora'))
        else:
            return render_template('login.html', msgError="Usuário ou senha incorretos.")
    return render_template('login.html')

# Rota para a tela de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form['usuario']
        senha = request.form['senha']
        
        # Armazenando os dados de cadastro na sessão 
        session['usuario'] = email
        session['senha'] = senha

        return redirect(url_for('calculadora'))  # Após cadastro, redireciona para a página de cálculo

    return render_template('cadastro.html')

# Rota para a calculadora de salário
@app.route('/calculadora', methods=['GET', 'POST'])
def calculadora():
    if 'usuario' not in session:
        return redirect(url_for('login'))  # Redireciona para login se não estiver autenticado

    resultado = None
    if request.method == 'POST':
        try:
            salario = float(request.form['salario'])
            horas = float(request.form['horas'])
            atraso = float(request.form['atraso'])
            extras = float(request.form['extras'])
            taxa = float(request.form['taxa']) / 100
            aliquota_inss = float(request.form['aliquota']) / 100
            bonus = float(request.form['bonus'])
            vavr = float(request.form['vavr']) if request.form['resposta'].lower() == 's' else 0

            resultado = calcular_salario(salario, horas, atraso, extras, taxa, aliquota_inss, bonus, vavr)
            session['resultado'] = resultado  # Armazenar o resultado na sessão
        except ValueError:
            resultado = {
                'valorhora': 0,
                'valorhoraextra': 0,
                'descontoatraso': 0,
                'dinss': 0,
                'fgts': 0,
                'descontovavr': 0,
                'liquido': 0
            }
            session['resultado'] = resultado
    return render_template('index.html', resultado=resultado)

# Rota para baixar o PDF
@app.route('/relatorio_pdf')
def relatorio_pdf():
    if 'usuario' not in session:
        return redirect(url_for('login'))  # Redireciona para login se não estiver autenticado

    dados = session.get('resultado')  # Pega o resultado da sessão
    if not dados:
        return "Nenhum cálculo encontrado. Por favor, faça o cálculo primeiro.", 400
    pdf = gerar_pdf(dados)
    return send_file(pdf, as_attachment=True, download_name="relatorio_salario.pdf", mimetype='application/pdf')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Remove o usuário da sessão
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
