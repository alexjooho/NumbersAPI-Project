from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email


class CSRFProtection(FlaskForm):
    """CSRFProtection form, intentionally left blank."""


class EmailAddForm(FlaskForm):
    """Form for adding subscription emails."""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
