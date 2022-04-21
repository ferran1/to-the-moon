from flask_restful import Resource
from flask import request, request
from .models import CryptoCurrentInfo, User
from flask_httpauth import HTTPBasicAuth  
from werkzeug.security import check_password_hash 
from . import db

auth = HTTPBasicAuth()

# API endpoint to retreive the current crypto information from the embedded device
class Crypto(Resource):
    def put(self):
        crypto_json_data = request.get_json(force=True)

        # Loop through the JSON array from the request, retreive and save the current prices (info) of the 3 cryptocurrencies (BTC, ETH, ADA)
        for i in range(len(crypto_json_data['data'])):
            coin_type = crypto_json_data['data'][i]['currency']
            current_price = crypto_json_data['data'][i]['price']
            converted_current_price_float = float(current_price)
            converted_current_price = round(converted_current_price_float, 2)

            current_date_bitcoin = crypto_json_data['data'][i]['price_date']
            new_crypto_current_info = CryptoCurrentInfo(
                coin_type=coin_type, current_price=converted_current_price, date=current_date_bitcoin)

            # If already exists in the db, update the current price (CryptoCurrentInfo)
            count = CryptoCurrentInfo.query.filter_by(
                coin_type=coin_type).count()
            if count > 0:
                crypto_info = CryptoCurrentInfo.query.filter_by(
                    coin_type=coin_type).first()
                crypto_info.current_price = converted_current_price
                print("Current price after converted: ",
                      crypto_info.current_price)
                crypto_info.date = current_date_bitcoin
                db.session.commit()
            else:
                db.session.add(new_crypto_current_info)
                db.session.commit()

        return crypto_json_data

@auth.verify_password
def verify(email, password):

    count = User.query.filter_by(
        email=email).count()
    if count == 0:
        return False

    user = User.query.filter_by(
    email=email).first()
    if check_password_hash(user.password, password):
        return email
    else:
        return False


# API endpoint that returns the profit of a user (For the embedded device)
class UserProfit(Resource):

    @auth.login_required
    def get(self):
        user = User.query.filter_by(
        email=auth.current_user()).first()
        return user.profit

