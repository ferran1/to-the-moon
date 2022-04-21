from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Purchase, CryptoCurrentInfo, User
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    # Calculate & save the profit/loss for the logged in user
    cryptoInfoRows = CryptoCurrentInfo.query.all()

    totalUserProfitOrLoss = 0

    for cryptoInfo in cryptoInfoRows:
        for userPurchase in current_user.purchases:
            if cryptoInfo.coin_type == userPurchase.coin_type:
                priceChange = cryptoInfo.current_price - userPurchase.price_when_purchased
                priceChangePercentage = (
                    priceChange / userPurchase.price_when_purchased) * 100

                profit = (userPurchase.paid / 100) * priceChangePercentage

                totalUserProfitOrLoss = totalUserProfitOrLoss + profit

    converted_total_profit_float = float(totalUserProfitOrLoss)
    converted_total_profit = round(converted_total_profit_float, 2)

    logged_in_user = User.query.get(current_user.id)

    logged_in_user.profit = converted_total_profit
    db.session.commit()

    return render_template("home.html", user=current_user)


@views.route('/purchase', methods=['GET', 'POST'])
@login_required
def purchase():
    if request.method == 'POST':

        cointype = request.form.get('cointype')
        paid = request.form.get('paid')

        count = CryptoCurrentInfo.query.filter_by(
            coin_type=cointype).count()
        if count > 0:
            current_crypto_price = CryptoCurrentInfo.query.filter_by(
                coin_type=cointype).first().current_price

            if not paid:
                flash(
                    'The \'Paid\' field can\'t be empty. Please fill in the amount of the purchase', category='error')
            else:
                new_purchase = Purchase(
                    coin_type=cointype, paid=paid, price_when_purchased=current_crypto_price, user_id=current_user.id)

                db.session.add(new_purchase)
                db.session.commit()
                flash('Your crypto purchase has successfully been saved!',
                      category='success')
        else:
            flash(
                'No crypto data is currently available. Please make sure the embedded device is working correctly..', category='error')

    return render_template("purchase.html", user=current_user)


@views.route('/delete-purchase', methods=['POST'])
def delete_purchase():
    purchase = json.loads(request.data)
    purchaseId = purchase['purchaseId']
    purchase = Purchase.query.get(purchaseId)
    if purchase:
        if purchase.user_id == current_user.id:
            print("Purchase with ID: ", purchaseId, " Has been deleted")
            db.session.delete(purchase)
            db.session.commit()

    return redirect(url_for('purchase'))
