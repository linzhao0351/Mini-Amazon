from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField

from .models.product import Product
from .models.cart import Cart
from .models.recommend import Recommend
from .models.user import User

from flask import Blueprint
bp = Blueprint('product', __name__)


class QuantityForm(FlaskForm):
	qty = IntegerField('Qty')
	submit = SubmitField("Add to Cart")

@bp.route('/product/<product_id>', methods=['GET', 'POST'])
def display_product(product_id):
	if current_user.is_authenticated and current_user.identity == 1:
		Recommend.update_footprint(current_user.id, product_id)

	product_info = Product.get(product_id)
	form = QuantityForm()
	if form.validate_on_submit():
		print(form.qty.data)
		Cart.insert(current_user.id, product_info.id, form.qty.data)
		return render_template("product.html", form=form)
	
	return render_template("product.html", info=product_id, form=form)