import tkinter as tk
from tkinter import ttk
import csv
import random

class Shop:
    
    def __init__(self,root):
        self.root = root
        self.root.title("Geeckjack")
        self.root.geometry("700x300")
        
        self.initialize_csv_files()
        self.setup_ui()
        
        self.read_csv("products.csv", self.product_listbox)
    
    def create_if_not_found_csv(self, filename, headers):
        try:
            with open(filename, mode='r') as file:
                pass
        except FileNotFoundError:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                
    def initialize_csv_files(self):
        self.create_if_not_found_csv("products.csv", ["Product ID", "Name", "Price", "Stock"])
        self.create_if_not_found_csv("customers.csv", ["Customer ID", "Name", "Contact"])
        self.create_if_not_found_csv("orders.csv", ["Order ID", "Customer ID", "Product ID", "Quantity"])
    
    def setup_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)
        
        self.products_tab = ttk.Frame(notebook)
        self.customers_tab = ttk.Frame(notebook)
        self.orders_tab = ttk.Frame(notebook)
        
        notebook.add(self.products_tab, text="Products")
        notebook.add(self.customers_tab, text="Customers") 
        notebook.add(self.orders_tab, text="Orders")
        
        self.setup_products_tab()
        self.setup_customers_tab()
        self.setup_orders_tab()
    
    def setup_products_tab(self):
        tk.Label(self.products_tab, text="Name").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.products_tab, text="Price").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.products_tab, text="Stock").grid(row=3, column=0, padx=10, pady=5)

        self.product_name_entry = tk.Entry(self.products_tab)
        self.product_price_entry = tk.Entry(self.products_tab)
        self.product_stock_entry = tk.Entry(self.products_tab)

        self.product_name_entry.grid(row=1, column=1)
        self.product_price_entry.grid(row=2, column=1)
        self.product_stock_entry.grid(row=3, column=1)

        self.product_listbox = tk.Listbox(self.products_tab, width=60)
        self.product_listbox.grid(row=0, column=3, rowspan=8, padx=20)

        tk.Button(self.products_tab, text="Add Product", command=self.add_product).grid(row=5, column=1, pady=10)
        tk.Button(self.products_tab, text="Refresh", command=lambda: self.read_csv("products.csv", self.product_listbox)).grid(row=6, column=1)
        tk.Button(self.products_tab, text="Delete Selected", command=lambda: self.delete_selected("products.csv", self.product_listbox)).grid(row=7, column=1)
        
    def setup_customers_tab(self):
        tk.Label(self.customers_tab, text="Name").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.customers_tab, text="Contact").grid(row=2, column=0, padx=10, pady=5)

        self.customer_name_entry = tk.Entry(self.customers_tab)
        self.customer_contact_entry = tk.Entry(self.customers_tab)

        self.customer_name_entry.grid(row=1, column=1)
        self.customer_contact_entry.grid(row=2, column=1)

        self.customer_listbox = tk.Listbox(self.customers_tab, width=60)
        self.customer_listbox.grid(row=0, column=3, rowspan=8, padx=20)
        
        tk.Button(self.customers_tab, text="Add Customer", command=self.add_customer).grid(row=4, column=1, pady=10)
        tk.Button(self.customers_tab, text="Refresh", command=lambda: self.read_csv("customers.csv", self.customer_listbox)).grid(row=5, column=1)
        tk.Button(self.customers_tab, text="Delete Selected",command=lambda: self.delete_selected("customers.csv", self.customer_listbox)).grid(row=6, column=1)
    
    def setup_orders_tab(self):

        tk.Label(self.orders_tab, text="Customer ID").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.orders_tab, text="Product ID").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.orders_tab, text="Quantity").grid(row=3, column=0, padx=10, pady=5)

        self.order_customer_entry = tk.Entry(self.orders_tab)
        self.order_product_entry = tk.Entry(self.orders_tab)
        self.order_quantity_entry = tk.Entry(self.orders_tab)

        self.order_customer_entry.grid(row=1, column=1)
        self.order_product_entry.grid(row=2, column=1)
        self.order_quantity_entry.grid(row=3, column=1)

        self.order_listbox = tk.Listbox(self.orders_tab, width=60)
        self.order_listbox.grid(row=0, column=3, rowspan=8, padx=20)


        tk.Button(self.orders_tab, text="Create Order", command=self.add_order).grid(row=5, column=1, pady=10)
        tk.Button(self.orders_tab, text="Refresh", command=lambda: self.read_csv("orders.csv", self.order_listbox)).grid(row=6, column=1)
        tk.Button(self.orders_tab, text="Delete Selected",command=lambda: self.delete_selected("orders.csv", self.order_listbox)).grid(row=7, column=1)

    def generate_id(self, prefix, filename):
        existing = set()
        try:
            with open(filename, mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                
                for row in reader:
                    existing.add(row[0])
        except FileNotFoundError:
            pass
        
        while True:
            new_id = f"{prefix}{random.randint(1000, 9999)}"
            if new_id not in existing:
                return new_id
    
    def append_to_csv(self,filename, data):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        
    def read_csv(self, filename, listbox):
        listbox.delete(0, tk.END)
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    listbox.insert(tk.END, ", ".join(row))
        except FileNotFoundError:
            pass
    def delete_selected(self, filename, listbox):
        selected = listbox.curselection()
        if not selected:
            return
        index = selected[0]
        listbox.delete(index)
        with open(filename, mode='r') as file:
            lines = file.readlines()
        with open(filename, mode='w') as file:
            for i, line in enumerate(lines):
                if i != index:
                    file.write(line)
    
    def add_product(self):
        
        product_id = self.generate_id("P", "products.csv")
        
        data = [
            product_id,
            self.product_name_entry.get(),
            self.product_price_entry.get(),
            self.product_stock_entry.get()
        ]
        
        self.append_to_csv("products.csv", data)
        self.read_csv("products.csv", self.product_listbox)
        
    def add_customer(self):
        customer_id = self.generate_id("C", "products.csv")
        data = [
            customer_id,
            self.customer_name_entry.get(),
            self.customer_contact_entry.get()
        ]
        
        self.append_to_csv("customers.csv", data)
        self.read_csv("customers.csv", self.customer_listbox)
    
    def add_order(self):
        order_id = self.generate_id("P", "products.csv")
        
        data = [
            order_id,
            self.order_customer_entry.get(),
            self.order_product_entry.get(),
            self.order_quantity_entry.get()
        ]
        
        self.append_to_csv("orders.csv", data)
        self.read_csv("orders.csv", self.order_listbox)

if __name__ == "__main__":
    root = tk.Tk()
    shop = Shop(root)
    root.mainloop()