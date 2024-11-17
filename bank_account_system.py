import tkinter as tk
import tkinter.messagebox
from tkinter import messagebox
from tkinter import StringVar
import csv
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Account:
    def __init__(self, account_name, account_number, account_balance=0, account_email_id=None):
        self.account_name = account_name
        self.account_number = account_number
        self.account_balance = float(account_balance)
        self.account_email_id = account_email_id
        self.transactionlist = []

    def deposit(self, amount):
        #if not amount.replace('.', '', 1).isdigit():
            #tkinter.messagebox.showerror("Amount must be a number.")
        amount=float(amount)
        if amount<=0:
            tkinter.messagebox.showerror(title="Error",message="Number should be positive")


        self.account_balance += amount
        #self.transactionlist.append("Deposit: $" + amount)
        self.transactionlist.append(f"Deposit: ${amount:.2f}")  # Convert float to string with 2 decimal place
        return self.account_balance

    def withdrawal(self, amount):
        amount=float(amount)
        if self.account_balance >= amount:
            self.account_balance -= amount
            self.transactionlist.append(f"Withdrawal: ${amount:.2f}")
            messagebox.showinfo(title="Success",message= f"${amount} withdrawn successfully!")
            return self.account_balance
        else:
            tkinter.messagebox.showerror(title="Error",message= "Insufficient funds")

    def get_balance(self):
        return self.account_balance

    def get_transaction_history(self):
        return self.transactionlist

