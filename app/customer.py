from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList, IntegerField, PasswordField, BooleanField, SelectField

from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from datetime import date
from werkzeug.urls import url_parse

from .models.cart import Cart
from .models.recommend import Recommend
from .models.user import User
from .models.order import Orders, Search

from flask import Blueprint
bp = Blueprint('customer', __name__)



##### Lin's Part

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



### Mae's Part

class Update_profile(FlaskForm):
	address = StringField('address', validators=[DataRequired()])
	firstname = StringField('firstname', validators=[DataRequired()])
	lastname = StringField('lastname', validators=[DataRequired()])
	email = StringField('email', validators=[Email(), DataRequired()])
	submit = SubmitField('Update', validators=[DataRequired()])

class Search_order(FlaskForm):
	search = StringField('Search', validators=[DataRequired()])
	submit = SubmitField('Search')

class balance_topup(FlaskForm):
	amount = StringField('amount', validators=[DataRequired()])
	submit = SubmitField('Top up')

class balance_withdraw(FlaskForm):
	amount = StringField('amount', validators=[DataRequired()])
	submit = SubmitField('Withdraw')
	

@bp.route('/customer/public_profile')
def public_profile():
	cuser = User.get(current_user.id)

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
		address = form.address.data

		User.Update(id, email, firstname, lastname, address)
		cuser = User.get(current_user.id)

		flash('Your profile is updated!')

		return render_template('customer_my_profile.html', form=form, cuser=cuser)
	return render_template('customer_my_profile.html', form=form, cuser=cuser)


@bp.route('/customer/account/my-balance')
def my_balance():
	balance_info = Balance.get(current_user.id)
	balance_info_all = Balance.get_all(current_user.id)

	return render_template('customer_my_balance.html', balance_info = balance_info, balance_info_all=balance_info_all)


@bp.route('/customer/account/my-balance/withdraw', methods=('GET', 'POST'))
def my_balance_withdraw():
	balance_info_all = Balance.get_lastrow()
	balance_info = Balance.get(current_user.id)

	form = balance_withdraw()
	if form.validate_on_submit():
		trans_id = balance_info_all.trans_id + 1
		trans_date = date.today()
		user_id = current_user.id
		trans = form.amount.data
		trans_description = 'Withdraw from bank account'
		balance = float(balance_info.balance) - float(trans)
		if balance < 0:
			flash('Withdrawal fail! (You can withdraw up to the available balance)')
			return redirect(url_for('customer.my_balance_withdraw'))

		else:
			Update_balance.insert(trans_id, trans_date, user_id, trans, trans_description, balance)
			balance_info = Balance.get(current_user.id)
			
			flash('Withdrawal successful!')
			return render_template('customer_my_balance_withdraw.html', balance_info = balance_info, form=form)

	return render_template('customer_my_balance_withdraw.html', balance_info = balance_info, form=form)


@bp.route('/customer/account/my-balance/topup', methods=('GET', 'POST'))
def my_balance_topup():
	balance_info_all = Balance.get_lastrow()
	balance_info = Balance.get(current_user.id)

	form = balance_topup()
	if form.validate_on_submit():
		trans_id = balance_info_all.trans_id + 1
		trans_date = date.today()
		user_id = current_user.id
		trans = form.amount.data
		balance = float(balance_info.balance) + float(trans)
		trans_description ='Deposit from bank account'
		
		Update_balance.insert(trans_id, trans_date, user_id, trans, trans_description, balance)
		balance_info = Balance.get(current_user.id)

		flash('Topup successful!')

		return render_template('customer_my_balance_topup.html', balance_info = balance_info, form=form)

	return render_template('customer_my_balance_topup.html', balance_info = balance_info, form=form)


@bp.route('/customer/account/my-orders', methods=['GET', 'POST'])
def my_orders():
	cuser = User.get(current_user.id)
	orders = Orders.get(current_user.id)

	form = Search_order()
	if form.validate_on_submit():
		return redirect(url_for('customer.display_history', search=form.search.data, cuser=cuser, orders=orders,form=form ))
	
	return render_template('customer_my_orders.html',cuser=cuser, orders=orders, form=form)

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

@bp.route('/customer/account/my-orders/order_details', methods=['GET', 'POST'])
def display_orderID(order_id=None):
	if order_id is None:
		order_id = request.form['order_id']

	return render_template('customer_my_orders_display.html', order_id=order_id)


##### Harsha's Part
@bp.route('/customer/account/my-messages')
def my_messages():
	msg = "Hello world!"
	return render_template('customer_my_messages.html', info = msg)

