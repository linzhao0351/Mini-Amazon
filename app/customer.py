from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList, IntegerField

from .models.cart import Cart
from .models.recommend import Recommend

from flask import Blueprint
bp = Blueprint('customer', __name__)

@bp.route('/customer')
def customer():
	if current_user.is_authenticated:
		recent_viewed = Recommend.rec_recent_viewed_item(current_user.id)
		no_recent_viewed = recent_viewed is None
		if no_recent_viewed:
			pass
		else:
			recent_viewed = recent_viewed[0:min(len(recent_viewed),5)]

		most_viewed = Recommend.rec_most_viewed_item(current_user.id)
		no_most_viewed = most_viewed is None
		if no_most_viewed:
			pass
		else:
			most_viewed = most_viewed[0:min(len(most_viewed),5)]

		return render_template('customer.html', recent_viewed=recent_viewed, no_recent_viewed=no_recent_viewed,
												most_viewed=most_viewed, no_most_viewed=no_most_viewed)
	else:
		return redirect(url_for('index.index'))


@bp.route('/customer/account', methods=['GET', 'POST'])
def customer_portal():
	if current_user.is_authenticated:
		return render_template('customer_portal.html', user_id=current_user.id)
	else:
		return redirect(url_for('index.index'))


class ItemForm(FlaskForm):
	product_id = StringField('Product ID')
	product_name = StringField('Product Name')
	price = StringField('Price')
	quantity = StringField('Quantity')
	
class CartForm(FlaskForm):
	items = FieldList(FormField(ItemForm))
	submit = SubmitField('Update Cart')


@bp.route('/customer/account/my-cart', methods=['GET', 'POST'])
def my_cart():
	cart_form = CartForm()

	if "Update" in request.form:
		# Update cart
		for item in cart_form.items:
			Cart.update(current_user.id, item.product_id.data, item.quantity.data)
		return redirect(url_for('customer.my_cart'))

	if "Clear" in request.form:
		# clear cart
		Cart.clear(current_user.id)
		return redirect(url_for('customer.my_cart'))


	if "Submit" in request.form:
		for item in cart_form.items:
			Cart.update(current_user.id, item.product_id.data, item.quantity.data)
		return redirect(url_for('customer.order_summary'))

	cart = Cart.get(current_user.id)
	for item in cart:
		item_form = ItemForm()
		item_form.product_id = item.product_id
		item_form.product_name = item.product_name
		item_form.price = item.price
		item_form.quantity = item.quantity

		cart_form.items.append_entry(item_form)

	return render_template('customer_my_cart.html', cart_form=cart_form)


@bp.route('/customer/account/my-cart/delete/<product_id>', methods=['GET', 'POST'])
def delete_item(product_id):
	Cart.delete(current_user.id, product_id)
	return redirect(url_for('customer.my_cart'))


@bp.route('/customer/account/my-cart/order_summary', methods=['GET', 'POST'])
def order_summary():
	cart = Cart.get(current_user.id)
	total_amount = sum([item.quantity * item.price for item in cart])

	if "Submit" in request.form:
		try:
			order_id = Cart.submit_aggregate(total_amount)
		except:
			return redirect(url_for('customer.order_summary'))

		try:
			Cart.submit_detail(current_user.id, order_id, cart) 
		except:
			Cart.retract_order(order_id)
			return redirect(url_for('customer.order_summary'))

		Cart.clear(current_user.id)
		return redirect(url_for('customer.success_order', order_id=order_id))

	return render_template('order_summary.html', cart=cart, total_amount=total_amount)

@bp.route('/customer/account/my-cart/success_order/<order_id>')
def success_order(order_id):
	return render_template('success_order.html', order_id=order_id)


@bp.route('/customer/account/my-orders')
def my_orders():
	msg = "Hello world!"
	return render_template('customer_my_orders.html', info = msg)


@bp.route('/customer/account/my-profile')
def my_profile():
	msg = "Hello world!"
	return render_template('customer_my_profile.html', info = msg)


@bp.route('/customer/account/my-messages')
def my_messages():
	msg = "Hello world!"
	return render_template('customer_my_messages.html', info = msg)

