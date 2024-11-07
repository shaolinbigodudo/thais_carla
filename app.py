from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para criar o banco de dados e a tabela (com a nova coluna 'classification')
def create_database():
    try:
        # Conecta ao banco de dados SQLite (o banco será criado se não existir)
        conn = sqlite3.connect('imc.db')
        cursor = conn.cursor()

        # Cria a tabela com a nova coluna 'classification' se não existir
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS imc_result (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            imc REAL NOT NULL,
            classification TEXT NOT NULL
        )
        ''')

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Erro ao criar banco de dados: {str(e)}")

# Função para adicionar um novo resultado no banco de dados
def add_imc_result(name, weight, height, imc, classification):
    try:
        conn = sqlite3.connect('imc.db')
        cursor = conn.cursor()

        # Insere os dados na tabela
        cursor.execute('''
        INSERT INTO imc_result (name, weight, height, imc, classification)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, weight, height, imc, classification))

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"Erro ao adicionar dados no banco: {str(e)}")

# Função para recuperar todos os resultados do banco de dados
def get_all_imc_results():
    try:
        conn = sqlite3.connect('imc.db')
        cursor = conn.cursor()

        # Recupera todos os resultados
        cursor.execute('SELECT * FROM imc_result')
        results = cursor.fetchall()

        conn.close()
        return results

    except Exception as e:
        print(f"Erro ao recuperar dados do banco: {str(e)}")
        return []

# Função para calcular o IMC e determinar a classificação
def calculate_imc(weight, height):
    imc = weight / (height ** 2)
    if imc < 18.5:
        classification = "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        classification = "Peso normal"
    elif 25 <= imc < 29.9:
        classification = "Sobrepeso"
    else:
        classification = "Obesidade"
    return round(imc, 2), classification

# Rota para a página inicial
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Recupera os dados do formulário
        name = request.form['name']
        weight = float(request.form['weight'])
        height = float(request.form['height'])

        # Calcula o IMC e a classificação
        imc, classification = calculate_imc(weight, height)

        # Adiciona o resultado no banco de dados
        add_imc_result(name, weight, height, imc, classification)

        # Redireciona para a página de histórico
        return redirect(url_for('history'))

    return render_template('index.html')

# Rota para mostrar o histórico de cálculos
@app.route('/history')
def history():
    results = get_all_imc_results()  # Obtém todos os resultados do banco de dados
    return render_template('history.html', results=results)

# Rota para limpar o histórico de cálculos
@app.route('/clear_history', methods=['POST'])
def clear_history():
    try:
        conn = sqlite3.connect('imc.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM imc_result')  # Deleta todos os registros
        conn.commit()
        conn.close()
        return redirect(url_for('history'))  # Redireciona de volta para a página de histórico
    except Exception as e:
        print(f"Erro ao limpar histórico: {str(e)}")
        return redirect(url_for('history'))  # Se der erro, redireciona sem limpar

if __name__ == '__main__':
    create_database()  # Cria o banco de dados ao iniciar o app
    app.run(debug=True)




















