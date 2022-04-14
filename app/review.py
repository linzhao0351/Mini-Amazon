from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, DecimalField, SelectField, TextAreaField

from .models.review import Product_Review, Seller_Review

from flask import Blueprint
bp = Blueprint('review', __name__)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review Content')
    rating = SelectField(u'Rating', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    submit = SubmitField('Post your review')


@bp.route('/product/<product_id>/review', methods = ['GET','POST'])
def write_review(product_id):
    # make sure only customer who bought the product can review
    if session["identity"] == "customer":
        if Product_Review.check_order(current_user.id, product_id):
            pass
        else:
            return redirect(url_for('product.display_product', product_id=product_id))
    else:
        return redirect(url_for('product.display_product', product_id=product_id))

    msg = product_id
    review_form = ReviewForm(request.form)
    if request.method == 'POST':
        if request.form.get("Submit_review"):
            try:
                if review_form.validate_on_submit():
                    Product_Review.add_review(current_user.id,product_id,review_form.review.data, review_form.rating.data,0)
                    return redirect(url_for('product.display_product', product_id=product_id))
                else:
                    flash('Your rating must be between 0 and 5!', 'warning')
            except Exception as e:
                print(e)
                return render_template('duplicate_review.html', product_id = product_id)

    return render_template("review.html", form = review_form,info = msg)


@bp.route('/product/<product_id>/review/edit', methods = ['GET','POST'])
def edit_review(product_id):
    msg = product_id
    review_form = ReviewForm(request.form)
    if request.method == 'POST':
        # if review_form.validate_on_submit():
        if request.form.get("Edit"):
            if review_form.validate_on_submit():
                Product_Review.update_review(current_user.id,product_id,review_form.review.data, review_form.rating.data)
                # flash('Your review has been published!', 'warning')
                return redirect(url_for('product.display_product', product_id=product_id))
            else:
                flash('Your rating must be between 0 and 5!', 'warning')
        if request.form.get("Delete"):
            Product_Review.delete_review(current_user.id, product_id)
            return redirect(url_for('product.display_product', product_id=product_id))
    current_product_review = Product_Review.get_current_review(current_user.id, product_id)
    review_form.review.data = current_product_review[0][0]
    return render_template("edit_review.html", form = review_form, info = msg)


@bp.route('/seller/<seller_id>/review', methods = ['GET','POST'])
def write_seller_review(seller_id):
    if session["identity"] == "customer":
        if Seller_Review.check_order(current_user.id, seller_id):
            pass
        else:
            return redirect(url_for('product.display_product', product_id=product_id))
    else:
        return redirect(url_for('product.display_product', product_id=product_id))

    msg = seller_id
    review_form = ReviewForm(request.form)
    if request.method == 'POST':
        if request.form.get("Submit_review"):
            try:
                if review_form.validate_on_submit():
                    Seller_Review.add_review(current_user.id,seller_id,review_form.review.data, review_form.rating.data,0)
                    return redirect(url_for('index.index'))
                else:
                    flash('Your rating must be between 0 and 5!', 'warning')
            except:
                return render_template('duplicate_review.html')

    return render_template("review.html", form = review_form,info = msg)


@bp.route('/seller/<seller_id>/review/edit', methods = ['GET','POST'])
def edit_seller_review(seller_id):
    msg = seller_id
    review_form = ReviewForm(request.form)
    if request.method == 'POST':
        # if review_form.validate_on_submit():
        if request.form.get("Edit"):
            if review_form.validate_on_submit():
                Seller_Review.update_review(current_user.id,seller_id,review_form.review.data, review_form.rating.data)
                # flash('Your review has been published!', 'warning')
                return redirect(url_for('index.index'))
            else:
                flash('Your rating must be between 0 and 5!', 'warning')
        if request.form.get("Delete"):
            Seller_Review.delete_review(current_user.id, seller_id)
            return redirect(url_for('index.index'))
    current_seller_review = Seller_Review.get_current_review(current_user.id, seller_id)
    review_form.review.data = current_seller_review[0][0]
    return render_template("edit_review.html", form = review_form, info = msg)
               