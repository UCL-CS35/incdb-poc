import datetime
from flask_user import UserMixin

from app import db


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    title = db.Column(db.Unicode(10), nullable=False, server_default=u'')
    affiliation = db.Column(db.Unicode(10), nullable=False, server_default=u'')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles', backref=db.backref('users', lazy='dynamic'))
    collections = db.relationship('Collection', backref='users', lazy='dynamic')

# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    name = db.Column(db.String(100), nullable=False, server_default='', unique=True)
    description = db.Column(db.String(255), nullable=True, server_default='')
    dataseturl = db.Column(db.Unicode(255), nullable=True, server_default=u'')
    contributors = db.Column(db.Unicode(255), nullable=True, server_default=u'')
    accessibility = db.Column(db.String(10), nullable=True, server_default='Public')

    movie_name = db.Column(db.String(100), nullable=False, server_default='')
    viewed_times = db.Column(db.Integer())
    presentation_method = db.Column(db.String(100), nullable=False, server_default='Projection and Mirror')
    audio_method = db.Column(db.String(100), nullable=True, server_default='')
    window_size = db.Column(db.String(100), nullable=True, server_default='')
    visual_angle = db.Column(db.Integer())
    triggered = db.Column(db.String(10), nullable=False, server_default='Unknown')
    video_resolution = db.Column(db.String(50), nullable=True, server_default='')
    video_codec = db.Column(db.String(50), nullable=True, server_default='')
    audio_quality = db.Column(db.String(50), nullable=True, server_default='')
    audio_codec = db.Column(db.String(50), nullable=True, server_default='')

    participant_age = db.Column(db.Integer())
    hardness = db.Column(db.String(10), nullable=False, server_default='Right')
    criteria = db.Column(db.String(255), nullable=True, server_default='')
    vision = db.Column(db.String(10), nullable=False, server_default='Unknown')
    hearing = db.Column(db.String(10), nullable=False, server_default='Unknown')
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
    order_of_acquisition = db.Column(db.String(10), nullable=False, server_default='Ascending')
    repetition_time = db.Column(db.String(255), nullable=True, server_default='')
    echo_time = db.Column(db.String(255), nullable=True, server_default='')
    flip_angle = db.Column(db.String(255), nullable=True, server_default='')

class AnalysisSet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    n_analyses = db.Column(db.Integer, default=0)
    type = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.now)

class Analysis(db.Model):

    __tablename__ = 'analysis'
    id = db.Column(db.Integer, primary_key=True)
    analysis_set_id = db.Column(db.Integer, db.ForeignKey(AnalysisSet.id))
    name = db.Column(db.String(100), unique=False)
    n_studies = db.Column(db.Integer, default=0)
    n_activations = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))
    # images = db.relationship('AnalysisImage', backref=db.backref('analysis', lazy='joined'), lazy='dynamic')
    analysis_set = db.relationship('AnalysisSet', backref=db.backref(
        'analyses', cascade='all'))
    display = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'analysis',
        'polymorphic_on': type
    }

    @property
    def reverse_inference_image(self):
        """ Convenience method for accessing the reverse inference image. """
        return self.images[1]

class TermAnalysis(Analysis):
    __tablename__ = 'term_analysis'
    id = db.Column(db.Integer, db.ForeignKey('analysis.id'), primary_key=True)
    images = db.relationship('TermAnalysisImage', backref=db.backref('analysis',
                             cascade='all'))
    cog_atlas = db.Column(db.Text, nullable=True)  # Cognitive Atlas RDF data
    __mapper_args__ = {
        'polymorphic_identity': 'term'
    }

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
    name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image_decoded_at = db.Column(db.DateTime,
                                 onupdate=datetime.datetime.utcnow)

    # Relationships
    decoding_set_id = db.Column(db.Integer, db.ForeignKey(DecodingSet.id))
    decoding_set = db.relationship(
        DecodingSet, backref=db.backref('decodings',
                                        cascade='all, delete-orphan'))

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    label = db.Column(db.String(200))
    kind = db.Column(db.String(200))
    description = db.Column(db.Text)
    stat = db.Column(db.String(200))
    image_file = db.Column(db.String(200))
    type = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.now)

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'image'
    }

    @property
    def uncorrected_image_file(self):
        """ Returns an uncorrected version of the filename if one is found. """
        if '_FDR' not in self.image_file:
            return self.image_file
        return self.image_file.split('_FDR')[0] + '.nii.gz'


class TermAnalysisImage(Image):
    __mapper_args__ = {'polymorphic_identity': 'term'}
    term_analysis_id = db.Column(db.Integer, db.ForeignKey(TermAnalysis.id), nullable=True)
    