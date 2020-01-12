import re

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from app.models import User, Paper, Comment


def get_papers():
    return Paper.query()


class EditProfileForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_name(self, name):
        if name.data != self.original_name:
            user = User.query.filter_by(name=self.name.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')




class PaperForm(FlaskForm):
    title = StringField('Title *', validators=[DataRequired()])
    first_author = StringField('First author')
    last_author = StringField('Last author')
    doi = StringField('DOI *', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '4')])
    comment = TextAreaField('Comment')

    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    paper = QuerySelectField('Paper', query_factory=get_papers, allow_blank=False)
    rating = SelectField('Rating', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '4')])
    comment = TextAreaField('Comment')

    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    data_type = SelectField('Select if you want to search for papers or users.', choices=[('paper', 'Papers'), ('user', 'Users')])
    search_text = StringField('Search: ', validators=[DataRequired()])

    submit = SubmitField('Submit')


class ModifyDataForm(FlaskForm):
    submit = SubmitField('Modify')
