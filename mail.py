
from flask import Flask
from flask_mail import Mail, Message
import smtplib


app = Flask(__name__)
app.config.update(
        DEBUG=True,        
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = 'blueorkasta@gmail.com',
        MAIL_PASSWORD = 'ajnqiqkumxicaccc'
        )
mail = Mail(app)

#####     COMO COMPATIBILIZAR ESTE SERVIDOR de mail.py CON EL SERVIDOR DE app.py ?      #####
#####             COMO SE LLAMA ESTA FUNCION DE CORREOS DESDE EL FRONT?                 #####

@app.route('/api/send_mail')
def send_mail():
    try:
        msg = Message("Send Testing Message", # EXPECIFICAR TITULO MINUTA X
            sender = "blueorkasta@gmail.com",
            recipients=["luisreyessegner@gmail.com"]) # COLOCAR A INVITADOS REUNIÓN X
        #msg.body = "testing" 
        msg.html = "<b>testing</b>" # MOSTRAR MINUTA X
        mail.send(msg)
        
        return 'Mail sent'

    except Exception as e:
        return str(e)

  
  
if __name__=="__main__":
    app.run()

       
