import os
from flask import Flask, request, jsonify, render_template
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, User, Meeting, Topic, Guest

BASE_DIR=os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

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
        #meetings = request.json.get('meetings', None)

        if not fullname:
            return jsonify({"msg": "fullname is required"}), 422
        if not email:
            return jsonify({"msg": "email is required"}), 422  
        if not password:
            return jsonify({"msg": "password is required"}), 422 

        user = User()
        user.fullname = fullname
        user.email = email
        user.password = password

        db.session.add(user)
        db.session.commit()

        # if meetings:
        #     if len(meetings) > 1:
        #         for x in range(len(meetings)):
        #             met = Meeting()
        #             met.create_date = meetings[x]["create_date"]
        #             met.meeting_date = meetings[x]["meeting_date"]
        #             met.meeting_hour = meetings[x]["meeting_hour"]
        #             met.project_name = meetings[x]["project_name"]
        #             met.title = meetings[x]["title"]
        #             met.topics = meetings[x]["topics"]
        #             met.guests = meetings[x]["guests"]
        #             met.place = meetings[x]["place"]
        #             met.description = meetings[x]["description"]
        #             met.user_id = user.id
        #             db.session.add(met)
        #     else:
        #         met = Address()
        #         met.create_date = meetings[0]["create_date"]
        #         met.meeting_date = meetings[0]["meeting_date"]
        #         met.meeting_hour = meetings[0]["meeting_hour"]
        #         met.project_name = meetings[0]["project_name"]
        #         met.title = meetings[0]["title"]
        #         met.topics = meetings[0]["topics"]
        #         met.guests = meetings[0]["guests"]
        #         met.place = meetings[0]["place"]
        #         met.description = meetings[0]["description"]
        #         met.user_id = user.id                
        #         db.session.add(met)
            
        #     db.session.commit()

        return jsonify(user.serialize()), 201

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

        # if meetings:
        #     if len(meetings) > 0:
        #         for x in range(len(meetings)):
        #             if meetings[x]["id"]:
        #                 met = Meeting.query.get(meetings[x]["id"])                                                
        #                 met.create_date = meetings[x]["create_date"]
        #                 met.meeting_date = meetings[x]["meeting_date"]
        #                 met.meeting_hour = meetings[x]["meeting_hour"]
        #                 met.project_name = meetings[x]["project_name"]
        #                 met.title = meetings[x]["title"]
        #                 met.topics = meetings[x]["topics"]
        #                 met.guests = meetings[x]["guests"]
        #                 met.place = meetings[x]["place"]
        #                 met.description = meetings[x]["description"]
        #                 met.user_id = user.id
        #             else:
        #                 met = Metting()
        #                 met.create_date = meetings[x]["create_date"]
        #                 met.meeting_date = meetings[x]["meeting_date"]
        #                 met.meeting_hour = meetings[x]["meeting_hour"]
        #                 met.project_name = meetings[x]["project_name"]
        #                 met.title = meetings[x]["title"]
        #                 met.topics = meetings[x]["topics"]
        #                 met.guests = meetings[x]["guests"]
        #                 met.place = meetings[x]["place"]
        #                 met.description = meetings[x]["description"]
        #                 met.user_id = user.id               
        #                 db.session.add(met)

        #     db.session.commit()

        return jsonify(user.serialize()), 200

    if request.method =='DELETE':
        user = User.query.get(id)

        if not user:                
                return jsonify({"msg":"user not found"}), 404

        db.session.delete(user)
        db.session.commit()           

        return jsonify({"msg":"user and their meetings deleted"}), 200



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
               
        create_date = request.json.get('create_date', None) # FUNCION QUE DEVUELVA EL DIA DE HOY
        meeting_date = request.json.get('meeting_date', None)
        meeting_hour = request.json.get('meeting_hour', None)
        project_name = request.json.get('project_name', None)
        title = request.json.get('title', None)       
        topics = request.json.get('topics', None) 
        guests = request.json.get('guests', None) 
        place = request.json.get('place', None)
        description = request.json.get('description', None) 
        target = request.json.get('target', None) 
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
        meeting.create_date = create_date
        meeting.meeting_date = meeting_date
        meeting.meeting_hour = meeting_hour
        meeting.project_name = project_name
        meeting.title = title       
        meeting.place = place
        meeting.description = description
        meeting.target = target
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

        create_date = request.json.get('create_date', None)
        meeting_date = request.json.get('meeting_date', None)
        meeting_hour = request.json.get('meeting_hour', None)
        project_name = request.json.get('project_name', None)
        title = request.json.get('title', None)     
        topics = request.json.get('topics', None) 
        guests = request.json.get('guests', None)    
        place = request.json.get('place', None)
        description = request.json.get('description', None) 
        target = request.json.get('target', None) 
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

        meeting.create_date = create_date
        meeting.meeting_date = meeting_date
        meeting.meeting_hour = meeting_hour
        meeting.project_name = project_name
        meeting.title = title         
        meeting.place = place
        meeting.description = description
        meeting.target = target
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






if __name__=="__main__":
    manager.run()


