from flask import render_template, redirect, url_for, flash, request, flash
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList, IntegerField, PasswordField, BooleanField, SelectField

from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import date
from werkzeug.urls import url_parse

from .models.cart import Cart
from .models.recommend import Recommend
from .models.user import User
from .models.buyer_order import Orders, Search
from .models.review import Product_Review, Seller_Review

from datetime import date

from flask import Blueprint
bp = Blueprint('customer', __name__)



##### Lin's Part
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

	if 'msg' in request.args:
		msg = request.args['msg']
	else:
		msg = ""

	return render_template('customer_my_cart.html', cart_form=cart_form, msg=msg)


@bp.route('/customer/account/my-cart/delete/<product_id>', methods=['GET', 'POST'])
def delete_item(product_id):
	Cart.delete(current_user.id, product_id)
	return redirect(url_for('customer.my_cart'))


@bp.route('/customer/account/my-cart/order_summary', methods=['GET', 'POST'])
def order_summary():
	cart = Cart.get(current_user.id)

	msg = Cart.check_avail(cart)
	if msg != "Valid":
		return redirect(url_for('customer.my_cart', msg=msg))

	total_amount = sum([item.quantity * item.price for item in cart])
	msg = Cart.check_balance(current_user.id, total_amount)
	if msg != "Valid":
		return redirect(url_for('customer.my_cart', msg=msg))


	if "Submit" in request.form:
		try:
			order_id = Cart.submit_aggregate(current_user.id, total_amount)
		except:
			return redirect(url_for('customer.order_summary'))

		try:
			Cart.submit_detail(order_id, cart) 
		except Exception as e:
			print(str(e))
			Cart.retract_order(order_id)
			return redirect(url_for('customer.order_summary'))

		try:
			Cart.update_inventory(cart) 
		except Exception as e:
			print(str(e))
			Cart.retract_order(order_id)
			return redirect(url_for('customer.order_summary'))		

		try:
			Cart.update_balance(current_user.id, total_amount) 
			Cart.update_seller_balance(cart)
		except Exception as e:
			print(str(e))
			Cart.retract_order(order_id)
			return redirect(url_for('customer.order_summary'))		



		Cart.clear(current_user.id)
		return redirect(url_for('customer.success_order', order_id=order_id))

	return render_template('order_summary.html', cart=cart, total_amount=total_amount)

@bp.route('/customer/account/my-cart/success_order/<order_id>')
def success_order(order_id):
	return render_template('success_order.html', order_id=order_id)

@bp.route('/customer/account/my-cart/cancel/<order_id>/<product_id>', methods=['GET', 'POST'])
def cancel_item(order_id, product_id):
	Cart.cancel_item(current_user.id, order_id, product_id)
	return redirect(url_for('customer.my_orders'))



### Mae's Part

class Update_profile(FlaskForm):
	firstname = StringField('firstname', validators=[DataRequired()])
	lastname = StringField('lastname', validators=[DataRequired()])
	email = StringField('email', validators=[Email(), DataRequired()])
	nickname = StringField('nickname', validators=[DataRequired()])
	address = StringField('address', validators=[DataRequired()])
	submit = SubmitField('Update', validators=[DataRequired()])

class Search_order(FlaskForm):
	search = StringField('Search', validators=[DataRequired()])
	submit = SubmitField('Search')

@bp.route('/public_profile/customer/<buyer_id>')
def public_profile(buyer_id):
	cuser = User.get(buyer_id)
	return render_template('customer_public_profile.html', cuser = cuser)


@bp.route('/customer/account/my-profile', methods=['GET', 'POST'])
def my_profile():
	cuser = User.get(current_user.id)
	form = Update_profile()

	if form.validate_on_submit():
		id = cuser.id
		email = form.email.data 
		firstname = form.firstname.data
		lastname = form.lastname.data
		nickname = form.nickname.data
		address = form.address.data

		User.Update(id, email, firstname, lastname, address, nickname, address)
		cuser = User.get(current_user.id)

		flash('Your profile is updated!')

		return render_template('customer_my_profile.html', form=form, cuser=cuser)
	return render_template('customer_my_profile.html', form=form, cuser=cuser)


@bp.route('/customer/account/my-orders', methods=['GET', 'POST'])
def my_orders():
	orders_summary = Orders.get_order_summary(current_user.id)

	form = Search_order()
	if form.validate_on_submit():
		return redirect(url_for('customer.display_history', search=form.search.data, cuser=cuser, orders=orders,form=form ))
	
	return render_template('customer_my_orders.html', orders_summary=orders_summary, form=form)


@bp.route('/customer/account/my-orders/result_page', methods=['GET', 'POST'])
def display_history():

	cuser = User.get(current_user.id)
	buyer_id = cuser.id
	form = Search_order() 
	search = request.args['search']
	matched_order = Search.search_order(search, buyer_id)
	no_match = matched_order is None

	return render_template('customer_my_orders_search.html',
							results=matched_order, no_match=no_match, search=search, form=form)


@bp.route('/customer/account/my-orders/order_details/<order_id>', methods=['GET', 'POST'])
def display_order_detail(order_id):
	order = Orders.get_order_detail(order_id)

	return render_template('customer_my_orders_display.html', order_id=order_id, order=order)


##### Harsha's Part
@bp.route('/customer/account/my-messages')
def my_messages():
	msg = "Hello world!"
	return render_template('customer_my_messages.html', info = msg)


@bp.route('/customer/account/my-reviews')
def my_reviews():
	all_reviews = Product_Review.get_all_reviews(current_user.id)
	all_seller_reviews = Seller_Review.get_all_reviews(current_user.id)
	return render_template('customer_my_reviews.html', info = current_user.id, all_reviews = all_reviews, all_seller_reviews=all_seller_reviews)



