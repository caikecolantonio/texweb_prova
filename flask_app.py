from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# from pytz import timezone

app = Flask(__name__)

##### Configurar o banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bancoDeDados.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#####

##### Criar o modelo para o registro do usuario
# class Usuario(db.Model):
#     codigo = 

class Apontamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(25), nullable=True)
    hora = db.Column(db.DateTime, default=datetime.now)
    # hora = db.Column(db.DateTime, default=datetime.now().astimezone(timezone('America/Sao_Paulo')))

# class Usuario(db.Model)
#     login = 
#     email = 

    @property
    def serializar(self):
        return {
            'id': self.id,
            'nome_usuario': self.nome_usuario,
            'hora': str(self.hora)[11:16]
        }

# db.create_all()

@app.route('/inicio')
@app.route('/')
def mostra_inicio():
    return render_template('index.html')

@app.route('/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    if request.method == 'POST':
        print(request.form['nome']) # a pessoa digitou
        usuario = Apontamento(nome_usuario=request.form['nome'])
        db.session.add(usuario)
        db.session.commit()
        return render_template('index.html')

    if request.method == 'GET':
        ultimos10 = Apontamento.query.order_by(-Apontamento.id).limit(10).all()
        print(ultimos10)
        j = jsonify(funcionarios=[i.serializar for i in ultimos10])
        print(j)
        return j
        

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


# @app.route('/login')
# def login():
#     return render_template('login.html')





## Para rodar o projeto em desenvolvimento

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
