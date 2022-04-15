from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField

from .models.product import Product
from .models.cart import Cart
from .models.recommend import Recommend
from .models.user import User
from .models.review import Product_Review

from flask import Blueprint
bp = Blueprint('product', __name__)


class QuantityForm(FlaskForm):
	qty = IntegerField('Qty')
	submit = SubmitField("Add to Cart")

@bp.route('/product/<product_id>', methods=['GET', 'POST'])
def display_product(product_id):
	if current_user.is_authenticated and session["identity"] == "customer":
		Recommend.update_footprint(current_user.id, product_id)

	product_info = Product.get(product_id)
	
	review_count = Product_Review.total_reviews(product_id)
	average_rating = Product_Review.average_rating(product_id)

	form = QuantityForm()
	
	top_upvotes = Product_Review.get_top_upvotes(product_id)
	most_recent = Product_Review.get_most_recent(product_id)
	
	if current_user.is_authenticated:
		quantity = Cart.get_quantity(current_user.id, product_id)
		if form.validate_on_submit():
			Cart.insert(current_user.id, product_info.product_id, form.qty.data)
			return redirect(url_for('product.display_product', product_id=product_id ))
			#return render_template("product.html",
			#	product_info=product_info,
			#	info = product_id,form=form, top_upvotes = top_upvotes, 
			#	most_recent=most_recent, current_user_id = current_user.id, count = review_count, avg = average_rating, quantity=quantity)
		
		if request.form.get("Upvote_1"):
			if Product_Review.upvote_exists(current_user.id,request.form.get('Upvote_1')):
				Product_Review.downvote(current_user.id,request.form.get('Upvote_1'))
				return redirect(url_for('product.display_product',product_id=product_id))	
			else:
				Product_Review.upvote(current_user.id,request.form.get('Upvote_1'))
				return redirect(url_for('product.display_product',product_id=product_id))
		
		if request.form.get("Upvote_2"):
			if Product_Review.upvote_exists(current_user.id,request.form.get('Upvote_2')):
				Product_Review.downvote(current_user.id,request.form.get('Upvote_2'))
				return redirect(url_for('product.display_product',product_id=product_id))
				
			else:
				Product_Review.upvote(current_user.id,request.form.get('Upvote_2'))
				return redirect(url_for('product.display_product',product_id=product_id))
	else:
		return render_template('no-login.html')
	
	return render_template("product.html", 
				product_info=product_info,
				info = product_id,form=form, top_upvotes = top_upvotes, 
				most_recent=most_recent, current_user_id = current_user.id, count = review_count, avg = average_rating, quantity=quantity)
