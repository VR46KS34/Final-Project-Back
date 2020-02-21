import os
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, User, Meeting, Topic, Guest

from flask_mail import Mail, Message

BASE_DIR=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.config.update(
        DEBUG=True,        
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = 'blueorkasta@gmail.com',
        MAIL_PASSWORD = 'ajnqiqkumxicaccc'
        )
mail = Mail(app)

db.init_app(app)

Migrate(app, db)

manager = Manager(app)
manager.add_command("db",MigrateCommand)

@app.route("/")
def home():
    return render_template("index.html")
    

# @app.route("/contacts", methods=['GET', 'POST']) 
# @app.route("/contacts/<int:id>", methods=['GET', 'PUT', 'DELETE'])
# def contacts(id=None):
#     if request.method =='GET':
#         if id is not None:
#             contact=Contact.query.get(id)
#             if contact:
#                 return jsonify(contact.serialize()), 200
#             else:
#                 return jsonify({"msg":"Contact not found"}), 404
#         else:
#             contacts = Contact.query.all()
#             contacts = list(map(lambda contact: contact.serialize(), contacts))
#             return jsonify(contacts), 200

#     if request.method =='POST':
#         name = request.json.get('name', None)
#         phone = request.json.get('phone', None)

#         if not name:
#             return jsonify({"msg": "name is required"}), 422
#         if not phone:
#             return jsonify({"msg": "phone is required"}), 422  

#         contact = Contact()
#         contact.name = name
#         contact.phone = phone

#         db.session.add(contact)
#         db.session.commit()

#         return jsonify(contact.serialize()), 201

#     if request.method =='PUT':

#         name = request.json.get('name', None)
#         phone = request.json.get('phone', None)

#         if not name:
#             return jsonify({"msg": "name is required"}), 422
#         if not phone:
#             return jsonify({"msg": "phone is required"}), 422  
             
#         contact = Contact.query.get(id)

#         if not contact:                
#                 return jsonify({"msg":"Contact not found"}), 404

#         contact.name = name
#         contact.phone = phone

#         db.session.commit()

#         return jsonify(contact.serialize()), 200

#     if request.method =='DELETE':
#         contact = Contact.query.get(id)

#         if not contact:                
#                 return jsonify({"msg":"Contact not found"}), 404

#         db.session.delete(contact)
#         db.session.commit()

#         return jsonify({"msg":"Contact deleted"}), 200

CORS(app)

@app.route("/api/users", methods=['GET', 'POST']) 
@app.route("/api/users/<int:id>", methods=['GET', 'PUT', 'DELETE'])

