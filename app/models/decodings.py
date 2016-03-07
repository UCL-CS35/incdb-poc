import datetime
from app import db
from app.models.analysis import AnalysisSet


class DecodingSet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    analysis_set_id = db.Column(db.Integer,
                                db.ForeignKey(AnalysisSet.id), nullable=True)
    analysis_set = db.relationship(AnalysisSet,
                                   backref=db.backref('decoding_set'))
    name = db.Column(db.String(20))
    n_images = db.Column(db.Integer)
    n_voxels = db.Column(db.Integer)
    is_subsampled = db.Column(db.Boolean)


class Decoding(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))
    uuid = db.Column(db.String(32), unique=True)
    movie = db.Column(db.String(200))
    term = db.Column(db.String(200))
    correlation = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image_decoded_at = db.Column(db.DateTime,
                                 onupdate=datetime.datetime.utcnow)

    # Relationships
    decoding_set_id = db.Column(db.Integer, db.ForeignKey(DecodingSet.id))
    decoding_set = db.relationship(
        DecodingSet, backref=db.backref(
            'decodings',
            cascade='all, delete-orphan'))
