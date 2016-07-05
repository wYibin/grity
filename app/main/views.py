from flask import render_template, session, redirect, url_for
from . import main
from .forms import PostForm
from .. import db
from ..models import User, Post
from ..decorators import admin_required
from flask_login import current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', pots=posts)

@admin_required
@main.route('/post', methods=['GET', 'POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, summary=form.summary.data,
            content=form.content.data, author_id= \
            current_user._get_current_object().id)
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template('post.html', form=form)
