import tkinter as tk
from tkinter import ttk
import webbrowser
import store_loc
from store_loc import stores_near_me
from scan_get_recipes import scan_n_load

stores = stores_near_me().copy()
recipes = scan_n_load()

print(recipes)

def open_link(event, store_tree):
    selected_item = store_tree.selection()
    if selected_item:
        link = store_tree.item(selected_item, "values")[3]
        webbrowser.open(link)

def sort_by_missing_ingredients():
    global recipes
    recipes.sort(key=lambda x: len(x[2]))  # Sort by fewest missing ingredients first
    update_recipe_table()

def update_recipe_table():
    recipe_tree.delete(*recipe_tree.get_children())
    for recipe in recipes:
        name = recipe[0]
        owned_ingredients = ", ".join(recipe[1])
        missing_ingredients = ", ".join(recipe[2])
        recipe_tree.insert("", "end", values=(name, owned_ingredients, missing_ingredients))

def get_color_based_on_missing(missing_count, max_missing):
    ratio = missing_count / max_missing if max_missing > 0 else 0
    red = int(255 * ratio)
    green = int(255 * (1 - ratio)+75)
    return f"#{red:02X}{green:02X}00"

def open_store_window(recipe_name, missing_count, max_missing):
    store_window = tk.Toplevel(root)
    store_window.title(f"Nearby Grocery Stores - {recipe_name}")
    store_window.geometry("800x300")
    color = get_color_based_on_missing(missing_count, max_missing)
    store_window.configure(bg=color)
    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#23272A", foreground="white", fieldbackground="#2C2F33", font=("Arial", 12))
    style.configure("Treeview.Heading", background="#7289DA", foreground="white", font=("Arial", 12, "bold"))
    style.map("Treeview", background=[("selected", "#7289DA")])
    
    store_tree = ttk.Treeview(store_window, columns=("Name", "Address", "Distance"), show="headings", height=10)
    store_tree.heading("Name", text="Name")
    store_tree.heading("Address", text="Address")
    store_tree.heading("Distance", text="Distance (km)")
    
    store_tree.column("Name", width=200, anchor="center")
    store_tree.column("Address", width=300, anchor="center")
    store_tree.column("Distance", width=100, anchor="center")
    
    for store in stores:
        store_tree.insert("", "end", values=store)
    
    store_tree.bind("<Double-1>", lambda event: open_link(event, store_tree))
    store_tree.pack(fill="both", expand=True, padx=10, pady=10)

def on_recipe_double_click(event):
    selected_item = recipe_tree.selection()
    if selected_item:
        item = recipe_tree.item(selected_item, "values")
        recipe_name = item[0]
        missing_count = len(item[2].split(", ")) if item[2] else 0
        max_missing = max(len(r[2]) for r in recipes) if recipes else 1
        open_store_window(recipe_name, missing_count, max_missing)

root = tk.Tk()
root.title("Found Recipes")
root.geometry("800x800")
root.configure(bg="#2C2F33")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#23272A", foreground="white", fieldbackground="#2C2F33", font=("Arial", 12))
style.configure("Treeview.Heading", background="#7289DA", foreground="white", font=("Arial", 12, "bold"))
style.map("Treeview", background=[("selected", "#7289DA")])

recipe_tree = ttk.Treeview(root, columns=("Recipe name", "Owned ingredients", "Missing Ingredients"), show="headings", height=10)
recipe_tree.heading("Recipe name", text="Recipe name")
recipe_tree.heading("Owned ingredients", text="Owned ingredients")
recipe_tree.heading("Missing Ingredients", text="Missing Ingredients", command=sort_by_missing_ingredients)

recipe_tree.column("Recipe name", width=200, anchor="center")
recipe_tree.column("Owned ingredients", width=300, anchor="center")
recipe_tree.column("Missing Ingredients", width=300, anchor="center")

update_recipe_table()
sort_by_missing_ingredients()

recipe_tree.bind("<Double-1>", on_recipe_double_click)
recipe_tree.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
