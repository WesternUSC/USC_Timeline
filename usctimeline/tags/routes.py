from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import login_required
from usctimeline import db
from usctimeline.models import Tag
from usctimeline.tags.forms import TagForm

tags = Blueprint('tags', __name__)


@tags.route("/tag/new", methods=['GET', 'POST'])
@login_required
def new_tag():
    """Route for creating a new Tag instance.

    Returns:
        If the form is successfully submitted, a redirect to the manage_tags
        route in the tags module is returned.
        Otherwise, a rendered HTML template for this route is returned.
    """
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash('Tag has been created!', 'success')
        return redirect(url_for('tags.manage_tags'))
    return render_template(
        'tags/edit_tag.html',
        title='New Tag',
        form=form,
        legend='New Tag'
    )


@tags.route("/tag/manage")
@login_required
def manage_tags():
    """Route for managing all existing tags.

    Returns:
        A rendered HTML template for this route.
    """
    tags = Tag.query.all()
    return render_template(
        'tags/manage_tags.html',
        title='Manage Tags',
        tags=tags
    )


@tags.route("/tag/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_tag(id):
    """Route for updating a specific Tag's information.

    Args:
        id: ID of the Tag to be updated.

    Returns:
        If the form submission is valid and a Tag with <id> exists, then a
        redirect to the manage_tags route inside the tags module is returned.
        If a Tag with <id> does not exist, then a 404 page is returned.
        Otherwise, a rendered HTML template for this route is returned.
    """
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
        'tags/edit_tag.html',
        title='Update Tag',
        form=form,
        legend='Update Tag'
    )


@tags.route("/tag/<int:id>/delete")
@login_required
def delete_tag(id):
    """Route for deleting a specific Tag.

    Args:
        id: ID of the Tag to be deleted.

    Returns:
        If a Tag with <id> exists, then a redirect to the index route in the
        main module is returned.
        Otherwise, a 404 page is returned.
    """
    tag = Tag.query.get_or_404(id)
    db.session.delete(tag)
    db.session.commit()
    flash('Tag has been deleted', 'success')
    return redirect(url_for('main.index'))


@tags.route("/tag/<int:id>/delete/confirm")
@login_required
def delete_tag_confirmation(id):
    """Route for confirming the deletion of a Tag.

    Args:
        id: ID of the Tag to be deleted.

    Returns:
        If a Tag with <id> exists then a rendered HTML template for this route
        is returned.
        Otherwise, a 404 page is returned.
    """
    tag = Tag.query.get_or_404(id)
    return render_template(
        'tags/delete_tag_confirmation.html',
        title='Delete Tag Confirmation',
        tag=tag
    )
