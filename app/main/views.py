from flask import render_template, session, redirect, url_for, request, \
    current_app, flash
from . import main
from .forms import PostForm, CommentForm
from .. import db
from ..models import User, Post, Comment
from ..decorators import admin_required
from flask_login import current_user


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['GRITY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', posts=posts, pagination=pagination)

@main.route('/archives')
def achives():
    user = User.query.filter_by(is_administrator=True).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('archives.html', posts=posts)

@admin_required
@main.route('/write', methods=['GET', 'POST'])
def write():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, summary=form.summary.data,
            content=form.content.data, author_id= \
            current_user._get_current_object().id)
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template('write.html', form=form)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(username=form.name.data, email=form.email.data,
            content=form.content.data, post=post)
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id))
    comments = post.comments.order_by(Comment.timestamp.asc()).all()
    return render_template('post.html', posts=[post], form=form, comments=comments)

@admin_required
@main.route('/comment/moderate/<id>')
def comment_moderate(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False if comment.disabled else True
    db.session.add(comment)
    return redirect(url_for('.post', id=comment.post_id))

@admin_required
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.summary = form.summary.data
        post.content = form.content.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.summary.data = post.summary
    form.content.data = post.content
    return render_template('edit_post.html', form=form)
