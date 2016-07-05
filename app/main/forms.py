from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

class PostForm(Form):
    title = StringField('Title', validators=[Required()])
    summary = StringField('Summary', validators=[Required()])
    content = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')
