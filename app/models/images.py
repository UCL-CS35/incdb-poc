import datetime
from app import db
from app.models.analysis import TermAnalysis

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