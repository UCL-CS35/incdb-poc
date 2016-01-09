from flask_wtf import Form
from wtforms import StringField, SubmitField, validators, RadioField
from flask_user.forms import RegisterForm

# Define the User Registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    title = StringField('Title')
    first_name = StringField('First Name', validators=[
        validators.DataRequired('First Name is required')])
    last_name = StringField('Last Name', validators=[
        validators.DataRequired('Last Name is required')])


# Define the User Profile form
class UserProfileForm(Form):
    title = StringField('Title')
    first_name = StringField('First Name', validators=[
        validators.DataRequired('First Name is required')])
    last_name = StringField('Last Name', validators=[
        validators.DataRequired('Last Name is required')])
    affiliation = StringField('Affiliation')
    submit = SubmitField('Save')


# Define the Collecetion form
class CollectionForm(Form):

    # Essential
    name = StringField('Name')
    description = StringField('Description')
    dataseturl = StringField('Dataset URL')
    contributors = StringField('Contributors')
    accessibility = RadioField('Accessibility', 
        choices=[('Public','Public'),('Private','Private')], 
        default='Public')

    # Movie
    movie_name = StringField('Movie Name')
    viewed_times = StringField('Number of Times previously viewed')
    presentation_method = RadioField('Method of Video Presentation', 
        choices=[('Projection and Mirror','Projection and Mirror'),('Goggles','Goggles')],
        default='Projection and Mirror')
    audio_method = StringField('Method of Audio Presentation')
    window_size = StringField('Size of Display Window')
    visual_angle = StringField('Visual Angle')
    triggered = RadioField('Triggered?', 
        choices=[('Unknown','Unknown'),('Yes','Yes'),('No','No')],
        default='Unknown')
    video_resolution = StringField('Video Resolution')
    video_codec = StringField('Video Codec')
    audio_quality = StringField('Audio Quality')
    audio_codec = StringField('Audio Codec')

    # Participant
    participant_age = StringField('Age of Participant')
    hardness = RadioField('Hardness', 
        choices=[('Right','Right'),('Left','Left'),('Both','Both')],
        default='Right')
    criteria = StringField('Inclusion/Exclusion Criteria')
    vision = RadioField('Normal (corrected) vision?', 
        choices=[('Unknown','Unknown'),('Yes','Yes'),('No','No')],
        default='Unknown')
    hearing = RadioField('Normal (corrected) hearing?', 
        choices=[('Unknown','Unknown'),('Yes','Yes'),('No','No')]
        ,default='Unknown')
    native_languages = StringField('Native Languages(s)')
    language_proficiency = RadioField('Language Proficiency', 
        choices=[('Monolingual','Monolingual'),('Bilingual','Bilingual'),('Multilingual','Multilingual')],
        default='Monolingual')

    # Design
    imaging_runs = StringField('Number of Imaging Runs')
    length_of_runs = StringField('Length of Runs')

    scanner_make = StringField('Scanner Make')
    scanner_model = StringField('Scanner Model')
    field_strength = StringField('Field Strength')
    pulse_sequence = StringField('Pulse Sequence')
    parallel_imaging = StringField('Parallel Imaging')
    field_of_view = StringField('Field of View')
    matrix_size = StringField('Matrix Size')
    slice_thickness = StringField('Slice Thickness')
    skip_distance = StringField('Skip Distance')
    acquisition_orientation = StringField('Acquisition of Orientation')
    order_of_acquisition = RadioField('Order of Acquisition', 
        choices=[('Ascending','Ascending'),('Descending','Descending'),('Interleaved','Interleaved')],
        default='Ascending')
    repetition_time = StringField('Repetition Time')
    echo_time = StringField('Echo Time')
    flip_angle = StringField('Flip Angle')
    