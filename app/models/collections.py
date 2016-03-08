from app import db
from app.models.users import *


class Collection(db.Model):

    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    name = db.Column(db.String(100), nullable=False, server_default='', unique=True)
    description = db.Column(db.String(255), nullable=True, server_default='')
    dataseturl = db.Column(db.Unicode(255), nullable=True, server_default=u'')
    contributors = db.Column(db.Unicode(255), nullable=True, server_default=u'')
    accessibility = db.Column(db.String(10), nullable=True, server_default='')

    movie_name = db.Column(db.String(100), nullable=True, server_default='')
    viewed_times = db.Column(db.Integer())
    presentation_method = db.Column(db.String(100), nullable=True, server_default='')
    audio_method = db.Column(db.String(100), nullable=True, server_default='')
    window_size = db.Column(db.String(100), nullable=True, server_default='')
    visual_angle = db.Column(db.Integer())
    triggered = db.Column(db.String(10), nullable=True, server_default='')
    video_resolution = db.Column(db.String(50), nullable=True, server_default='')
    video_codec = db.Column(db.String(50), nullable=True, server_default='')
    audio_quality = db.Column(db.String(50), nullable=True, server_default='')
    audio_codec = db.Column(db.String(50), nullable=True, server_default='')

    participant_age = db.Column(db.Integer())
    handedness = db.Column(db.String(10), nullable=True, server_default='')
    criteria = db.Column(db.String(255), nullable=True, server_default='')
    vision = db.Column(db.String(10), nullable=True, server_default='')
    hearing = db.Column(db.String(10), nullable=True, server_default='')
    native_languages = db.Column(db.String(255), nullable=True, server_default='')
    language_proficiency = db.Column(db.String(255), nullable=True, server_default='')

    imaging_runs = db.Column(db.Integer())
    length_of_runs = db.Column(db.String(255), nullable=False, server_default='')

    scanner_make = db.Column(db.String(255), nullable=True, server_default='')
    scanner_model = db.Column(db.String(255), nullable=True, server_default='')
    field_strength = db.Column(db.String(255), nullable=True, server_default='')
    pulse_sequence = db.Column(db.String(255), nullable=True, server_default='')
    parallel_imaging = db.Column(db.String(255), nullable=True, server_default='')
    field_of_view = db.Column(db.String(255), nullable=True, server_default='')
    matrix_size = db.Column(db.String(255), nullable=True, server_default='')
    slice_thickness = db.Column(db.String(255), nullable=True, server_default='')
    skip_distance = db.Column(db.String(255), nullable=True, server_default='')
    acquisition_orientation = db.Column(db.String(255), nullable=True, server_default='')
    order_of_acquisition = db.Column(db.String(10), nullable=True, server_default='')
    repetition_time = db.Column(db.String(255), nullable=True, server_default='')
    echo_time = db.Column(db.String(255), nullable=True, server_default='')
    flip_angle = db.Column(db.String(255), nullable=True, server_default='')

    def get_username(self):
        username = User.query.get(self.user_id).first_name
        return username