def users(id=None):
    if request.method =='GET':
        if id is not None:
            user=User.query.get(id)
            if user:
                return jsonify(user.serialize()), 200
            else:
                return jsonify({"msg":"user not found"}), 404
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200

    if request.method =='POST':
        fullname = request.json.get('fullname', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        repeated_pass = request.json.get('repeated_pass', None)
        #meetings = request.json.get('meetings', None)
        if mail is not None:
            validate = User.query.filter_by(email=email).first()
            if validate:
                return jsonify({
                    "status": "Alerta",
                    "msg": "Mail Ya en uso"}), 401 
        if not fullname:
            return jsonify({
                "status": "Alerta",
                "msg": "El nombre es requerido"}), 422
        if not email:
            return jsonify({
                "status": "Alerta",
                "msg": "email es requerido"}), 422  
        if not password:
            return jsonify({
                "status": "Alerta",
                "msg": "contraseña es requerida"}), 422 
        if not repeated_pass:
            return jsonify({
                "status": "Alerta",
                "msg": "segunda contraseña es requerida"}), 422 
        if password != repeated_pass:
            return jsonify({
                "status": "Alerta",
                "msg": "Las contraseñas no coinciden"
            }),401
        user = User()
        user.fullname = fullname
        user.email = email
        user.password = password
        db.session.add(user)
        db.session.commit()
        objeto = {
                "status": "Success",
                "msg": "Registro Correcto"
            }
        usuario = user.serialize()
        respuesta = {**objeto, **usuario}
        return jsonify(respuesta), 201

    if request.method =='PUT':

        fullname = request.json.get('fullname', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        #meetings = request.json.get('meetings', None)

        if not fullname:
            return jsonify({"msg": "fullname is required"}), 422
        if not email:
            return jsonify({"msg": "email is required"}), 422  
        if not password:
            return jsonify({"msg": "password is required"}), 422 
             
        user = User.query.get(id)

        if not user:                
                return jsonify({"msg":"user not found"}), 404

        user.fullname = fullname
        user.email = email
        user.password = password

        db.session.commit()

        return jsonify(user.serialize()), 200

    if request.method =='DELETE':
        user = User.query.get(id)

        if not user:                
            return jsonify({"msg":"user not found"}), 404

        db.session.delete(user)
        db.session.commit()           

        return jsonify({"msg":"user deleted"}), 200


@app.route("/user/login", methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if request.method =='POST':
        if not email:
            return jsonify({
                "status": "Alerta",
                "msg": "Email es requerido"}), 401
        if not password:
            return jsonify({
                "status": "Alerta", 
                "msg": "Contraseña es requerida"}), 401
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                "status": "Alerta",
                "msg": "El usuario no existe"}), 404
        if password != user.password:
            return jsonify({
                "status": "Alerta",
                "msg": "Contraseña incorrecta"}), 401
        if password == user.password:
            objeto = {
                "status": "Success",
                "msg": "Autentificacion Correcta"
            }
            usuario = user.serialize()
            respuesta = {**objeto, **usuario}
            return jsonify(respuesta), 200
        else:
            return jsonify({
                "status": "Alerta",
                "msg": "Something happened"}), 500
    else:
        return jsonify({"msg": "Bad request method"}), 401


@app.route("/api/meetings", methods=['GET', 'POST']) 
@app.route("/api/meetings/<int:id>", methods=['GET', 'PUT', 'DELETE'])
#@app.route("/api/meetings/user/<int:user_id>", methods=['GET', 'POST']) 
#@app.route("/api/meetings/<int:id>/user/<int:user_id>", methods=['GET', 'PUT', 'DELETE'])
def meetings(id=None):
    if request.method =='GET':
        if id is not None:
            meeting=Meeting.query.get(id)
            if meeting:
                return jsonify(meeting.serialize()), 200
            else:
                return jsonify({"msg":"meeting not found"}), 404
        else:
            meetings = Meeting.query.all()
            meetings = list(map(lambda meeting: meeting.serialize(), meetings))
            return jsonify(meetings), 200


    if request.method =='POST':
               
        #create_date = request.json.get('create_date', None)
        meeting_date = request.json.get('meeting_date', None)
        meeting_hour = request.json.get('meeting_hour', None)
        project_name = request.json.get('project_name', None)
        title = request.json.get('title', None)       
        topics = request.json.get('topics', None) 
        guests = request.json.get('guests', None) 
        place = request.json.get('place', None)
        description = request.json.get('description', None) 
        target = request.json.get('target', None) 
        done = request.json.get('done', None) 
        user_id = request.json.get('user_id', None)

        if not meeting_date:
            return jsonify({"msg": "date is required"}), 422
        if not meeting_hour:
            return jsonify({"msg": "hour is required"}), 422
        if not project_name:
            return jsonify({"msg": "project name is required"}), 422
        if not title:
            return jsonify({"msg": "title is required"}), 422          
        if not place:
            return jsonify({"msg": "place is required"}), 422 

        meeting = Meeting()
        #meeting.create_date = create_date
        meeting.meeting_date = meeting_date
        meeting.meeting_hour = meeting_hour
        meeting.project_name = project_name
        meeting.title = title       
        meeting.place = place
        meeting.description = description
        meeting.target = target
        meeting.done = done
        meeting.user_id = user_id

        db.session.add(meeting)
        db.session.commit()


        if topics:
            if len(topics) > 1:
                for x in range(len(topics)):
                    top = Topic()
                    top.title = topics[x]["title"]
                    top.priority = topics[x]["priority"]
                    top.notes = topics[x]["notes"]
                    top.care = topics[x]["care"]
                    top.tracking = topics[x]["tracking"]
                    top.duration = topics[x]["duration"]
                    top.meeting_id = meeting.id
                    db.session.add(top)
            else:
                top = Topic()                
                top.title = topics[0]["title"]
                top.priority = topics[0]["priority"]
                top.notes = topics[0]["notes"]
                top.care = topics[0]["care"]
                top.tracking = topics[0]["tracking"]
                top.duration = topics[0]["duration"]
                top.meeting_id = meeting.id
                db.session.add(top)
            
            db.session.commit()


        if guests:
            if len(guests) > 1:
                for x in range(len(guests)):
                    gue = Guest()
                    gue.fullname = guests[x]["fullname"]
                    gue.email = guests[x]["email"]
                    gue.rol = guests[x]["rol"]                  
                    gue.meeting_id = meeting.id
                    db.session.add(gue)
            else:                
                    gue = Guest()                
                    gue.fullname = guests[0]["fullname"]
                    gue.email = guests[0]["email"]
                    gue.rol = guests[0]["rol"]                  
                    gue.meeting_id = meeting.id       
                    db.session.add(gue)
            
            db.session.commit()

        return jsonify(meeting.serialize()), 201

    if request.method =='PUT':

        #create_date = request.json.get('create_date', None)
        meeting_date = request.json.get('meeting_date', None)
        meeting_hour = request.json.get('meeting_hour', None)
        project_name = request.json.get('project_name', None)
        title = request.json.get('title', None)     
        topics = request.json.get('topics', None) 
        guests = request.json.get('guests', None)    
        place = request.json.get('place', None)
        description = request.json.get('description', None) 
        target = request.json.get('target', None) 
        done = request.json.get('done', None) 
        user_id = request.json.get('user_id', None)

        # if not meeting_date:
        #     return jsonify({"msg": "date is required"}), 422
        # if not meeting_hour:
        #     return jsonify({"msg": "hour is required"}), 422
        # if not project_name:
        #     return jsonify({"msg": "project name is required"}), 422
        # if not title:
        #     return jsonify({"msg": "title is required"}), 422         
        # if not place:
        #     return jsonify({"msg": "place is required"}), 422 
             
        meeting = Meeting.query.get(id)

        if not meeting:                
                return jsonify({"msg":"meeting not found"}), 404

        #meeting.create_date = create_date
        meeting.meeting_date = meeting_date
        meeting.meeting_hour = meeting_hour
        meeting.project_name = project_name
        meeting.title = title         
        meeting.place = place
        meeting.description = description
        meeting.target = target
        meeting.done = done
        meeting.user_id = user_id

        db.session.commit()
        
        if topics:
            if len(topics) > 0:
                for x in range(len(topics)):
                    if topics[x]["id"] == 0: 
                        top = Topic()
                        top.title = topics[x]["title"]
                        top.priority = topics[x]["priority"]
                        top.notes = topics[x]["notes"]
                        top.care = topics[x]["care"]
                        top.tracking = topics[x]["tracking"]
                        top.duration = topics[x]["duration"]
                        top.meeting_id = meeting.id
                        db.session.add(top)
                    else:
                        top = Topic.query.get(topics[x]["id"])
                        top.title = topics[x]["title"]
                        top.priority = topics[x]["priority"]
                        top.notes = topics[x]["notes"]
                        top.care = topics[x]["care"]
                        top.tracking = topics[x]["tracking"]
                        top.duration = topics[x]["duration"]
                        top.meeting_id = meeting.id
                    
            db.session.commit()  

        if guests:
            if len(guests) > 0:
                for x in range(len(guests)):
                    if guests[x]["id"] == 0:
                        gue = Guest()
                        gue.fullname = guests[x]["fullname"]
                        gue.email = guests[x]["email"]
                        gue.rol = guests[x]["rol"]                      
                        gue.meeting_id = meeting.id
                        db.session.add(gue)
                    else:
                        gue = Guest.query.get(guests[x]["id"])
                        gue.fullname = guests[x]["fullname"]
                        gue.email = guests[x]["email"]
                        gue.rol = guests[x]["rol"]                      
                        gue.meeting_id = meeting.id

            db.session.commit()      

        return jsonify(meeting.serialize()), 200

    if request.method =='DELETE':
      
        Topic.query.filter_by(meeting_id=id).delete()
        Guest.query.filter_by(meeting_id=id).delete()                     
        meeting = Meeting.query.get(id)

        if not meeting:                
                return jsonify({"msg":"meeting not found"}), 404

        db.session.delete(meeting)
        db.session.commit()
        return jsonify({"msg":"meeting deleted"}), 200




@app.route("/api/topics", methods=['GET', 'POST']) 
@app.route("/api/topics/<int:id>", methods=['GET', 'PUT', 'DELETE'])

def topics(id=None):
    if request.method =='GET':
        if id is not None:
            topic = Topic.query.get(id)
            if topic:
                return jsonify(topic.serialize()), 200
            else:
                return jsonify({"msg":"topic not found"}), 404
        else:
            topics = Topic.query.all()
            topics = list(map(lambda topic: topic.serialize(), topics))
            return jsonify(topics), 200

    if request.method =='POST':
        title = request.json.get('title', None)
        priority = request.json.get('priority', None)
        notes = request.json.get('notes', None)
        care = request.json.get('care', None)
        tracking = request.json.get('tracking', None)
        duration = request.json.get('duration', None)
        meeting_id = request.json.get('meeting_id', None)
        
        if not title:
            return jsonify({"msg": "title is required"}), 422
        if not priority:
            return jsonify({"msg": "priority is required"}), 422
        
        topic = Topic()
        topic.title = title
        topic.priority = priority
        topic.notes = notes
        topic.care = care
        topic.tracking = tracking
        topic.duration = duration  
        topic.meeting_id = meeting_id      

        db.session.add(topic)
        db.session.commit()

        return jsonify(topic.serialize()), 201

    if request.method =='PUT':

        title = request.json.get('title', None)
        priority = request.json.get('priority', None)
        notes = request.json.get('notes', None)
        care = request.json.get('care', None)
        tracking = request.json.get('tracking', None)
        duration = request.json.get('duration', None)
        meeting_id = request.json.get('meeting_id', None)

        if not title:
            return jsonify({"msg": "title is required"}), 422
        if not priority:
            return jsonify({"msg": "priority is required"}), 422
             
        topic = Topic.query.get(id)

        if not topic:                
                return jsonify({"msg":"topic not found"}), 404

        topic.title = title
        topic.priority = priority
        topic.notes = notes
        topic.care = care
        topic.tracking = tracking
        topic.duration = duration 
        topic.meeting_id = meeting_id

        db.session.commit()

        return jsonify(topic.serialize()), 200

    if request.method =='DELETE':
        topic = Topic.query.get(id)

        if not topic:                
            return jsonify({"msg":"topic not found"}), 404

        db.session.delete(topic)
        db.session.commit()

        return jsonify({"msg":"topic deleted"}), 200



@app.route("/api/guests", methods=['GET', 'POST']) 
@app.route("/api/guests/<int:id>", methods=['GET', 'PUT', 'DELETE'])

def guests(id=None):
    if request.method =='GET':
        if id is not None:
            guest = Guest.query.get(id)
            if guest:
                return jsonify(guest.serialize()), 200
            else:
                return jsonify({"msg":"guest not found"}), 404
        else:
            guests = Guest.query.all()
            guests = list(map(lambda guest: guest.serialize(), guests))
            return jsonify(guests), 200

    if request.method =='POST':

        fullname= request.json.get('fullname', None)
        email= request.json.get('email', None)
        rol= request.json.get('rol', None)
        meeting_id = request.json.get('meeting_id', None)
    
        if not fullname:
            return jsonify({"msg": "fullname is required"}), 422        
               
        guest = Guest()
        guest.fullname = fullname
        guest.email = email
        guest.rol = rol
        guest.meeting_id = meeting_id
                
        db.session.add(guest)
        db.session.commit()

        return jsonify(guest.serialize()), 201

    if request.method =='PUT':

        fullname= request.json.get('fullname', None)
        email= request.json.get('email', None)
        rol= request.json.get('rol', None)
        meeting_id = request.json.get('meeting_id', None)
       
        if not fullname:
            return jsonify({"msg": "fullname is required"}), 422
             
        guest = Guest.query.get(id)

        if not guest:                
                return jsonify({"msg":"guest not found"}), 404

        guest.fullname = fullname
        guest.email = email
        guest.rol = rol 
        guest.meeting_id = meeting_id       

        db.session.commit()

        return jsonify(guest.serialize()), 200

    if request.method =='DELETE':
        guest = Guest.query.get(id)

        if not guest:                
                return jsonify({"msg":"guest not found"}), 404

        db.session.delete(guest)
        db.session.commit()

        return jsonify({"msg":"guest deleted"}), 200





    
@app.route('/api/sendInvitation', methods=['GET', 'POST']) 
def send_invitation(): 

    if request.method =='POST':   
        user = request.json.get('user', None)        
        title = request.json.get('title', None)
        #description = request.json.get('description', None)
        date = request.json.get('meeting_date', None)
        hour = request.json.get('meeting_hour', None)
        place = request.json.get('place', None)
        topics = request.json.get('topics', None)
        recipients = request.json.get('guest_mails', None)      
        
        if not title:
            return jsonify({"msg": "title is required"}), 422
        if not date:
            return jsonify({"msg": "date is required"}), 422
        if not hour:
            return jsonify({"msg": "hour is required"}), 422
        if not place:
            return jsonify({"msg": "place is required"}), 422
        if not recipients:
            return jsonify({"msg": "recipients are required"}), 422
        
        try:
            msg = Message('Se cita a reunión "'+title+'"'+" para el día "+("/".join(reversed(date.split("-"))))+" a las "+hour+" hrs.",
                sender = "blueorkasta@gmail.com",
                recipients=recipients)
            #msg.body = topics                
            
            html_message="<h2>Estimad@:</h2><br>"+"<h2>Los temas a revisar y sus tiempos estimados serán los siguientes:</h2>"
            for i in range(len(topics)):              
                html_message += "<h3>Tema "+str(i+1)+": "+ topics[i]["title"] +". Tiempo: "+str(topics[i]["duration"])+" minutos.</h3>"
           
            total_duration=0
            for j in range(len(topics)):              
                total_duration += int(topics[j]["duration"])

            html_message+="<br><h2>La reunión será realizada en "+place+" en el horario indicado en el asunto y tendrá una duración total estimada de "+str(total_duration)+" minutos.</h2><h2>Se solicita puntualidad.</h2>"+"<h2>Atentamente,</h2><br>"+"<h2>"+user+"</h2>"
            
            msg.html = html_message
            mail.send(msg)
            
            return jsonify({"msg": "Mail sent"}), 200

        except Exception as e:
            return str(e)



@app.route('/api/sendMeeting', methods=['GET', 'POST']) 
def send_meeting(): 

    if request.method =='POST':    
        user = request.json.get('user', None)
        title = request.json.get('title', None)
        date = request.json.get('meeting_date', None)
        topics = request.json.get('topics', None)
        recipients = request.json.get('guest_mails', None)      
        
        if not title:
            return jsonify({"msg": "title is required"}), 422
        if not recipients:
            return jsonify({"msg": "recipients are required"}), 422
        
        try:
            msg = Message('Acta de reunión "'+ title+'"'+" realizada el "+("/".join(reversed(date.split("-")))),
                sender = "blueorkasta@gmail.com",
                recipients=recipients)
            #msg.body = topics                
            
            html_message="<h2>Estimad@:</h2><h2>A continuación se presenta una síntesis de los temas y acuerdos tomados durante la reunión:</h2>"
            for i in range(len(topics)):              
                html_message += "<h2>Tema "+str(i+1)+": "+ topics[i]["title"] +"</h2>"+"<h4>Prioridad: "+topics[i]["priority"]+"</h4>"+"<h4>Fecha de Seguimento: "+topics[i]["tracking"]+"</h4>"+"<h4>Responsable: "+topics[i]["care"]+"</h4>"+"<h4>Notas: "+topics[i]["notes"]+"</h4><br>"
            html_message += "<h2>Atentamente,</h2><br>"+"<h2>"+user+"</h2>"

            msg.html = html_message
            mail.send(msg)
            
            return jsonify({"msg": "Mail sent"}), 200

        except Exception as e:
            return str(e)



if __name__=="__main__":
    manager.run()
