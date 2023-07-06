import json
import tkinter as tk
from tkinter import messagebox

# Initialize menu and orders
menu = []
orders = {}

# Load menu and orders data from JSON file
def load_data():
    try:
        with open('data.json') as file:
            data = json.load(file)
            menu.extend(data['menu'])
            orders.update(data['orders'])
    except FileNotFoundError:
        pass

# Save menu and orders data to JSON file
def save_data():
    data = {'menu': menu, 'orders': orders}
    with open('data.json', 'w') as file:
        json.dump(data, file)

# Function to add a dish to the menu
def add_dish():
    global dish_id_entry, dish_name_entry, price_entry, availability_entry
    dish_id = dish_id_entry.get()
    dish_name = dish_name_entry.get()
    price = float(price_entry.get())
    availability = availability_entry.get()

    dish = {
        'dish_id': dish_id,
        'dish_name': dish_name,
        'price': price,
        'availability': availability.lower() == 'yes'
    }

    menu.append(dish)
    save_data()
    messagebox.showinfo("Success", "Dish added to the menu successfully!")

    # Clear the entry fields
    dish_id_entry.delete(0, tk.END)
    dish_name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    availability_entry.delete(0, tk.END)

# Function to remove a dish from the menu
def remove_dish():
    global dish_id_entry
    dish_id = dish_id_entry.get()

    for dish in menu:
        if dish['dish_id'] == dish_id:
            menu.remove(dish)
            save_data()
            messagebox.showinfo("Success", "Dish removed from the menu successfully!")
            break
    else:
        messagebox.showerror("Error", "Dish not found in the menu.")

    # Clear the entry field
    dish_id_entry.delete(0, tk.END)

# Function to update the availability of a dish
def update_availability():
    global dish_id_entry, availability_entry

    dish_id = dish_id_entry.get()
    new_availability = availability_entry.get()

    for dish in menu:
        if dish['dish_id'] == dish_id:
            dish['availability'] = new_availability.lower() == 'yes'
            save_data()
            messagebox.showinfo("Success", "Availability updated successfully!")
            break
    else:
        messagebox.showerror("Error", "Dish not found in the menu.")

    # Clear the entry fields
    dish_id_entry.delete(0, tk.END)
    availability_entry.delete(0, tk.END)

# Function to take an order
def take_order():
    global customer_name_entry, dish_ids_entry

    customer_name = customer_name_entry.get()
    dish_ids = dish_ids_entry.get().split(',')

    order_id = len(orders) + 1
    order = {
        'customer_name': customer_name,
        'dishes': [],
        'status': 'received'
    }

    for dish_id in dish_ids:
        for dish in menu:
            if dish['dish_id'] == dish_id.strip() and dish['availability']:
                order['dishes'].append(dish)
                break
        else:
            messagebox.showerror("Error", f"Dish with ID {dish_id} is not available.")

    if order['dishes']:
        orders[order_id] = order
        save_data()
        messagebox.showinfo("Success", f"Order taken successfully! Order ID: {order_id}")

    # Clear the entry fields
    customer_name_entry.delete(0, tk.END)
    dish_ids_entry.delete(0, tk.END)

# Function to update the status of an order
def update_order_status():
    global order_id_entry, status_entry

    order_id = int(order_id_entry.get())
    new_status = status_entry.get()

    if order_id in orders:
        orders[order_id]['status'] = new_status
        save_data()
        messagebox.showinfo("Success", "Order status updated successfully!")
    else:
        messagebox.showerror("Error", "Order ID not found.")

    # Clear the entry fields
    order_id_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)

# Function to review all orders
def review_orders():
    if not orders:
        messagebox.showinfo("No Orders", "No orders found.")
        return

    order_text = ""
    for order_id, order in orders.items():
        order_text += f"Order ID: {order_id}\n"
        order_text += f"Customer Name: {order['customer_name']}\n"
        order_text += "Dishes:\n"
        for dish in order['dishes']:
            order_text += f"- {dish['dish_name']} (${dish['price']})\n"
        order_text += f"Status: {order['status']}\n\n"

    messagebox.showinfo("Orders", order_text)

