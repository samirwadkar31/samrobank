from flask import Flask,request,render_template,flash,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
import pytz


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#31L"F4Q8z\n\xec]/!'
db = SQLAlchemy(app)

IST = pytz.timezone('Asia/Kolkata')

class Customers(db.Model):
    customer_account_no = db.Column(db.Integer,primary_key = True)
    customer_name = db.Column(db.String(200),nullable = False)
    email = db.Column(db.String(120), nullable = False)
    account_type = db.Column(db.String(120), default = 'Saving')
    current_bal = db.Column(db.Integer, default = 3000)

    def __repr__(self):
        return f"{self.customer_name}"


class Transaction(db.Model):
    trans_id = db.Column(db.Integer,primary_key = True)
    sender_name = db.Column(db.String(200),nullable = False)
    sender_account_no = db.Column(db.Integer,nullable = False)
    receiver_name = db.Column(db.String(200),nullable = False)
    receiver_account_no = db.Column(db.Integer,nullable = False)
    amount_transfered = db.Column(db.Integer, nullable = False)
    date_transfer = db.Column(db.DateTime,default = datetime.now(IST))

    # def __repr__(self):
    #     return f"{self.receiver_name}"

@app.route('/')
def home():
    # c1 = Customers(customer_name = 'Samir Wadkar',email = 'samir@gmail.com')
    # c2 = Customers(customer_name = 'Muskan Gupta',email = 'muskan@gmail.com')
    # c3 = Customers(customer_name = 'roshni wadkar',email = 'roshni@gmail.com')
    # c4 = Customers(customer_name = 'hemant mishra',email = 'hemant@gmail.com')
    # c5 = Customers(customer_name = 'ranjit patil',email = 'ranjit@gmail.com')
    # c6 = Customers(customer_name = 'givinder singh',email = 'givinder@gmail.com')
    # c7 = Customers(customer_name = 'judewin noronha',email = 'judewin@gmail.com')
    # c8 = Customers(customer_name = 'ashish jaiswal',email = 'ashish@gmail.com')
    # c9 = Customers(customer_name = 'kashish dungar',email = 'kashish@gmail.com')
    # c10 = Customers(customer_name = 'Saloni takhtani',email = 'saloni@gmail.com')

    # db.session.add(c1)
    # db.session.add(c2)
    # db.session.add(c3)
    # db.session.add(c4)
    # db.session.add(c5)
    # db.session.add(c6)
    # db.session.add(c7)
    # db.session.add(c8)
    # db.session.add(c9)
    # db.session.add(c10)
    # db.session.commit()

    return render_template('home.html')

@app.route('/customer_view',methods = ['GET'])
def customer_view():
    if request.method == 'GET':
        all_customer = Customers.query.all()
        return render_template('customer.html',all_customer = all_customer)

@app.route('/transfer_money',methods = ['GET','POST'])
def transfer_money():
    if request.method == 'POST':
        sender_name = request.form['sender_name']
        sender_account_no = request.form['sender_account_no']
        receiver_name = request.form['receiver_name']
        receiver_account_no = request.form['receiver_account_no']
        amount = int(request.form['amount'])

        check_sender_account_no = Customers.query.filter_by(customer_account_no = sender_account_no).first()
        if check_sender_account_no != None:
            check_receiver_account_no = Customers.query.filter_by(customer_account_no = receiver_account_no).first()
            if check_receiver_account_no != None:
                if check_sender_account_no.current_bal >= amount:
                    check_sender_account_no.current_bal = check_sender_account_no.current_bal - amount
                    check_receiver_account_no.current_bal = check_receiver_account_no.current_bal + amount
                    db.session.add(check_receiver_account_no)
                    db.session.add(check_sender_account_no)
                    transaction = Transaction(
                        sender_name = sender_name,
                        sender_account_no = sender_account_no,
                        receiver_name = receiver_name,
                        receiver_account_no = receiver_account_no,
                        amount_transfered = amount)
                    db.session.add(transaction)
                    db.session.commit()
                    message = "Amount transfered succesfully!!"
                    flash(message)
                    return redirect(url_for('customer_view')) 
                else:
                    message = "Not enough money in our bank account"
                    flash(message)
                    return render_template('transfer_money.html')
            else:
                message = "This account doesn't exist!"
                flash(message)
                return render_template('transfer_money.html')
        else:
            message = "This account doesn't exist!"
            flash(message)
            return render_template('transfer_money.html')
    else:
        return render_template('transfer_money.html')

@app.route('/bank_statement/<int:customer_account_no>')
def bank_statement(customer_account_no):
    customer = Customers.query.filter_by(customer_account_no = customer_account_no).first()
    # bank_statement = Transaction.query.filter_by(sender_account_no = customer_account_no).all() + Transaction.query.filter_by(receiver_account_no = customer_account_no).all()
    bank_statement = Transaction.query.filter(or_(Transaction.sender_account_no.like(customer_account_no),Transaction.receiver_account_no.like(customer_account_no))).all()
    print(bank_statement)
    return render_template('bank_statement.html',bank_statement = bank_statement,customer_account_no = customer_account_no,customer = customer)


if __name__ == "__main__":
    app.run(debug=True)
