import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os


root = tk.Tk()
root.title("Online Shop Management System")
root.geometry("900x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)


products_tab = ttk.Frame(notebook)
notebook.add(products_tab, text="Products")

tk.Label(products_tab, text="Product ID").grid(row=0, column=0, padx=10, pady=5)
tk.Label(products_tab, text="Name").grid(row=1, column=0, padx=10, pady=5)
tk.Label(products_tab, text="Price").grid(row=2, column=0, padx=10, pady=5)
tk.Label(products_tab, text="Stock").grid(row=3, column=0, padx=10, pady=5)

product_id_entry = tk.Entry(products_tab)
product_name_entry = tk.Entry(products_tab)
product_price_entry = tk.Entry(products_tab)
product_stock_entry = tk.Entry(products_tab)

product_id_entry.grid(row=0, column=1)
product_name_entry.grid(row=1, column=1)
product_price_entry.grid(row=2, column=1)
product_stock_entry.grid(row=3, column=1)

product_listbox = tk.Listbox(products_tab, width=60)
product_listbox.grid(row=0, column=3, rowspan=8, padx=20)


customers_tab = ttk.Frame(notebook)
notebook.add(customers_tab, text="Customers")

tk.Label(customers_tab, text="Customer ID").grid(row=0, column=0, padx=10, pady=5)
tk.Label(customers_tab, text="Name").grid(row=1, column=0, padx=10, pady=5)
tk.Label(customers_tab, text="Contact").grid(row=2, column=0, padx=10, pady=5)

customer_id_entry = tk.Entry(customers_tab)
customer_name_entry = tk.Entry(customers_tab)
customer_contact_entry = tk.Entry(customers_tab)

customer_id_entry.grid(row=0, column=1)
customer_name_entry.grid(row=1, column=1)
customer_contact_entry.grid(row=2, column=1)

customer_listbox = tk.Listbox(customers_tab, width=60)
customer_listbox.grid(row=0, column=3, rowspan=8, padx=20)


orders_tab = ttk.Frame(notebook)
notebook.add(orders_tab, text="Orders")

tk.Label(orders_tab, text="Order ID").grid(row=0, column=0, padx=10, pady=5)
tk.Label(orders_tab, text="Customer ID").grid(row=1, column=0, padx=10, pady=5)
tk.Label(orders_tab, text="Product ID").grid(row=2, column=0, padx=10, pady=5)
tk.Label(orders_tab, text="Quantity").grid(row=3, column=0, padx=10, pady=5)

order_id_entry = tk.Entry(orders_tab)
order_customer_entry = tk.Entry(orders_tab)
order_product_entry = tk.Entry(orders_tab)
order_quantity_entry = tk.Entry(orders_tab)

order_id_entry.grid(row=0, column=1)
order_customer_entry.grid(row=1, column=1)
order_product_entry.grid(row=2, column=1)
order_quantity_entry.grid(row=3, column=1)

order_listbox = tk.Listbox(orders_tab, width=60)
order_listbox.grid(row=0, column=3, rowspan=8, padx=20)

def append_to_csv(filename, data):
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_csv(filename, listbox):
    listbox.delete(0, tk.END)
    if os.path.exists(filename):
        with open(filename, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                listbox.insert(tk.END, row)

def add_product():
    data = [
        product_id_entry.get(),
        product_name_entry.get(),
        product_price_entry.get(),
        product_stock_entry.get()
    ]
    append_to_csv("products.csv", data)
    read_csv("products.csv", product_listbox)
    messagebox.showinfo("Success", "Product Added")

def add_customer():
    data = [
        customer_id_entry.get(),
        customer_name_entry.get(),
        customer_contact_entry.get()
    ]
    append_to_csv("customers.csv", data)
    read_csv("customers.csv", customer_listbox)
    messagebox.showinfo("Success", "Customer Added")

def add_order():
    data = [
        order_id_entry.get(),
        order_customer_entry.get(),
        order_product_entry.get(),
        order_quantity_entry.get()
    ]
    append_to_csv("orders.csv", data)
    read_csv("orders.csv", order_listbox)
    messagebox.showinfo("Success", "Order Created")
def delete_selected(filename, listbox):
    selected = listbox.curselection()
    
    if not selected:
        messagebox.showwarning("Warning", "No item selected")
        return

    index = selected[0]
    listbox.delete(index)

    # Rewrite CSV without deleted row
    with open(filename, "r") as file:
        rows = list(csv.reader(file))

    rows.pop(index)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    messagebox.showinfo("Success", "Record Deleted")

tk.Button(products_tab, text="Add Product", command=add_product).grid(row=5, column=1, pady=10)
tk.Button(products_tab, text="Refresh", command=lambda: read_csv("products.csv", product_listbox)).grid(row=6, column=1)
tk.Button(products_tab, text="Delete Selected", command=lambda: delete_selected("products.csv", product_listbox)).grid(row=7, column=1)

tk.Button(customers_tab, text="Add Customer", command=add_customer).grid(row=4, column=1, pady=10)
tk.Button(customers_tab, text="Refresh", command=lambda: read_csv("customers.csv", customer_listbox)).grid(row=5, column=1)
tk.Button(customers_tab, text="Delete Selected",command=lambda: delete_selected("customers.csv", customer_listbox)).grid(row=6, column=1)

tk.Button(orders_tab, text="Create Order", command=add_order).grid(row=5, column=1, pady=10)
tk.Button(orders_tab, text="Refresh", command=lambda: read_csv("orders.csv", order_listbox)).grid(row=6, column=1)
tk.Button(orders_tab, text="Delete Selected",command=lambda: delete_selected("orders.csv", order_listbox)).grid(row=7, column=1)

root.mainloop()