class BankAction:
    def __init__(self, filename="account.csv"):
        self.filename = filename
        self.accounts = {}  # Dictionary to store account objects

    def read_accounts(self):
        try:
            with open(self.filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    if len(row) >= 4:  # Ensure the row has at least 4 elements
                        account_name, account_number, account_balance, account_email = row[:4]
                        account = Account(account_name, account_number, account_balance, account_email)
                        self.accounts[account_number] = account
                    else:
                        print(f"Skipping invalid row: {row}")
        except FileNotFoundError:
            pass

    def save_accounts(self):
        with open(self.filename, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for account in self.accounts.values():
                writer.writerow([account.account_name, account.account_number, account.account_balance, account.account_email_id])

    def create_account(self, account_name, account_number, initial_balance, account_email_id=None):
        if account_number in self.accounts:
            tkinter.messagebox.showerror("Error", "Account number already exists")
            return None
        if not account_number.isalnum():
            tkinter.messagebox.showerror(title="Error",message="Account number can only contain letters and numbers")
            return None
        account = Account(account_name, account_number, initial_balance, account_email_id)
        self.accounts[account_number] = account
        self.save_accounts()
        return account

    def login(self, account_name, account_number):
        account = self.accounts.get(account_number)
        if account and account.account_name == account_name:
            return account
        else:
            return None

class BankAccountGUI:
    def __init__(self):
        self.bank_system = BankAction()
        self.bank_system.read_accounts()
        self.current_account =None  # Stores the logged-in account object
        self.main_window = tk.Tk()
        self.main_window.title("RBS Account System")
        self.create_main_window()

    def create_main_window(self):
        self.main_window.geometry("600x400")

        # Create a frame to contain the widgets
        frame = tk.Frame(self.main_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Load the image and place it on the side
        image_path = "Bank.png"  # Adjust the path to your image
        side_image = Image.open(image_path)
        side_image = side_image.resize((400, 400), Image.Resampling.LANCZOS)
        side_photo = ImageTk.PhotoImage(side_image)

        # Label to hold the image
        image_label = tk.Label(frame, image=side_photo)
        image_label.image = side_photo  # Keep a reference to avoid garbage collection
        image_label.pack(side=tk.LEFT, padx=20, pady=20)

        # Create buttons and other widgets in the remaining space
        button_frame = tk.Frame(frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)



        login_btn = tk.Button(button_frame, text='Login', command=self.open_login_window, font=("Helvetica", 16),bg="dodger blue", fg="white")
        #login_btn.pack(pady=10)
        login_btn.place(relx=0.4, rely=0.4, anchor=tk.CENTER)

        create_account_btn = tk.Button(button_frame, text='Sign Up', command=self.open_create_account_window,
                                       font=("Helvetica", 16),bg="dodger blue", fg="white")
        create_account_btn.place(relx=0.4, rely=0.6, anchor=tk.CENTER)

        #create_account_btn.pack(pady=10)

        #self.main_window.mainloop()

    def open_create_account_window(self):
        create_window = tk.Toplevel(self.main_window)
        create_window.title("Create Account")
        frame = tk.Frame(create_window)
        frame.pack()

        userinfoframe = tk.LabelFrame(frame, text="Create Account")
        userinfoframe.grid(row=0, column=0)

        account_name_label = tk.Label(userinfoframe, text="Account Name")
        account_name_label.grid(row=0, column=0)
        self.enter_name = tk.Entry(userinfoframe,width=40)
        self.enter_name.grid(row=0, column=1)

        account_number_label = tk.Label(userinfoframe, text="Account Number")
        account_number_label.grid(row=1, column=0)
        self.enter_number = tk.Entry(userinfoframe,width=40)
        self.enter_number.grid(row=1, column=1)

        # Inform user about allowed characters
        #account_number_instruction = tk.Label(userinfoframe, text="Only numbers and letters are allowed.")
        #account_number_instruction.grid(row=1, column=2, padx=10)
        #self.enter_number.grid(row=1, column=1)

        # Bind click event to the text box
        self.enter_number.bind("<Button-1>", self.show_message)


        account_email_label = tk.Label(userinfoframe, text="Account Email")
        account_email_label.grid(row=2, column=0)
        self.enter_email = tk.Entry(userinfoframe,width=40)
        self.enter_email.grid(row=2, column=1)

        account_balance_label = tk.Label(userinfoframe, text="Account Balance")
        account_balance_label.grid(row=3, column=0)
        initial_value = StringVar(value="0")
        self.initial_balance = tk.Entry(userinfoframe,width=40, textvariable=initial_value,state="readonly")
        self.initial_balance.grid(row=3, column=1)

        create_btn = tk.Button(userinfoframe, text='Create Account', command=self.get_create_account,bg="dodger blue", fg="white")
        create_btn.grid(row=4, column=0)

    def show_message(self, event):
        messagebox.showinfo(title="Info", message="Only numbers and letters are allowed for the account number.")

    def get_create_account(self):
        account_name = self.enter_name.get()
        account_number = self.enter_number.get()
        account_email = self.enter_email.get()
        initial_balance = self.initial_balance.get()

        if account_number and account_name and initial_balance:
            try:
                new_account = self.bank_system.create_account(account_name, account_number, initial_balance, account_email)
                if new_account:
                    messagebox.showinfo(title="Success", message="Account created successfully!")
            except ValueError as e:
                messagebox.showerror(title="Error", message=str(e))
        else:
            messagebox.showerror(title="Error", message="Please fill all required fields.")

    def open_login_window(self):
        self.login_window = tk.Toplevel(self.main_window)
        self.login_window.title("Login")
        frame = tk.Frame(self.login_window)
        frame.pack()

        userinfoframe = tk.LabelFrame(frame, text="Login ID")
        userinfoframe.grid(row=0, column=0)

        account_name_label = tk.Label(userinfoframe, text="Account Name")
        account_name_label.grid(row=0, column=0)
        self.enter_name = tk.Entry(userinfoframe, width=40)
        self.enter_name.grid(row=0, column=1)

        account_number_label = tk.Label(userinfoframe, text="Account Number")
        account_number_label.grid(row=1, column=0)
        self.enter_number = tk.Entry(userinfoframe, width=40)
        self.enter_number.grid(row=1, column=1)
        create_btn = tk.Button(userinfoframe, text='Continue', command=self.get_login_account,bg="dodger blue", fg="white")
        create_btn.grid(row=2, column=1)
    def get_login_account(self):
        account_name = self.enter_name.get()
        account_number = self.enter_number.get()
        account = self.bank_system.login(account_name, account_number)
        if account:
            self.current_account = account
            self.login_window.destroy()
            self.open_account_dashboard()
        else:
            messagebox.showerror(title="Error", message="Invalid account number or name.")
    def open_account_dashboard(self):
        # Create a new window for the logged-in user's dashboard
        self.dashboard_window = tk.Toplevel(self.main_window)
        self.dashboard_window.title("Account Dashboard")

        tk.Label(self.dashboard_window, text=f"Welcome, {self.current_account.account_name}").pack(pady=10)
        tk.Button(self.dashboard_window, text="Deposit", width=20, command=self.open_deposit_window,bg="dodger blue", fg="white").pack(pady=5)
        tk.Button(self.dashboard_window, text="Withdraw", width=20, command=self.open_withdraw_window,bg="dodger blue", fg="white").pack(pady=5)
        tk.Button(self.dashboard_window, text="View Balance", width=20, command=self.view_balance,bg="dodger blue", fg="white").pack(pady=5)
        tk.Button(self.dashboard_window, text="Transaction History", width=20, command=self.view_transaction_history,bg="dodger blue", fg="white").pack(pady=5)

        graph_btn = tk.Button(self.dashboard_window, text="View Transaction Graph",
                              command=self.show_transaction_graph, bg="dodger blue", fg="white")
        graph_btn.pack(pady=10)

        tk.Button(self.dashboard_window, text="Logout", width=20, command=self.logout,bg="dodger blue", fg="white").pack(pady=5)


        print("After deposit/withdraw, checking dashboard window status...")
    def open_deposit_window(self):
        self.transaction_window = tk.Toplevel(self.main_window)
        self.transaction_window.title("Deposit")

        tk.Label(self.transaction_window, text="Amount:").grid(row=0, column=0)
        self.transaction_amount_entry = tk.Entry(self.transaction_window)
        self.transaction_amount_entry.grid(row=0, column=1)

        tk.Button(self.transaction_window, text="Deposit", command=self.deposit).grid(row=1, columnspan=2, pady=10)

    def deposit(self):

            #self.dashboard_window=tk.Toplevel(self.main_window)
            if self.current_account is None:
                messagebox.showerror(title="Error", message="No account is logged in!")
                return
            try:
                amount = float(self.transaction_amount_entry.get())
                self.current_account.deposit(amount)
                self.bank_system.save_accounts()
                messagebox.showinfo(title="Success",message= f"${amount} deposited successfully!")
                #self.reopen_dashboard()
                self.transaction_window.destroy()

            except ValueError:
                messagebox.showerror(title="Error",message= "Invalid amount.")

    def open_withdraw_window(self):

        self.transaction_window = tk.Toplevel(self.main_window)
        self.transaction_window.title("Withdraw")

        tk.Label(self.transaction_window, text="Amount:").grid(row=0, column=0)
        self.transaction_amount_entry = tk.Entry(self.transaction_window)
        self.transaction_amount_entry.grid(row=0, column=1)

        tk.Button(self.transaction_window, text="Withdraw", command=self.withdraw).grid(row=1, columnspan=2, pady=10)


    def withdraw(self):
            try:
                amount = float(self.transaction_amount_entry.get())
                self.current_account.withdrawal(amount)
                self.bank_system.save_accounts()
                #messagebox.showinfo("Success", f"${amount} withdrawn successfully!")
                #self.reopen_dashboard()
                self.transaction_window.destroy()
            except ValueError as e:
                messagebox.showerror(title="Error",message= str(e))

    def view_balance(self):
            #self.reopen_dashboard()
            balance = self.current_account.get_balance()
            messagebox.showinfo(title="Current Balance", message=f"Your current balance is: ${balance:.2f}")

    def view_transaction_history(self):
            history = self.current_account.get_transaction_history()
            history_text = "\n".join(history) if history else "No transactions yet."
            messagebox.showinfo("Transaction History",  history_text)

    def reopen_dashboard(self):
        # Close the transaction window if it's open
        if hasattr(self, 'transaction_window') and self.transaction_window.winfo_exists():
            self.transaction_window.destroy()

        # Reopen the dashboard window
        if not hasattr(self, 'dashboard_window') or not self.dashboard_window.winfo_exists():
            self.open_account_dashboard()

    def show_transaction_graph(self):
        if not self.current_account:
            tk.messagebox.showerror("Error", "No account is logged in.")
            return

        # Prepare data for the graph
        transactions = self.current_account.get_transaction_history()
        balances = []
        balance = self.current_account.get_balance()  # Start with the current balance

        # Build balances list based on transaction history
        for transaction in reversed(transactions):  # Reverse to get the order correctly
            if transaction.startswith("Deposit"):
                amount = float(transaction.split("$")[1])
                balance -= amount
            elif transaction.startswith("Withdrawal"):
                amount = float(transaction.split("$")[1])
                balance += amount
            balances.insert(0, balance)  # Insert at the beginning to maintain chronological order

        # Add the current balance to the end of the list
        balances.append(self.current_account.get_balance())
        x_labels = [f"Transaction {i + 1}" for i in range(len(balances))]

        # Create a new window for the graph
        graph_window = tk.Toplevel(self.main_window)
        graph_window.title("Transaction Graph")

        # Create the Matplotlib figure
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x_labels, balances, marker='o', linestyle='-', color='blue')
        ax.set_title("Account Transaction History")
        ax.set_xlabel("Transactions")
        ax.set_ylabel("Balance ($)")
        ax.grid()

        # Embed the graph into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add a close button
        close_btn = tk.Button(graph_window, text="Close", command=graph_window.destroy)
        close_btn.pack(pady=10)

    def logout(self):
            self.current_account = None
            self.dashboard_window.destroy()
            messagebox.showinfo(title="Logged Out",message= "You have been logged out.")


if __name__ == "__main__":
    bankgui = BankAccountGUI()
    bankgui.main_window.mainloop()