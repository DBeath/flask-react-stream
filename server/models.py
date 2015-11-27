from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Factory as FakerFactory

from marshmallow import Schema, fields, ValidationError

db = SQLAlchemy()
faker = FakerFactory.create()


class Entry(db.Model):
    __tablename__ = 'entry'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return '{0}: {1}'.format(self.posted, self.text)


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class EntrySchema(Schema):

    id = fields.Int(dump_only=True)
    text = fields.Str(required=True, validate=must_not_be_blank)
    posted = fields.DateTime(dump_only=True)


class EntryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Entry
        sqlalchemy_session = db.session

    id = factory.Sequence(lambda n: n)
    text = factory.LazyAttribute(lambda t: faker.text(max_nb_chars=140))
    posted = factory.LazyAttribute(lambda d: faker.date_time_between(start_date='-1d', end_date='now'))


