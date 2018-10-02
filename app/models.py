from app import db
from datetime import datetime
# association table
ta_assignment = db.Table(
    'assistants',
    # ForeignKey constraints that column to only allow values that are present in
    # the corresponding table (almost always the primary key for their owning table)
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id')),
    db.Column('workshop_id', db.Integer, db.ForeignKey('workshop.id'))
)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), db.ForeignKey('user.email'))
    name = db.Column(db.String(64), unique=True)
    join_date = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True, nullable=False)
    degree = db.Column(db.String(32))
    university = db.Column(db.String(64))
    assigned_ta = db.relationship(
        'Workshop',
        secondary=ta_assignment,
        backref=db.backref('assistants', lazy='dynamic'))

    assigned_instructor = db.relationship(
        'Workshop',
        backref=db.backref('instructor'))

    def __repr__(self):
        return '<Employee {}, join date: {}>'.format(self.name, self.join_date)

class Workshop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workshop_name = db.Column(db.String(64))
    workshop_category = db.Column(db.Enum(
        "Academy", "DSS", "Corporate", "Others", name="workshop_category"), nullable=False)
    workshop_instructor = db.Column(db.Integer, db.ForeignKey(
        'employee.id'), nullable=False)
    workshop_start = db.Column(db.DateTime, default=datetime.utcnow)
    workshop_hours = db.Column(db.Integer)
    workshop_venue = db.Column(db.String(64))
    class_size = db.Column(db.Integer)
    responses = db.relationship('Response', backref='workshop', lazy='dynamic')

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workshop_id = db.Column(db.Integer, db.ForeignKey('workshop.id'), nullable=False)
    difficulty = db.Column(db.Integer)
    assistants_score = db.Column(db.Integer)
    knowledge = db.Column(db.Integer)
    objectives = db.Column(db.Integer)
    timeliness = db.Column(db.Integer)
    venue_score = db.Column(db.Integer)
    satisfaction_score = db.Column(db.Integer)
    comments = db.Column(db.Text)