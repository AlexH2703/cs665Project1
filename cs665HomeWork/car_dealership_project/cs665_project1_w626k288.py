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
    display_data(rows, ["ID", "First", "Last", "Phone", "Email"])

def view_inventory():
    query = """
    SELECT Car.CarID, Car.Make, Car.Model, Car.Year, Inventory.Price, Inventory.Status
    FROM Car
    JOIN Inventory ON Car.CarID = Inventory.CarID
    WHERE Inventory.Status = 'Available'
    """
    rows = myDatabase.execute_query(query)
    display_data(rows, ["CarID", "Make", "Model", "Year", "Price", "Status"])

def view_sales():
    query = """
    SELECT Sales.SaleID, Customer.FirstName, Customer.LastName, Car.Make, Car.Model, Sales.SaleDate, Sales.TotalPrice
    FROM Sales
    JOIN Customer ON Sales.CustomerID = Customer.CustomerID
    JOIN Inventory ON Sales.InventoryID = Inventory.InventoryID
    JOIN Car ON Inventory.CarID = Car.CarID
    """
    rows = myDatabase.execute_query(query)
    display_data(rows, ["SaleID", "First Name", "Last Name", "Make", "Model", "Sale Date", "Total Price"])

def display_data(rows, columns):
    # Clear all current columns and data
    treeview.delete(*treeview.get_children())
    treeview["columns"] = columns

    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center")

    # Insert the data into the treeview
    if rows:
        for row in rows:
            clean_row = tuple(val[0] if isinstance(val, tuple) else val for val in row)
            treeview.insert("", "end", values=clean_row)


def add_sale():
    customer_id_value = customer_id.get()
    inventory_id_value = inventory_id.get()
    technician_name_value = technician_name.get()
    sale_date_value = sale_date.get()

    if not customer_id_value or not inventory_id_value or not technician_name_value or not sale_date_value:
        messagebox.showwarning("Input Error", "All fields must be filled!")
        return

    query = """
    INSERT INTO Sales (CustomerID, InventoryID, TechnicianName, SaleDate, TotalPrice)
    VALUES (?, ?, ?, ?, (SELECT Price FROM Inventory WHERE InventoryID = ?))
    """
    params = (customer_id_value, inventory_id_value, technician_name_value, sale_date_value, inventory_id_value)
    myDatabase.execute_query(query, params)
    messagebox.showinfo("Success", "Sale added successfully.")

def delete_customer():
    selected = treeview.selection()  # use the unified treeview
    if not selected:
        messagebox.showwarning("Warning", "No customer selected.")
        return

    try:
        customer_id = int(treeview.item(selected[0])['values'][0])
        query = "DELETE FROM Customer WHERE CustomerID = ?"
        myDatabase.execute_query(query, (customer_id,))
        messagebox.showinfo("Success", "Customer deleted.")
        view_customers()  # refresh view
    except ValueError:
        messagebox.showerror("Error", "Invalid customer ID format.")



# --- GUI SETUP ---
root = tk.Tk()
root.title("Car Dealership Management")

# --- Create frames for grouping ---
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# --- Customer form inputs ---
first_name = tk.StringVar()
last_name = tk.StringVar()
phone = tk.StringVar()
email = tk.StringVar()

tk.Label(input_frame, text="First Name").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(input_frame, textvariable=first_name).grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Last Name").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(input_frame, textvariable=last_name).grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Phone Number").grid(row=0, column=2, padx=5, pady=5)
tk.Entry(input_frame, textvariable=phone).grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Email").grid(row=1, column=2, padx=5, pady=5)
tk.Entry(input_frame, textvariable=email).grid(row=1, column=3, padx=5, pady=5)

tk.Button(input_frame, text="Add Customer", command=add_customer).grid(row=2, column=0, columnspan=2, pady=5)
tk.Button(input_frame, text="View Customers", command=view_customers).grid(row=4, column=0, columnspan=2, pady=5)
tk.Button(input_frame, text="Delete Selected", command=delete_customer).grid(row=2, column=1, columnspan=2, pady=5)

tk.Button(input_frame, text="View Inventory", command=view_inventory).grid(row=4, column=1, columnspan=2, pady=5)
tk.Button(input_frame, text="View Sales", command=view_sales).grid(row=4, column=2, columnspan=2, pady=5)
# --- Sales form inputs ---
customer_id = tk.StringVar()
inventory_id = tk.StringVar()
technician_name = tk.StringVar()
sale_date = tk.StringVar()

tk.Label(input_frame, text="Customer ID").grid(row=5, column=0, padx=5, pady=5)
tk.Entry(input_frame, textvariable=customer_id).grid(row=5, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Inventory ID").grid(row=5, column=2, padx=5, pady=5)
tk.Entry(input_frame, textvariable=inventory_id).grid(row=5, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Technician Name").grid(row=6, column=0, padx=5, pady=5)
tk.Entry(input_frame, textvariable=technician_name).grid(row=6, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Sale Date (YYYY-MM-DD)").grid(row=6, column=2, padx=5, pady=5)
tk.Entry(input_frame, textvariable=sale_date).grid(row=6, column=3, padx=5, pady=5)

tk.Button(input_frame, text="Add Sale", command=add_sale).grid(row=7, column=0, columnspan=4, pady=5)

# --- Treeview for displaying data ---
treeview_frame = tk.Frame(root)
treeview_frame.pack(pady=10)

treeview = ttk.Treeview(treeview_frame, show='headings')  # Initially empty treeview
treeview.pack()

# --- Initially show customers ---
view_customers()

root.mainloop()
