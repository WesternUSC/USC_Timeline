from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required
from usctimeline import db
from usctimeline.models import Tag
from usctimeline.tags.forms import TagForm

tags = Blueprint('tags', __name__)


@tags.route("/tag/new", methods=['GET', 'POST'])
@login_required
def new_tag():
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash('Tag has been created!', 'success')
        return redirect(url_for('tags.manage_tags'))
    return render_template(
        'edit_tag.html',
        title='New Tag',
        form=form,
        legend='New Tag'
    )


@tags.route("/tag/manage")
@login_required
def manage_tags():
    tags = Tag.query.all()
    return render_template(
        'manage_tags.html',
        title='Manage Tags',
        tags=tags
    )


@tags.route("/tag/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_tag(id):
    tag = Tag.query.get_or_404(id)
    form = TagForm()
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.commit()
        flash('Tag has been updated', 'success')
        return redirect(url_for('tags.manage_tags'))
    elif request.method == 'GET':
        form.name.data = tag.name
    return render_template(
        'edit_tag.html',
        title='Update Tag',
        form=form,
        legend='Update Tag'
    )


@tags.route("/tag/<int:id>/delete")
@login_required
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag has been deleted', 'success')
    return redirect(url_for('main.index'))


@tags.route("/tag/<int:id>/delete/confirm")
@login_required
def delete_tag_confirmation(id):
    tag = Tag.query.get_or_404(id)
    return render_template(
        'delete_tag_confirmation.html',
        title='Delete Tag Confirmation',
        tag=tag
    )
