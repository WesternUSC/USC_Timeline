from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required
from usctimeline import db
from usctimeline.models import Category
from usctimeline.categories.forms import CategoryForm

categories = Blueprint('categories', __name__)


@categories.route("/category/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.name.data = category.name
    return render_template(
        'categories/edit_category.html',
        title='Update Category',
        form=form
    )


@categories.route("/category/manage")
@login_required
def manage_categories():
    categories = Category.query.all()
    return render_template(
        'categories/manage_categories.html',
        title='Manage Categories',
        categories=categories
    )
