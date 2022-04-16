from flask import Flask, render_template,request
from flask_mail import Mail, Message
from celery import

import redis
keyslang="Slang"
keysig="Significado"
r= redis.Redis(host='127.0.0.1',port=6379)
r.set("id",-1)


def Añadir(Slang,Significado):
    r.incr("id")
    r.rpush(keyslang, Slang)
    r.rpush(keysig, Significado)
    print("\n Se agregó el slang con éxito")

#Slangant = slang anterior, Slangact= slang actual
def editarregistro(SlangAnt,newSlang,newSignificado):
    CantSlang = r.llen(keyslang)
    for i in range(CantSlang):
        Slangact = r.lindex(kesyslang, i).decode('utf-8')
        if(Slangact == SlangAnt):
            r.lset(keyslang, i, NewSlang)
            r.lset(keysig, i, NewSignificado)
            break
    print("El slang"+SlangAnt+"ha sido editado")

def verregistros():
    CantSlang = r.llen(keyslang)
    for i in range(CantSlang):
        print(f'{i + 1}. Slang: {r.lindex(keyslang, i).decode("utf-8")} \n Significado: {r.lindex(keysig, i).decode("utf-8")}')

def revisar(Slang):
    Cantslang=r.llen(keyslang)
    slangexist=False
    for i in range(Cantslang):
        Slangact = r.lindex(keyslang, i).decode('utf-8')
        if(Slangact == Slang):
            slangexist = True
            break
    return slangexist

def eliminarregistro(Slang):
    CantSlang = r.llen(keyslang)
    slangs=[]
    for i in range(CantSlang):
        slangs.append(({"name": r.lindex(keyslang, i).decode(
            "utf-8"), "definicion": r.lindex(keysig, i).decode("utf-8")}))
    retunr slangs

print(r.keys())

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("Index.html")

@app.route('/Add', methods=['GET', 'POST'])
def Add():
    if request.method == 'POST':
        Slang = request.form["word"]
        Significado = request.form["meaning"]
        if revisar(Slang) == False:
            Añadir(Slang, Significado)
            return render_template("Add.html", message="Slang agregado")
        else:
            return render_template("Add.html", message="Esta palabra ya esta en el diccionario")

    return render_template("Add.html")

@app.route('/Editar', methods=['GET', 'POST'])
  if request.method == 'POST':
        slangant = request.form["oldWord"]
        slangnew = request.form["word"]
        significadonew = request.form["meaning"]

        if revisar(slangant):
            editarregistro(slangant, slangnew,significadonew)

            return render_template("Editar.html", message=False)
        else:

            return render_template("Editar.html", message=True)

    return render_template("Editar.html")

@app.route('/Eliminar',methods=['GET', 'POST'])
def eliminar():
    if request.method == 'POST':
        Slang = request.form["word"]


        if revisar(palabra):
            eliminarregistro(Slang)
            verregistros()
            return render_template("Eliminar.html", message=False)
        else:
            verregistros()
            return render_template("Eliminar.html", message=True)
        
    return render_template("Eliminar.html")
@app.route('/Lista', methods=['GET', 'POST'])
def listaslangs():
    listaslangs = verregistros()
    return render_template("listasslangs.html", palabras=listaslangs)

@app.route('/Buscarsignificado', methods=['GET', 'POST'])
def BuscarSignificado():
     if request.method == 'POST':
        Slang = request.form["Slang"]
        if revisar(palabra):
            CantSlang = r.llen(keyslang)
            for i in range(CantSlang):
                 Slangact = r.lindex(keyslang, i).decode('utf-8')
                 if(Slangact == Slang):
                    gSlang = {"Slang": Slang, "Significado": r.lindex(
                        keysig, i).decode("utf-8")}

                    return render_template("BuscarSignificado.html", ShowWord=gSlang)

         else:
            return render_template("BuscarSignificado.html", message=True)
    return render_template("BuscarSignificado.html")

##TAREA CELERY ENVIAR CORREO ELECTRONICO
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '57f2ff6b9a0188'
app.config['MAIL_PASSWORD'] = 'f82835a15c4057'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

celery = Celery(app.name, broker='redis://localhost:6379/0')
mail = Mail(app)
@Celery.task
def send_async_email(email_data):
    print(email_data + "hola")
    msg = Message(email_data['subject'],
                  sender='franciscoeduardo@rubioduarte.com',
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    mail.send(msg)

@app.route('/sendEmail', methods=['GET', 'POST'])
def sendEmail():
    if request.method == 'GET':
        return render_template('sendEmail.html')

    email = request.form['email']
    message = request.form['message']

    email_data = {
        'subject': 'Hello from the other side!',
        'to': email,
        'body': message,
    }

    send_async_email(email_data)
    
if __name__ == "__main__":
    app.run(debug=True)


