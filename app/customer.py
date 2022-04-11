from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import current_app as app

from flask import Blueprint
bp = Blueprint('customer', __name__)

from .models.user import User
from .models.balance import Balance

class Update_profile(FlaskForm):
    firstname = StringField('firstname')
    email = StringField('email', validators=[Email()])
    submit = SubmitField('Update')

@bp.route('/customer')
def customer():
	if current_user.is_authenticated:
		recommended_products = ['abc']
		return render_template('customer.html', rec_prod = recommended_products)
	else:
		return redirect(url_for('index.index'))

@bp.route('/customer/public_profile')
def public_profile():
	cuser = User.get(current_user.id)

	return render_template('customer_public_profile.html', cuser = cuser)

@bp.route('/customer/account')
def customer_portal():
	if current_user.is_authenticated:
		return render_template('customer_portal.html')
	else:
		return redirect(url_for('index.index'))


@bp.route('/customer/account/my-cart')
def my_cart():
	msg = "Hello world!"
	return render_template('customer_my_cart.html', info = msg)


@bp.route('/customer/account/my-orders')
def my_orders():
	msg = "Hello world!"
	return render_template('customer_my_orders.html', info = msg)


@bp.route('/customer/account/my-profile', methods=['GET', 'POST'])
def my_profile():
	cuser = User.get(current_user.id)

	form = Update_profile()

	if request.method == "POST":
		if  form.validate_on_submit():
			id = cuser.id
			firstname_new = request.form.get('firstname')
			email = form.email.data
			
			app.db.execute("""
			UPDATE Users
			SET email = email, firstname = firstname
			WHERE id = id
			""", 
						   email = email, 
						   firstname=firstname_new)

			return render_template('customer_my_profile.html', title='Manage your profile', form=form, cuser=cuser)

	else:
		id = cuser.id
		rows = app.db.execute("""
		SELECT *
		FROM Users
		WHERE id = id
		""")

		for row in rows:
			form.email.data = row[1]
			form.firstname.data = row[2]
			return render_template('customer_my_profile.html', title='Manage your profile', form=form, cuser=cuser)
	
@bp.route('/customer/account/my-messages')
def my_messages():
	msg = "Hello world!"
	return render_template('customer_my_messages.html', info = msg)

@bp.route('/customer/account/my-balance')
def my_balance():
	balance_info = Balance.get(current_user.id)

	return render_template('customer_my_balance.html', balance_info = balance_info)

@bp.route('/customer/account/my-balance/withdraw')
def my_balance_withdraw():
	balance_info = Balance.get(current_user.id)
	user_balance = balance_info.balance
	return render_template('customer_my_balance_withdraw.html', user_balance = user_balance)

@bp.route('/customer/account/my-balance/topup', methods=('GET', 'POST'))
def my_balance_topup():

	if request.method == "POST":
		trans = request.form['trans']
		rows = app.db.execute("""
		INSERT INTO Balance(trans_id, trans_date,id , trans, balance)
		VALUES(:trans_id, :trans_date, :id, :trans, :balance)
		RETURNING id
		""",
                              trans_id='7',
							  trans_date = '2019-02-23 20:02:21.550',
							  id = current_user.id, 
							  trans=trans, 
							  balance = '100')

#		row = Balance(	trans_id='5',
#						trans_date = '2019-02-23 20:02:21.550',
#						id = '1', 
#						trans=trans, 
#						balance = '100')
#		app.db.session.add(row)
#		app.db.session.commit()
		return redirect(url_for('customer.my_balance_topup'))

	balance_info = Balance.get(current_user.id)
	
	return render_template('customer_my_balance_topup.html', balance_info = balance_info)

			
#			rows = app.db.execute("""
#INSERT INTO Balance(trans_id, trans_date, id, trans, balance)
#VALUES(:trans_id, :trans_date, :id, :trans, :balance)
#RETURNING id
#""",
                                  
#								  trans=trans)
		
	

