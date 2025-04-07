import tkinter as tk
from tkinter import messagebox, ttk
import myDatabase

def clear_fields():
    customer_id_var.set("")
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

def update_customer():
    cust_id = customer_id_var.get()
    if not cust_id:
        messagebox.showwarning("Warning", "No customer selected.")
        return

    query = """
    UPDATE Customer
    SET FirstName = ?, LastName = ?, PhoneNumber = ?, Email = ?
    WHERE CustomerID = ?
    """
    params = (first_name.get(), last_name.get(), phone.get(), email.get(), cust_id)
    myDatabase.execute_query(query, params)
    messagebox.showinfo("Success", "Customer updated.")
    view_customers()
    clear_fields()


def view_customers():
    current_view.set("customer")
    clear_fields()
    query = "SELECT * FROM Customer"
    rows = myDatabase.execute_query(query)
    display_data(rows, ["ID", "First", "Last", "Phone", "Email"])

def view_inventory():
    current_view.set("inventory")
    clear_fields()
    query = "SELECT * FROM Inventory"
    rows = myDatabase.execute_query(query)
    display_data(rows, ["InventoryID", "CarID", "Price", "Status"])

def view_sales():
    current_view.set("sales")
    clear_fields()
    query = "SELECT * FROM Sales"
    rows = myDatabase.execute_query(query)
    display_data(rows, ["SaleID", "CustomerID", "InventoryID", "TechnicianName", "SaleDate", "TotalPrice"])

def view_cars():
    current_view.set("car")
    clear_fields()
    query = "SELECT * FROM Car"
    rows = myDatabase.execute_query(query)
    display_data(rows, ["CarID", "Make", "Model", "Year", "VIN"])


def view_useful_inventory():
    current_view.set("useful_inventory")
    clear_fields()
    query = """
    SELECT Car.CarID, Car.Make, Car.Model, Car.Year, Inventory.Price, Inventory.Status
    FROM Car
    JOIN Inventory ON Car.CarID = Inventory.CarID
    WHERE Inventory.Status = 'Available'
    """
    rows = myDatabase.execute_query(query)
    display_data(rows, ["CarID", "Make", "Model", "Year", "Price", "Status"])

def view_useful_sales():
    current_view.set("useful_sales")
    clear_fields()
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

    insert_query = """
    INSERT INTO Sales (CustomerID, InventoryID, TechnicianName, SaleDate, TotalPrice)
    VALUES (?, ?, ?, ?, (SELECT Price FROM Inventory WHERE InventoryID = ?))
    """
    insert_params = (customer_id_value, inventory_id_value, technician_name_value, sale_date_value, inventory_id_value)
    
    update_query = "UPDATE Inventory SET Status = 'Sold' WHERE InventoryID = ?"

    myDatabase.execute_query(insert_query, insert_params)
    myDatabase.execute_query(update_query, (inventory_id_value,))
    
    messagebox.showinfo("Success", "Sale added and vehicle marked as sold.")
    view_useful_sales()


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

def delete_sale():
    selected = treeview.selection()
    if not selected:
        messagebox.showwarning("Warning", "No sale selected.")
        return

    try:
        sale_id = int(treeview.item(selected[0])['values'][0])  # First column is SaleID

        # First, get the InventoryID for the sale
        get_inventory_query = "SELECT InventoryID FROM Sales WHERE SaleID = ?"
        inventory_id_row = myDatabase.execute_query(get_inventory_query, (sale_id,))
        
        if not inventory_id_row:
            messagebox.showerror("Error", "Sale not found.")
            return
        
        inventory_id = inventory_id_row[0][0]  # Extract the InventoryID

        # Set the car status back to 'Available'
        update_inventory_query = "UPDATE Inventory SET Status = 'Available' WHERE InventoryID = ?"
        myDatabase.execute_query(update_inventory_query, (inventory_id,))

        # Now delete the sale
        delete_query = "DELETE FROM Sales WHERE SaleID = ?"
        myDatabase.execute_query(delete_query, (sale_id,))

        messagebox.showinfo("Success", "Sale deleted and vehicle marked as available.")
        view_useful_sales()
    
    except ValueError:
        messagebox.showerror("Error", "Invalid Sale ID format.")

