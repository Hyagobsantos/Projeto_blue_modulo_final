from flask import (Flask, Blueprint, render_template, request)
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
bp = Blueprint('app', __name__)


user ='wsljzdgv'
password = 'rq4KWQFKb_wvUGBuMJ-pKE9AEVAqGVpM'
host='tuffi.db.elephantsql.com'
database='wsljzdgv'


app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}' 
#definir log = false
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Secreto'

db = SQLAlchemy(app)

class animes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    imagem_url = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255), nullable=False)
    descricao2 = db.Column(db.String(1000), nullable=False)

    def __init__(self, nome,imagem_url,descricao,descricao2):
        self.nome = nome
        self.imagem_url = imagem_url
        self.descricao = descricao
        self.descricao2 = descricao2

    @staticmethod
    def ListarAnimes():
        return animes.query.order_by(animes.id.asc()).all()

    @staticmethod
    def ListarAnimeSingle(anime_id):
        return animes.query.get(anime_id)
    
    def salvar(self):
        db.session.add(self)
        db.session.commit()
    
    def atualizar(self, novo):
        self.nome = novo.nome
        self.imagem_url = novo.imagem_url
        self.descricao = novo.descricao
        self.descricao2 = novo.descricao2
        self.salvar()
    
    def deletar(self):
        db.session.delete(self)
        db.session.commit()


@bp.route('/')
def listar_animes():
    animesLista = animes.ListarAnimes()
    return render_template("index.html", animesLista = animesLista)

@bp.route('/listar/<anime_id>')
def listar_anime(anime_id):
    anime = animes.ListarAnimeSingle(anime_id)
    return render_template('listarSingle.html', anime = anime)

@bp.route('/criar', methods=('GET','POST'))
def criar():
    id_anime = None
    if request.method == 'POST':
        form = request.form
        anime = animes(form['nome'], form['imagem_url'], form['descricao'], form['descricao2'])
        anime.salvar()
        id_anime = anime.id
    return render_template('create.html', id_anime = id_anime)

@bp.route('/atualiza/<anime_id>', methods=('GET','POST'))
def atualizar(anime_id):
    sucesso = None
    anime = animes.ListarAnimeSingle(anime_id)

    if request.method == 'POST':
        form = request.form
        novo = animes(form['nome'], form['imagem_url'], form['descricao'], form['descricao2'])
        anime.atualizar(novo)
        sucesso = True
    return render_template('atualiza.html', anime = anime, sucesso=sucesso)

@bp.route('/deletar/<anime_id>')
def deletar(anime_id):
    anime = animes.ListarAnimeSingle(anime_id)
    return render_template('deletar.html', anime=anime)

@bp.route('/deletar/<anime_id>/confirmed')
def deletar_confirmed(anime_id):
    sucesso = None
    anime = animes.ListarAnimeSingle(anime_id)
    if anime:
        anime.deletar()
        sucesso = True
    return render_template('deletar.html', sucesso=sucesso)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)





