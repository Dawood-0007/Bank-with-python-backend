import random

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

def account():
    try:
        name = input("Enter your name : ").title()
        while True:
            for char in name:
                if not (char.isalpha() or char.isspace()):
                    name = input("Enter a correct name(Only contains alphabets and space)").title()
                    break
            else:
                break
        cnic = input('Enter Your CNIC Number(CNIC can only contain numeric character without symbols): ').strip()
        while True:
            if cnic.isdigit():
                break
            else:
                cnic = input('Enter Your CNIC Number(CNIC can only contain numeric character without symbols): ').strip()
        while check_cnic(cnic) :
            cnic = input('Enter a correct CNIC Number: ').strip()
        pin = input("Enter a unique 4 Digit PIN number fo your account\nPIN Number will be needed for multiple operations: ")
        while True:
            if pin.isdigit() and len(pin) == 4:
                print("Remember your pin")
                break
            else:
                pin = input("PIN can only contains four(4) numeric values i.e. 0 - 9: ")
        account_no = random_no()
        accounts[account_no] = {'name':name, 'cnic': cnic, 'balance':0, 'pin':pin}
        print('Your Account number Is:', account_no)
        print("Your Initial Balance is 0")
        if current_acc != 0:
            current_acc.clear()
        current_acc.append(account_no)
    except Exception as e:
        print(e)

def account_deletion():
    try:
        account_no = current_acc[0]
        pin = input("Enter your 4-digit pin number: ")
        while pin_check(account_no, pin):
            pin = input("Enter Your Correct 4-digit PIN Number: ")
        cnic = input('Enter CNIC Number: ').strip()
        while diff_cnic(cnic, account_no) :
            cnic = input('Enter A Correct CNIC Number: ').strip()
        if accounts[account_no]['balance'] != 0 :
            print('Balance Should Be Zero to delete an account')
            while accounts[account_no]['balance'] != 0 :
                print('Your current Balance is:', accounts[account_no]['balance'])
                print('You have to transfer or withdraw all your money to proceed')
                choice = input('Enter Withdraw or Transfer').lower().strip()
                while True:
                    if choice == 'withdraw' :
                        # withdraw_balance(account_no)
                        break
                    elif choice == 'transfer':
                        # transaction_intermediate(account_no)
                        break
                    else:
                        choice = input("Please enter proper withdraw or transfer").lower().strip()
        del accounts[account_no]
        print('Your Account has Been Deleted Successfully')
    except Exception as e:
        print(e)

def deactivation() :
    try:
        account_no = current_acc[0]
        pin = input("Enter your 4-digit pin number: ")
        while pin_check(account_no, pin):
            pin = input("Enter Your Correct 4-digit PIN Number: ")
        cnic = input('Enter CNIC Number: ').strip()
        while diff_cnic(cnic, account_no) :
            cnic = input('Enter A Correct CNIC Number: ').strip()
        if accounts[account_no]['balance'] != 0 :
            print('Balnce Should Be Zero to deactivate an account')
            while accounts[account_no]['balance'] != 0 :
                print('Your current Balance is:', accounts[account_no]['balance'])
                print('You has to transfer or withdraw all your money to proceed')
                choice = input('Enter Withdraw or Transfer').lower().strip()
                while True:
                    if choice == 'withdraw' :
                        # withdraw_balance(account_no)
                        break
                    elif choice == 'transfer':
                        # transaction_intermediate(account_no)
                        break
                    else:
                        choice = input("Please Enter proper withdraw or transfer: ")
        name = accounts[account_no]['name']
        de_acc[account_no] = {'name':name, 'cnic': cnic, 'balance':0, 'pin':pin}
        print('Your Account has been Deactivated')
        del accounts[account_no]
    except Exception as e:
        print(e)

def reactivation():
    try:
        account_no = input('Enter Your Account Number To Reactivate your account: ').strip()
        while account_no not in de_acc.keys():
            print('Invalid Account Number')
            account_no = input('Enter Your Account Number To Reactivate your account: ').strip()
        pin = input("Enter your 4-digit pin number: ")
        while pin != de_acc[account_no]["pin"]:
            print("You entered Wrong PIN Number: ")
            pin = input("Enter Your Correct 4-digit PIN Number: ")
        cnic = input('Enter CNIC Number: ').strip()
        while cnic != de_acc[account_no]["cnic"]:
            print("You entered Wrong CNIC Number")
            cnic = input("Enter a correct CNIC Number: ").strip()
        name = de_acc[account_no]['name']
        accounts[account_no] = {'name':name, 'cnic': cnic, 'balance':0, 'pin':pin}
        del de_acc[account_no]
        print('Your Account has been Reactivated')
        print("Your balance after reactivation is 0")
    except Exception as e:
        print(e)

#By Transaction ID
def transaction_id_tracker():
    try:
        id = input("Enter your transaction ID (e.g, 111-111)").strip()
        breaker = 0
        while breaker == 0:
            for key in transaction.keys(): 
                if key == id:
                    breaker += 1
                    break
            else:
                id = input("Enter your Correct transaction ID (e.g, 111-111)").strip()
        account_no = current_acc[0]
        pin = input("Enter your 4-digit pin number: ")
        while pin_check(account_no, pin):
            pin = input("Enter Your Correct 4-digit PIN Number: ")
        for key,value in transaction.items():
            if key == id:
                print(value)
    except Exception as e:
        print(e)

def export_transaction():
    try:
        account_no = current_acc[0]
        pin = input("Enter your 4-digit pin number: ")
        while pin_check(account_no, pin):
            pin = input("Enter Your Correct 4-digit PIN Number: ")
        export_transaction_process(account_no)
    except Exception as e:
        print(e)
 
def export_transaction_process(account_no):
    record = 0
    record1 = 0
    transactions_list = []
    for key, value in transaction.items():
        if value.get("Sender Account No") == account_no or value.get("Account No") == account_no:
            transactions_list.append(value)
            if value.get("Sender Account No") == account_no:
                record += 1
            else:
                record1 += 1
    if transactions_list == []:
        print("No transactions or deposit and withdrawal is performed in this account")
    else:
        outfile = open("Transactions.txt", "w")
        for entry in transactions_list:
            outfile.write(f"{entry}\n")
        outfile.write(f"Your total transactions are: {record}\n")
        outfile.write(f"Your total deposit and withdrawal are: {record1}\n")
        print("Exported Successfully")