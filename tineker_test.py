import tkinter as tk
from tkinter import ttk
import webbrowser
import tkinter.font as tkFont  # Import font module
import store_loc
from store_loc import stores_near_me

stores = stores_near_me().copy()

def open_link(event):
    """Opens the Google Maps link for the selected store."""
    selected_item = tree.selection()
    if selected_item:
        link = tree.item(selected_item, "values")[3]
        webbrowser.open(link)

def sort_by_distance():
    """Sorts stores by distance and updates the table."""
    global stores
    stores = sorted(stores, key=lambda x: x[2])
    update_table()

def update_table():
    """Updates the table with the current store data."""
    tree.delete(*tree.get_children()) 
    for store in stores:
        tree.insert("", "end", values=store)


root = tk.Tk()
root.title("Nearby Grocery Stores")
root.geometry("800x300")
root.configure(bg="#2C2F33") 


style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#23272A", foreground="white", fieldbackground="#2C2F33", font=("Arial", 12))
style.configure("Treeview.Heading", background="#7289DA", foreground="white", font=("Arial", 12, "bold"))
style.map("Treeview", background=[("selected", "#7289DA")])


tree = ttk.Treeview(root, columns=("Name", "Address", "Distance"), show="headings", height=10)
tree.heading("Name", text="Name")
tree.heading("Address", text="Address")
tree.heading("Distance", text="Distance (km)", command=sort_by_distance) 

update_table()
sort_by_distance()

tree.bind("<Double-1>", open_link)

tree.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
