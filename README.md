# Bank_account_system
This is a python project that simulate simple bank account system. It provides the functionalities for creating account with unique account number, depositing and, withdrawing money, checking account balances and viewing transaction history
Features:  
 Account Creation
•	This bank account system allows user to create an account using Account name, Account number and Email id(optional). Account number must be alphanumeric characters and it should be between 6 and 10 characters. Account number is case sensitive
•	The system validates the input and check whether it is unique account number
•	New user information validating using dictionary, account number as a key, after validation account information write in to csv file and user receives the confirmation of successful creation
Login
•	Once user creates the account, user can login using registered username and account number, it would take the user to their account dash board.
•	The program reads the csv file in to dictionary, where account number as a key and account details as a value. This allows the validation of login credential
•	Up on successful login users are redirect in to account dashboard
Account Dashboard
•	In the Account dashboard account holder can see their current account balance, and perform all transactions like deposit and withdrawal. Account holder is able to see their transaction history during each login and have an option to view transaction graph where account holder can visualize their balance after each transaction.
Deposit
•	User can enter the amount to deposit, system validate the input, it allows maximum 6-digit numbers (999,999) and allows only valid numbers
•	After successful deposit, system will update the current balance and transaction history
Withdraw
•	Users enter the amount to withdraw, system will check whether account have enough balance to withdraw specified funds
•	If the balance is sufficient, system will update current balance and transaction history, otherwise system will throw the error message
Transaction History
•	Users can view all the transactions they performed after logged in, including withdraw and deposit
View transaction Graph
•	User can visualize their transaction and see the balance after each transaction
  Log out
•	Ends the session and redirects the user to the login screen.
Requirements
•	Python 3.x
•	Tkinter (built-in with Python)
•	Matplotlib (install via pip install matplotlib)
•	PIL \Pilow Library

How to Run the Application
Install Dependencies:
Make sure you have Matplotlib and Pilow installed
Run the Code Click on Run button

 

 
