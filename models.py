from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Contact(db.Model):
#     __tablename__="contacts"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50),nullable=False)
#     phone = db.Column(db.String(50),nullable=False)

#     def __repr__(self):
#         return "<Contact %r>" % self.name
    
#     def serialize(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "phone": self.phone
#         }


class User(db.Model):  
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50),nullable=False)    
    #meetings = db.relationship('Meeting', backref='users')                                                                    
    
    def __repr__(self):
        return "<User %r>" % self.id
    
    def serialize(self):
       # meetings=[]

        #if self.meetings:            
        #    meetings=list(map(lambda meeting:meeting.serialize(), self.meetings))
        
        return {
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "password": self.password,
            #"meetings" : meetings         
        }


class Meeting(db.Model):
    __tablename__="meetings"
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.String(50),nullable=False)
    meeting_date = db.Column(db.String(50),nullable=False)
    meeting_hour = db.Column(db.String(50),nullable=False)
    project_name = db.Column(db.String(50))
    title = db.Column(db.String(50),nullable=False)   
    topics = db.relationship('Topic', backref='meetings')
    guests = db.relationship('Guest', backref='meetings')
    place = db.Column(db.String(50))
    description = db.Column(db.String(50))
    target = db.Column(db.String(50))

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    user = db.relationship(User)

    def __repr__(self):
        return "<Meeting %r>" % self.title
    
    def serialize(self):
        topics=[]
        guests=[]

        if self.topics:            
            topics=list(map(lambda topic:topic.serialize(), self.topics))

        if self.guests:            
            guests=list(map(lambda guest:guest.serialize(), self.guests))

        return {          
            "id" : self.id,
            "create_date" : self.create_date,
            "meeting_date" : self.meeting_date,
            "meeting_hour" : self.meeting_hour,
            "project_name" : self.project_name,
            "title" : self.title,
            "topics" : topics, 
            "guests" : guests,        
            "place" : self.place,
            "description" : self.description,
            "target" : self.target,
            "user_id" : self.user_id, 
            #"user" : self.user.serialize()
        }


class Topic(db.Model):
    __tablename__="topics"
    id = db.Column(db.Integer, primary_key=True)   
    title = db.Column(db.String(50),nullable=False)
    priority = db.Column(db.String(50))
    notes = db.Column(db.String(50))
    care = db.Column(db.String(50))
    tracking = db.Column(db.String(50))
    duration = db.Column(db.Integer)    

    meeting_id = db.Column(db.Integer,db.ForeignKey('meetings.id'),nullable=False)
    meeting = db.relationship(Meeting)
    
    def __repr__(self):
        return "<Topic %r>" % self.title
    
    def serialize(self):
        return {          
            "id" : self.id,            
            "title" : self.title,
            "priority" : self.priority,
            "notes" : self.notes,
            "care" : self.care,
            "tracking" : self.tracking,
            "duration" : self.duration,
            "meeting_id" : self.meeting_id,     
            #"meeting" : self.meeting.serialize()   
        }

class Guest(db.Model):
    __tablename__="guests"
    id = db.Column(db.Integer, primary_key=True)    
    fullname= db.Column(db.String(50), nullable=False)
    email= db.Column(db.String(50))
    rol= db.Column(db.String(50))

    meeting_id = db.Column(db.Integer,db.ForeignKey('meetings.id'),nullable=False)
    meeting = db.relationship(Meeting)

    def __repr__(self):
        return "<Guest %r>" % self.fullname
    
    def serialize(self):
        return {          
            "id" : self.id,
            "fullname" : self.fullname,
            "email" : self.email,
            "rol" : self.rol,   
            "meeting_id" : self.meeting_id,                    
            #"meeting" : self.meeting.serialize()
        }