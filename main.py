import random
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

accounts = {'506-932': {'name': 'User1', 'cnic': '423011234567891', 'balance': 25000, 'pin': '1111'}, 
            '131-323': {'name': 'User2', 'cnic': '423019876543212', 'balance': 25000, 'pin': '1234'}, 
            '305-900': {'name': 'User3', 'cnic': '423011928374653', 'balance': 25000, 'pin': '1122'}, 
            '633-374': {'name': 'User4', 'cnic': '423012468135794', 'balance': 25000, 'pin': '2222'}}
de_acc = {}
transaction = {}
loans = {}
current_acc = []

def random_no():
    ran1 = random.randint(100,999)
    ran2 = random.randint(101,998)
    merge_ran = str(ran1) + "-" + str(ran2)
    return merge_ran

def acc_check(account_no) :
    if account_no not in accounts.keys() :
        print('Invalid Account Number')
        return True
    else:
        return False

def diff_cnic(cnic, account_no):
    if cnic == accounts[account_no]['cnic']:
        return False
    else :
        print('CNIC Number is not correct')
        return True

def check_cnic(cnic):
    for i in accounts.keys() :
        if cnic == accounts[i]['cnic']:
            print('This CNIC is already associated with another account')
            choice = input("Do you want to create your second account (Yes/No): ").lower().strip()
            while True:
                if choice == "yes":
                    return False
                    break
                elif choice == "no":
                    return True
                    break
                else:
                    choice = input("Please Enter Proper (Yes/No): ").lower().strip()
    else:
        return False
    
def pin_check(account_no, pin):
    if pin != accounts[account_no]["pin"]:
        print("PIN Entered is not correct")
        return True
    else:
        return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        global current_acc
        if request.method == 'POST':
            print("Login Request Received")
            data = request.get_json()
            account_no = data.get('account_no', '').strip()
            pin = data.get('pin', '').strip()
            if not account_no or not pin:
                return "Account number and PIN are required", 400
            if acc_check(account_no):
                return "Invalid Account Number", 400
            if pin_check(account_no, pin):
                return "Invalid PIN", 400
            if len(current_acc) != 0:
                current_acc.clear()
            current_acc.append(account_no)
        return "Login Successful"
    except Exception as e:
        return "Invalid error Occured"
    
@app.route('/logout', methods=['GET'])
def logout():
    try:
        global current_acc
        if not current_acc:
            return "No account is currently logged in", 400
        print("Logout Request Received")
        current_acc.clear()
        return "Logout Successful"
    except Exception as e:
        return "Invalid Error Occurred"

@app.route('/check_balance', methods=['GET'])
def check_balance():
    try:
        account_no = current_acc[0]
        balance = accounts[account_no]["balance"]
        return jsonify({"balance": balance, "account_no": account_no})
    except Exception as e:
        return "Invalid Error Occurred"

@app.route('/deposit', methods=['POST'])
def deposit():
    try:
        global current_acc
        if not current_acc:
            return "No account is currently logged in", 400
        print("Deposit Request Received")
        account_no = current_acc[0]
        data = request.get_json()
        if not data or 'amount' not in data:
            return "Amount to deposit is required", 400
        amount = data['amount']
        if amount <= 0:
            return "Please enter a valid amount to deposit", 400
        pin = data.get('pin')
        while pin_check(account_no, pin):
            return "Invalid PIN", 400
        accounts[account_no]['balance'] += amount
        date = time.strftime("%A %b/%d/%y %I:%M %p", time.localtime())
        unique_id = random_no()
        transaction[unique_id] = {"Method":"Deposit", "Account No":account_no, "Amount":amount, "Time":date}
        return "Deposit Successful"
    except Exception as e:
        return "Invalid Error Occurred"

@app.route('/withdraw', methods=['POST'])
def withdraw() :
    try:
        global current_acc
        if not current_acc:
            return "No account is currently logged in", 400
        print("Withdraw Request Received")
        account_no = current_acc[0]
        data = request.get_json()
        if not data or 'amount' not in data:
            return "Amount to withdraw is required", 400
        amount = data['amount']
        if amount <= 0 or amount > accounts[account_no]['balance']:
            return "Please enter a valid amount to withdraw", 400
        pin = data.get('pin')
        while pin_check(account_no, pin):
            return "Invalid PIN", 400
        accounts[account_no]['balance'] -= amount
        date = time.strftime("%A %b/%d/%y %I:%M %p", time.localtime())
        unique_id = random_no()
        transaction[unique_id] = {"Method":"Withdraw", "Account No":account_no, "Amount":amount, "Time":date}
        return "Withdraw Successful"
    except Exception as e:
        return "Invalid Error Occurred"

