from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from datetime import date
from .models.balance import Balance, Update_balance

from flask import Blueprint
bp = Blueprint('balance', __name__)


class balance_topup(FlaskForm):
	amount = StringField('amount', validators=[DataRequired()])
	submit = SubmitField('Top up')

class balance_withdraw(FlaskForm):
	amount = StringField('amount', validators=[DataRequired()])
	submit = SubmitField('Withdraw')
	

@bp.route('/my-balance')
def my_balance():
	balance_info = Balance.get(current_user.id)
	balance_info_all = Balance.get_all(current_user.id)

	return render_template('customer_my_balance.html', balance_info=balance_info, balance_info_all=balance_info_all)


@bp.route('/my-balance/withdraw', methods=('GET', 'POST'))
def my_balance_withdraw():
	balance_info = Balance.get(current_user.id)

	form = balance_withdraw()
	if form.validate_on_submit():
		trans_date = date.today()
		user_id = current_user.id
		trans = form.amount.data
		trans_description = 'Withdraw from bank account'
		balance = float(balance_info.balance) - float(trans)
		if balance < 0:
			flash('Withdrawal fail! (You can withdraw up to the available balance)')
			return redirect(url_for('balance.my_balance_withdraw'))

		else:
			Update_balance.insert(trans_date, user_id, trans, trans_description, balance)
			balance_info = Balance.get(current_user.id)
			
			flash('Withdrawal successful!')
			return render_template('customer_my_balance_withdraw.html', balance_info = balance_info, form=form)

	return render_template('customer_my_balance_withdraw.html', balance_info = balance_info, form=form)


@bp.route('/my-balance/topup', methods=('GET', 'POST'))
def my_balance_topup():
	balance_info = Balance.get(current_user.id)

	form = balance_topup()
	if form.validate_on_submit():
		trans_date = date.today()
		user_id = current_user.id
		trans = form.amount.data
		balance = float(balance_info.balance) + float(trans)
		trans_description ='Deposit from bank account'
		
		Update_balance.insert(trans_date, user_id, trans, trans_description, balance)
		balance_info = Balance.get(current_user.id)

		flash('Topup successful!')

		return render_template('customer_my_balance_topup.html', balance_info = balance_info, form=form)

	return render_template('customer_my_balance_topup.html', balance_info = balance_info, form=form)
