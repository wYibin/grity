from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, Length
from flask_pagedown.fields import PageDownField

class PostForm(Form):
    title = StringField('Title', validators=[Required()])
    summary = StringField('Summary', validators=[Required()])
    content = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(Form):
    name = StringField('Name', validators=[Required(), Length(1, 64)])
    email = StringField('Email', validators=[Required(), Length(1, 64),
        Email()])
    content = StringField("Comment", validators=[Required()])
    submit = SubmitField('Submit')