# Function to exit the program
def exit_program():
    save_data()
    messagebox.showinfo("Goodbye", "Thank you for using Zesty Zomato's command-line system. Goodbye!")
    window.destroy()

# Create the GUI
def create_gui():
    global dish_id_entry, dish_name_entry, price_entry, availability_entry
    global customer_name_entry, dish_ids_entry, order_id_entry, status_entry

    window = tk.Tk()
    window.title("Zomato Chronicles")

    # Create labels
    label1 = tk.Label(window, text="Dish ID:")
    label1.grid(row=0, column=0, padx=5, pady=5)

    label2 = tk.Label(window, text="Dish Name:")
    label2.grid(row=1, column=0, padx=5, pady=5)

    label3 = tk.Label(window, text="Price:")
    label3.grid(row=2, column=0, padx=5, pady=5)

    label4 = tk.Label(window, text="Availability:")
    label4.grid(row=3, column=0, padx=5, pady=5)

    label5 = tk.Label(window, text="Dish ID:")
    label5.grid(row=0, column=0, padx=5, pady=5)

    label6 = tk.Label(window, text="Customer Name:")
    label6.grid(row=5, column=0, padx=5, pady=5)

    label7 = tk.Label(window, text="Dish IDs (comma-separated):")
    label7.grid(row=6, column=0, padx=5, pady=5)

    label8 = tk.Label(window, text="Order ID:")
    label8.grid(row=9, column=0, padx=5, pady=5)

    label9 = tk.Label(window, text="New Status:")
    label9.grid(row=10, column=0, padx=5, pady=5)

    # Create entry fields
    dish_id_entry = tk.Entry(window)
    dish_id_entry.grid(row=0, column=1, padx=5, pady=5)

    dish_name_entry = tk.Entry(window)
    dish_name_entry.grid(row=1, column=1, padx=5, pady=5)

    price_entry = tk.Entry(window)
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    availability_entry = tk.Entry(window)
    availability_entry.grid(row=3, column=1, padx=5, pady=5)

    customer_name_entry = tk.Entry(window)
    customer_name_entry.grid(row=5, column=1, padx=5, pady=5)

    dish_ids_entry = tk.Entry(window)
    dish_ids_entry.grid(row=6, column=1, padx=5, pady=5)

    order_id_entry = tk.Entry(window)
    order_id_entry.grid(row=9, column=1, padx=5, pady=5)

    status_entry = tk.Entry(window)
    status_entry.grid(row=10, column=1, padx=5, pady=5)

    # Create buttons
    add_dish_button = tk.Button(window, text="Add Dish", command=add_dish)
    add_dish_button.grid(row=4, column=0, padx=5, pady=5)

    remove_dish_button = tk.Button(window, text="Remove Dish", command=remove_dish)
    remove_dish_button.grid(row=4, column=1, padx=5, pady=5)

    update_availability_button = tk.Button(window, text="Update Availability", command=update_availability)
    update_availability_button.grid(row=4, column=2, padx=5, pady=5)

    take_order_button = tk.Button(window, text="Take Order", command=take_order)
    take_order_button.grid(row=7, column=0, padx=5, pady=5)

    update_order_status_button = tk.Button(window, text="Update Status", command=update_order_status)
    update_order_status_button.grid(row=11, column=0, padx=5, pady=5)

    review_orders_button = tk.Button(window, text="Review Orders", command=review_orders)
    review_orders_button.grid(row=11, column=1, padx=5, pady=5)

    exit_button = tk.Button(window, text="Exit", command=exit_program)
    exit_button.grid(row=11, column=2, padx=5, pady=5)

    # Start the GUI event loop
    window.mainloop()

# Load data from JSON file
load_data()

# Create the GUI
create_gui()