@app.route('/transfer', methods=['POST'])
def transfer_money() :
    try:
        global current_acc
        if not current_acc:
            return "No account is currently logged in", 400
        print("Transfer Request Received")
        account_no = current_acc[0]
        data = request.get_json()
        if not data or 'second_acc' not in data or 'amount' not in data:
            return "Account number to transfer money and amount are required", 400
        second_acc = data['second_acc'].strip()
        if second_acc == account_no:
            return "You cannot transfer money to your own account", 400
        if acc_check(second_acc):
            return "Invalid Account Number to transfer money", 400
        amount = data['amount']
        if amount <= 0 or amount > accounts[account_no]['balance']:
            return "Please enter a valid amount to transfer", 400
        pin = data.get('pin')
        while pin_check(account_no, pin):
            return "Invalid PIN", 400
        accounts[account_no]['balance'] -= amount
        accounts[second_acc]['balance'] += amount
        date = time.strftime("%A %b/%d/%y %I:%M %p", time.localtime())
        transaction_id = random_no()
        transaction[transaction_id] = {"Method":"Transfer", "Transaction ID":transaction_id, "Sender Account No": account_no, "Reciever":second_acc, "Amount": amount, "Time": date}
        return "Transfer Successful"
    except Exception as e:
        return "Invalid Error Occurred"

#By account Number
@app.route('/transactions', methods=['GET'])
def transactions():
    try:
        global current_acc
        if not current_acc:
            return "No account is currently logged in", 400
        print("Transaction Request Received")
        account_no = current_acc[0]
        record = 0
        records = []
        for key,value in transaction.items():
            if value.get("Sender Account No") == account_no or value.get("Account No") == account_no:
                json_value = json.dumps(value)
                records.append(json_value)
                record += 1
        print(records)
        if records:
            return jsonify({"transactions": records, "total_transactions": record}), 200
        else:
            return jsonify({"transactions": json.dumps([]), "total_transactions": 0}), 200
    except Exception as e:
        return "Invalid Error Occurred"

@app.route('/loan', methods=['POST', 'GET'])
def loan_system():
    try:
        global current_acc
        if not current_acc:
            return "No account is currently logged in", 400
        print("Loan Request Received")
        if request.method == 'POST':
            data = request.get_json()
            if not data or 'amount' not in data:
                return "Amount to take loan is required", 400
            amount = data['amount']
            if amount <= 0 or amount > 100000:
                return "Please enter a valid amount to take loan", 400
            account_no = current_acc[0]
            pin = data.get('pin')
            while pin_check(account_no, pin):
                return "Invalid PIN", 400
            accounts[account_no]['balance'] += amount
            for key, value in loans.items():
                if value.get("Account No") == account_no:
                    return jsonify({"message": "Loan already exists for this account"}), 400
            date = time.strftime("%A %b/%d/%y %I:%M %p", time.localtime())
            unique_id = random_no()
            loans[unique_id] = {"Type":"Loan", "Account No":account_no, "Amount":amount, "Time":date}
            return jsonify({"message": "Loan Granted Successfully", "loan_id": unique_id}), 200
        elif request.method == 'GET':
            account_no = current_acc[0]
            loan_records = []
            for key, value in loans.items():
                if value.get("Account No") == account_no:
                    json_value = json.dumps(value)
                    loan_records.append(json_value)
            if loan_records:
                return jsonify({"loans": loan_records}), 200
            else:
                return jsonify({"loans": json.dumps([])}), 200
    except Exception as e:
        return "Invalid Error Occurred", 500
    
@app.route('/pay_loan', methods=['POST'])
def pay_loan():
    try:
        global current_acc
        if not current_acc:
            return "No account is currently logged in", 400
        print("Pay Loan Request Received")
        account_no = current_acc[0]
        data = request.get_json()
        if not data or 'amount' not in data:
            return "Amount to pay loan is required", 400
        amount = data['amount']
        if amount <= 0 or amount > accounts[account_no]['balance']:
            return "Please enter a valid amount to pay loan", 400
        pin = data.get('pin')
        while pin_check(account_no, pin):
            return "Invalid PIN", 400
        for key, value in loans.items():
            if value.get("Account No") == account_no:
                if amount > value.get("Amount"):
                    return jsonify({"message": "Amount exceeds the loan amount"}), 400
                elif amount < value.get("Amount"):
                    accounts[account_no]['balance'] -= amount
                    loans[key]['Amount'] -= amount
                    transaction_id = random_no()
                    date = time.strftime("%A %b/%d/%y %I:%M %p", time.localtime())
                    unique_id = random_no()
                    loans[unique_id] = {"Type":"Loan", "Account No":account_no, "Amount":loans[key]['Amount'], "Time":date}
                    transaction[transaction_id] = {"Method":"Pay Loan", "Transaction ID":transaction_id, "Account No": account_no, "Amount": amount, "Time": date}
                    return jsonify({"message": "Loan Payment Successful"}), 200
                elif amount == value.get("Amount"):
                    accounts[account_no]['balance'] -= amount
                    del loans[key]
                    date = time.strftime("%A %b/%d/%y %I:%M %p", time.localtime())
                    transaction_id = random_no()
                    transaction[transaction_id] = {"Method":"Fully Paid Loan", "Transaction ID":transaction_id, "Account No": account_no, "Amount": amount, "Time": date}
                    return jsonify({"message": "Loan Paid Successfully"}), 200
        return jsonify({"message": "No active loan found for this account"}), 400
    except Exception as e:
        return "Invalid Error Occurred", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)