from abc import ABC, abstractmethod


class BaseAccount(ABC):

    bank_name = "Vietcombank"

    def __init__(self, account_number, owner, balance=0):
        self.__balance = balance
        self.account_number = account_number
        self.owner = owner

    @property
    def balance(self):
        return self.__balance

    def _change_balance(self, amount):
        self.__balance += amount

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    def __add__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented
        return self.balance + other.balance

    def __lt__(self, other):
        if not isinstance(other, BaseAccount):
            return NotImplemented
        return self.balance < other.balance


    @staticmethod
    def validate_account_number(account_number):
        return account_number.isdigit() and len(account_number) == 10


    @classmethod
    def update_bank_name(cls, new_name):
        cls.bank_name = new_name



class SavingsAccount(BaseAccount):

    def __init__(self, account_number, owner, interest_rate):
        super().__init__(account_number, owner)
        self.interest_rate = interest_rate


    def deposit(self, amount):
        self._change_balance(amount)


    def withdraw(self, amount):
        fee = amount * 0.02
        total = amount + fee

        if total <= self.balance:
            self._change_balance(-total)
            return True

        return False


    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self._change_balance(interest)



class CreditAccount(BaseAccount):

    def __init__(self, account_number, owner, credit_limit):
        super().__init__(account_number, owner)
        self.credit_limit = credit_limit


    def withdraw(self, amount):

        if self.balance - amount >= -self.credit_limit:
            self._change_balance(-amount)
            return True

        raise Exception(
            "Vượt quá hạn mức thấu chi cho phép"
        )


    def deposit(self, amount):
        self._change_balance(amount)



class DigitalPremiumMixin:


    def cashback_reward(self, amount):

        if amount > 5000000:
            return amount * 0.01

        return 0



class HybridAccount(
    SavingsAccount,
    DigitalPremiumMixin
):

    pass



class VNPayGateway:


    def execute_pay(self, account, amount):

        if account.balance >= amount:
            account.withdraw(amount)
            return True

        return False



class ViettelMoneyGateway:


    def execute_pay(self, account, amount):

        if account.balance >= amount:
            account.withdraw(amount)
            return True

        return False



def process_payment(payment_gateway, account, amount):

    try:
        payment_gateway.execute_pay(
            account,
            amount
        )

    except AttributeError:

        print(
            "Cổng thanh toán không hợp lệ hoặc chưa được tích hợp"
        )



accounts = []
current_account = None


def menu():

    global current_account

    while True:

        print("""
1. Create account
2. Show account
3. Deposit / Withdraw
4. Apply interest
5. Compare account
6. Payment
7. Exit
        """)


        choice = input(
            "Choose: "
        )


        if choice == "1":

            account_type = input(
                "1.Savings 2.Credit 3.Hybrid: "
            )


            number = input(
                "Account number: "
            )


            if not BaseAccount.validate_account_number(number):
                print(
                    "Số tài khoản không hợp lệ"
                )
                continue


            name = input(
                "Owner: "
            ).strip().upper()


            if account_type == "1":

                rate = float(
                    input("Interest: ")
                )

                current_account = SavingsAccount(
                    number,
                    name,
                    rate
                )


            elif account_type == "2":

                current_account = CreditAccount(
                    number,
                    name,
                    20000000
                )


            else:

                current_account = HybridAccount(
                    number,
                    name,
                    0.06
                )


            accounts.append(current_account)


        elif choice == "2":

            if current_account:

                print(
                    current_account.__class__.__name__
                )

                print(
                    current_account.balance
                )

                print(
                    HybridAccount.mro()
                )


        elif choice == "3":

            amount = float(
                input("Amount: ")
            )

            action = input(
                "1.Deposit 2.Withdraw: "
            )


            if action == "1":
                current_account.deposit(amount)

            else:
                current_account.withdraw(amount)


        elif choice == "4":

            if hasattr(
                current_account,
                "apply_interest"
            ):
                current_account.apply_interest()


        elif choice == "5":

            other = accounts[0]

            print(
                current_account + other
            )

            print(
                current_account < other
            )


        elif choice == "6":

            gateway = VNPayGateway()

            process_payment(
                gateway,
                current_account,
                500000
            )


        elif choice == "7":
            break



menu()