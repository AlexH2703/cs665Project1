import tkinter as tk
from tkinter import messagebox, ttk
import myDatabase

def clear_fields():
    first_name.set("")
    last_name.set("")
    phone.set("")
    email.set("")

def add_customer():
    query = "INSERT INTO Customer (FirstName, LastName, PhoneNumber, Email) VALUES (?, ?, ?, ?)"
    params = (first_name.get(), last_name.get(), phone.get(), email.get())
    myDatabase.execute_query(query, params)
    messagebox.showinfo("Success", "Customer added.")
    clear_fields()

def view_customers():
    query = "SELECT * FROM Customer"
    rows = myDatabase.execute_query(query)
    customer_list.delete(*customer_list.get_children())
    if rows:
        for row in rows:
            # Ensure all row values are scalar (not tuple-wrapped)
            clean_row = tuple(val[0] if isinstance(val, tuple) else val for val in row)
            customer_list.insert("", "end", values=clean_row)

def view_inventory():
    query = """
    SELECT Car.CarID, Car.Make, Car.Model, Car.Year, Inventory.Price, Inventory.Status
    FROM Car
    JOIN Inventory ON Car.CarID = Inventory.CarID
    WHERE Inventory.Status = 'Available'
    """
    rows = myDatabase.execute_query(query)
    inventory_list.delete(*inventory_list.get_children())  # Clear current entries in the Treeview

    if rows:
        for row in rows:
            # Ensure all row values are scalar (not tuple-wrapped)
            clean_row = tuple(val[0] if isinstance(val, tuple) else val for val in row)
            inventory_list.insert("", "end", values=clean_row)



def delete_customer():
    selected = customer_list.selection()
    if not selected:
        messagebox.showwarning("Warning", "No customer selected.")
        return

    customer_id = int(customer_list.item(selected[0])['values'][0])

    try:
        query = "DELETE FROM Customer WHERE CustomerID = ?"
        myDatabase.execute_query(query, (customer_id,))
        messagebox.showinfo("Success", "Customer deleted.")
        view_customers()
    except ValueError:
        messagebox.showerror("Error", "Invalid customer ID format.")


# --- GUI SETUP ---
root = tk.Tk()
root.title("Car Dealership Management")

# --- Input fields ---
first_name = tk.StringVar()
last_name = tk.StringVar()
phone = tk.StringVar()
email = tk.StringVar()

tk.Label(root, text="First Name").pack()
tk.Entry(root, textvariable=first_name).pack()

tk.Label(root, text="Last Name").pack()
tk.Entry(root, textvariable=last_name).pack()

tk.Label(root, text="Phone Number").pack()
tk.Entry(root, textvariable=phone).pack()

tk.Label(root, text="Email").pack()
tk.Entry(root, textvariable=email).pack()

tk.Button(root, text="Add Customer", command=add_customer).pack(pady=5)
tk.Button(root, text="View Customers", command=view_customers).pack(pady=5)
tk.Button(root, text="Delete Selected", command=delete_customer).pack(pady=5)

# --- Customer list ---
customer_list = ttk.Treeview(root, columns=("ID", "First", "Last", "Phone", "Email"), show='headings')
for col in ("ID", "First", "Last", "Phone", "Email"):
    customer_list.heading(col, text=col)
customer_list.pack(pady=10)

# --- Inventory viewer ---
inventory_list = ttk.Treeview(root, columns=("CarID", "Make", "Model", "Year", "Price", "Status"), show='headings')
for col in ("CarID", "Make", "Model", "Year", "Price", "Status"):
    inventory_list.heading(col, text=col)
inventory_list.pack(pady=10)

tk.Button(root, text="View Inventory", command=view_inventory).pack(pady=5)

root.mainloop()