def on_customer_select(event):
    if current_view.get() != "customer":
        return  # Only act when customer view is active

    selected = treeview.selection()
    if not selected:
        return

    values = treeview.item(selected[0], "values")
    if values and len(values) >= 5:
        customer_id_var.set(values[0])  # Store selected customer ID
        first_name.set(values[1])
        last_name.set(values[2])
        phone.set(values[3])
        email.set(values[4])



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
customer_id_var = tk.StringVar()  # Used for updating customers


tk.Button(input_frame, text="View Customers", command=view_customers).grid(row=0, column=0, columnspan=1, pady=5)
tk.Button(input_frame, text="View Inventory", command=view_inventory).grid(row=0, column=1, columnspan=1, pady=5)
tk.Button(input_frame, text="View Sales", command=view_sales).grid(row=0, column=2, columnspan=1, pady=5)
tk.Button(input_frame, text="View Cars", command=view_cars).grid(row=0, column=3, columnspan=1, pady=5)
tk.Button(input_frame, text="View Useful Inventory Info", command=view_useful_inventory).grid(row=0, column=6, columnspan=1, pady=5)
tk.Button(input_frame, text="View Useful Sales Info", command=view_useful_sales).grid(row=0, column=7, columnspan=1, pady=5)

tk.Label(input_frame, text="First Name").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(input_frame, textvariable=first_name).grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Last Name").grid(row=2, column=0, padx=5, pady=5)
tk.Entry(input_frame, textvariable=last_name).grid(row=2, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Phone Number").grid(row=1, column=2, padx=5, pady=5)
tk.Entry(input_frame, textvariable=phone).grid(row=1, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Email").grid(row=2, column=2, padx=5, pady=5)
tk.Entry(input_frame, textvariable=email).grid(row=2, column=3, padx=5, pady=5)

tk.Button(input_frame, text="Add Customer", command=add_customer).grid(row=3, column=1, columnspan=1, pady=5)
tk.Button(input_frame, text="Delete Customer", command=delete_customer).grid(row=3, column=2, columnspan=1, pady=5)
tk.Button(input_frame, text="Update Customer", command=update_customer).grid(row=3, column=3, columnspan=1, pady=5)


# --- Sales form inputs ---
customer_id = tk.StringVar()
inventory_id = tk.StringVar()
technician_name = tk.StringVar()
sale_date = tk.StringVar()
current_view = tk.StringVar(value="customer") 


tk.Label(input_frame, text="Customer ID").grid(row=1, column=5, padx=5, pady=5)
tk.Entry(input_frame, textvariable=customer_id).grid(row=1, column=6, padx=5, pady=5)

tk.Label(input_frame, text="Inventory ID").grid(row=1, column=7, padx=5, pady=5)
tk.Entry(input_frame, textvariable=inventory_id).grid(row=1, column=8, padx=5, pady=5)

tk.Label(input_frame, text="Technician Name").grid(row=2, column=5, padx=5, pady=5)
tk.Entry(input_frame, textvariable=technician_name).grid(row=2, column=6, padx=5, pady=5)

tk.Label(input_frame, text="Sale Date (YYYY-MM-DD)").grid(row=2, column=7, padx=5, pady=5)
tk.Entry(input_frame, textvariable=sale_date).grid(row=2, column=8, padx=5, pady=5)

tk.Button(input_frame, text="Add Sale", command=add_sale).grid(row=3, column=6, columnspan=1, pady=5)
tk.Button(input_frame, text="Delete Sale", command=delete_sale).grid(row=3, column=7, columnspan=1, pady=5)


# --- Treeview for displaying data ---
treeview_frame = tk.Frame(root)
treeview_frame.pack(pady=10)

treeview = ttk.Treeview(treeview_frame, show='headings')  # Initially empty treeview
treeview.pack()
treeview.bind("<<TreeviewSelect>>", on_customer_select)


# --- Initially show customers ---
view_customers()

root.mainloop()
