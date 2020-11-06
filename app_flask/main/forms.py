from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from main.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Pseudo',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])

    email = StringField('E-mail',
                        validators=[DataRequired(),
                                    Email()])

    password = PasswordField('Mot de passe',
                             validators=[DataRequired()])

    confirm_password = PasswordField('Confirmez votre mot de passe',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])

    submit = SubmitField('Valider')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                f'Le pseudo {user.username} est déjà pris. Choisissez un autre pseudo.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'Un compte existe déjà avec cette adresse e-mail')


class LoginForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(),
                                    Email()])

    password = PasswordField('Mot de passe',
                             validators=[DataRequired()])

    remember = BooleanField('Se souvenir de moi')

    submit = SubmitField('Connection')


class UpdateAccountForm(FlaskForm):
    username = StringField('Pseudo',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])

    email = StringField('E-mail',
                        validators=[DataRequired(),
                                    Email()])

    picture = FileField('Modifier la photo de profile',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Valider')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    f'Le pseudo {user.username} est déjà pris. Choisissez un autre pseudo.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError(
                    'Un compte existe déjà avec cette adresse e-mail')


class PostForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Envoyer')
