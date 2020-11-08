from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField
from wtforms.validators import DataRequired

class PictureForm(FlaskForm):
    picture = FileField('Placez votre images ici',
                        validators=[DataRequired(),
                            FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Valider')
