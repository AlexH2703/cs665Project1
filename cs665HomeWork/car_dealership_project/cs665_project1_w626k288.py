import tkinter as tk
from tkinter import messagebox
import myDatabase 

# Example function to show customers from the database
def show_customers():
    query = "SELECT * FROM Customer"
    customers = myDatabase.execute_query(query)
    for customer in customers:
        print(customer)  

# Create the main window
root = tk.Tk()
root.title("Car Dealership Management")

# Example button to show customers
show_button = tk.Button(root, text="Show Customers", command=show_customers)
show_button.pack(pady=20)

root.mainloop()
