from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, SelectField
from flask_user.forms import RegisterForm


# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    """ Form for User Registration """
    title = StringField('Title')
    first_name = StringField('First Name', validators=[
        validators.DataRequired('First Name is required')])
    last_name = StringField('Last Name', validators=[
        validators.DataRequired('Last Name is required')])


class UserProfileForm(Form):
    """ Form for User Account """
    title = StringField('Title')
    first_name = StringField('First Name', validators=[
        validators.DataRequired('First Name is required')])
    last_name = StringField('Last Name', validators=[
        validators.DataRequired('Last Name is required')])
    affiliation = StringField('Affiliation')
    submit = SubmitField('Save')


class CollectionForm(Form):
    """ Form for Collection """

    # Essential
    name = StringField('Name', validators=[
        validators.DataRequired('Name for collection is required.')])
    description = StringField('Description')
    dataseturl = StringField('Full Dataset URL',
        description=u'Link to an external dataset the maps in this collection have been generated from (for example: "https://openfmri.org/dataset/ds000001" or "http://dx.doi.org/10.15387/fcp_indi.corr.mpg1")')
    contributors = StringField('Contributors')
    accessibility = SelectField('Accessibility',
        choices=[('', ''), ('Public', 'Public'), ('Private', 'Private')],
        description='Public (The collection will be accessible by anyone and all the data in it will be distributed under CC0 license). Private (The collection will be not listed in the INcDb index).')

    # Movie
    movie_name = StringField('Movie Name', validators=[
        validators.DataRequired('Movie Name is required.')])
    viewed_times = StringField('Number of Times previously viewed',
        description=u'The number of times the participant has seen the movie before')
    presentation_method = SelectField('Method of Video Presentation',
        choices=[('', ''), ('Projection and Mirror', 'Projection and Mirror'), ('Goggles', 'Goggles')],
        description=u'How was the movie presented to participants')
    audio_method = StringField('Method of Audio Presentation',
        description=u'For example, air conduction headphones; noise cancelling headphones, etc.')
    window_size = StringField('Size of Display Window',
        description=u'The size of the surface onto which the movie was displayed.')
    visual_angle = StringField('Visual Angle',
        description=u'Degrees of visual angle subtended by the video if known')
    triggered = SelectField('Triggered?',
        choices=[('', ''), ('Unknown', 'Unknown'), ('Yes', 'Yes'), ('No', 'No')],
        description=u'Was the video started by the scanner or vice versa?')
    video_resolution = StringField('Video Resolution')
    video_codec = StringField('Video Codec')
    audio_quality = StringField('Audio Quality (Hz)')
    audio_codec = StringField('Audio Codec')

    # Participant
    participant_age = StringField('Age of Participant')
    handedness = SelectField('Handedness',
        choices=[('',''), ('Right', 'Right'), ('Left', 'Left'), ('Both', 'Both')],
        description=u'Handedness of participants')
    criteria = StringField('Inclusion/Exclusion Criteria',
        description=u'Additional inclusion/exclusion criteria, if any (including specific sampling strategies that limit inclusion to a specific group, such as laboratory members)')
    vision = SelectField('Normal (corrected) vision?', 
        choices=[('',''), ('Unknown','Unknown'), ('Yes','Yes'), ('No','No')])
    hearing = SelectField('Normal (corrected) hearing?', 
        choices=[('',''), ('Unknown','Unknown'), ('Yes','Yes'), ('No','No')])
    native_languages = StringField('Native Languages(s)',
        description=u'What language has the participant spoken fluently/regularly since being able to speak')
    language_proficiency = SelectField('Language Proficiency', 
        choices=[('',''), ('Monolingual','Monolingual'), ('Bilingual', 'Bilingual'), ('Multilingual', 'Multilingual')],
        default="",
        description=u'Does the participant speak multiple languages fluently?')

    # Design
    imaging_runs = StringField('Number of Imaging Runs')
    length_of_runs = StringField('Length of Runs',
        description=u'If multiple runs, length of each imaging run in seconds')

    # Acquisition
    scanner_make = StringField('Scanner Make',
        description=u'Manufacturer of MRI scanner')
    scanner_model = StringField('Scanner Model',
        description=u'Model of MRI scanner')
    field_strength = StringField('Field Strength',
        description=u'Field strength of MRI scanner (in Tesla)')
    pulse_sequence = StringField('Pulse Sequence',
        description=u'Description of pulse sequence used for fMRI')
    parallel_imaging = StringField('Parallel Imaging',
        description=u'Description of parallel imaging method and parameters')
    field_of_view = StringField('Field of View',
        description=u'Imaging field of view in millimeters')
    matrix_size = StringField('Matrix Size',
        description=u'Matrix size for MRI acquisition')
    slice_thickness = StringField('Slice Thickness',
        description=u'Distance between slices (includes skip or distance factor) in millimeters')
    skip_distance = StringField('Skip Distance',
        description=u'The size of the skipped area between slices in millimeters')
    acquisition_orientation = StringField('Acquisition of Orientation',
        description=u'The orientation of slices')
    order_of_acquisition = SelectField('Order of Acquisition', 
        choices=[('',''), ('Ascending', 'Ascending'),('Descending', 'Descending'),('Interleaved', 'Interleaved')],
        description=u'Order of acquisition of slices (ascending, descending, or interleaved)')
    repetition_time = StringField('Repetition Time',
        description=u'Repetition time (TR) in milliseconds')
    echo_time = StringField('Echo Time',
        description=u'Echo time (TE) in milliseconds')
    flip_angle = StringField('Flip Angle',
        description=u'Flip angle in degrees')
