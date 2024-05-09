# -*- coding: utf-8 -*-
"""
Created on Mon May  6 22:45:52 2024

@author: Lenovo
"""

import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('pets.db')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS pets''')

cur.execute('''CREATE TABLE pets (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                breed TEXT,
                available BOOLEAN)''')
conn.commit()


def add_pet():
    name = pet_name_entry.get()
    age = pet_age_entry.get()
    breed = pet_breed_entry.get()
    available = pet_available_var.get()

    if not all([name, age, breed]):
        messagebox.showerror("Error", "Please fill out all fields!")
        return
    try:
        int(age)
    except ValueError:
        messagebox.showerror("Error", "Invalid age format. Please enter a number.")
        return

    cur.execute("INSERT INTO pets (name, age, breed, available) VALUES (?, ?, ?, ?)",
                (name, age, breed, available))
    conn.commit()
    messagebox.showinfo("Success", "Pet added successfully!")
    clear_add_pet_fields()


def delete_pet():
    pet_id = delete_pet_id_entry.get()

    if not pet_id:
        messagebox.showerror("Error", "Please enter a pet ID to delete!")
        return
    try:
        int(pet_id)
    except ValueError:
        messagebox.showerror("Error", "Invalid pet ID format. Please enter a number.")
        return

    cur.execute("DELETE FROM pets WHERE id=?", (pet_id,))
    conn.commit()
    messagebox.showinfo("Success", "Pet deleted successfully!")
    delete_pet_id_entry.delete(0, tk.END)


def update_pet():
    pet_id = update_pet_id_entry.get()
    name = update_pet_name_entry.get()
    age = update_pet_age_entry.get()
    breed = update_pet_breed_entry.get()
    available = update_pet_available_var.get()

    if not all([pet_id, name, age, breed]):
        messagebox.showerror("Error", "Please fill out all fields!")
        return

    try:
        int(pet_id)
        int(age)
    except ValueError:
        messagebox.showerror("Error", "Invalid pet ID or age format. Please enter numbers.")
        return

    cur.execute("UPDATE pets SET name=?, age=?, breed=?, available=? WHERE id=?",
                (name, age, breed, available, pet_id))
    conn.commit()
    messagebox.showinfo("Success", "Pet record updated successfully!")
    clear_update_pet_fields()


def search_pets():
    search_term = search_entry.get()
    search_by = search_var.get()

    if not search_term:
        messagebox.showinfo("Search", "Please enter a search term.")
        return

    if search_by == "name":
        query = "SELECT * FROM pets WHERE LOWER(name) LIKE ?"
        params = ('%' + search_term.lower() + '%',)
    elif search_by == "breed":
        query = "SELECT * FROM pets WHERE LOWER(breed) LIKE ?"
        params = ('%' + search_term.lower() + '%',)
    else:
        messagebox.showerror("Error", "Invalid search criteria. Please choose name or breed.")
        return

    cur.execute(query, params)
    pets = cur.fetchall()

    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    if pets:
        for pet in pets:
            result_text.insert(tk.END, f"ID: {pet[0]}\nName: {pet[1]}\nAge: {pet[2]}\nBreed: {pet[3]}\nAvailable: {'Yes' if pet[4] else 'No'}\n\n")
    else:
        messagebox.showinfo("No Results", "No pets found matching the search criteria.")
    result_text.config(state=tk.DISABLED)


def clear_add_pet_fields():
    pet_name_entry.delete(0, tk.END)
    pet_age_entry.delete(0, tk.END)
    pet_breed_entry.delete(0, tk.END)
    pet_available_check.deselect()


def clear_delete_pet_field():
    delete_pet_id_entry.delete(0, tk.END)


def clear_update_pet_fields():
    update_pet_id_entry.delete(0, tk.END)
    update_pet_name_entry.delete(0, tk.END)
    update_pet_age_entry.delete(0, tk.END)
    update_pet_breed_entry.delete(0, tk.END)
    update_pet_available_check.deselect()


# GUI elements

root = tk.Tk()
root.title("Pet Adoption System")

root.config(background="black")

# Add Pet Section
add_frame = tk.LabelFrame(root, text="Add Pet", padx=10, pady=10)
add_frame.grid(row=0, column=0, padx=10, pady=10)

pet_name_label = tk.Label(add_frame, text="Pet Name:")
pet_name_label.grid(row=0, column=0)
pet_name_entry = tk.Entry(add_frame)
pet_name_entry.grid(row=0, column=1)

pet_age_label = tk.Label(add_frame, text="Age:")
pet_age_label.grid(row=1, column=0)
pet_age_entry = tk.Entry(add_frame)
pet_age_entry.grid(row=1, column=1)

pet_breed_label = tk.Label(add_frame, text="Breed:")
pet_breed_label.grid(row=2, column=0)
pet_breed_entry = tk.Entry(add_frame)
pet_breed_entry.grid(row=2, column=1)

pet_available_var = tk.BooleanVar()
pet_available_check = tk.Checkbutton(add_frame, text="Available for Adoption", variable=pet_available_var)
pet_available_check.grid(row=3, column=0, columnspan=2)

add_button = tk.Button(add_frame, text="Add Pet",font=("Times new Roman",15,"bold"),fg="white",bg="#5d76cb", command=add_pet)
add_button.grid(row=4, column=0, columnspan=2)


# Delete pet section
delete_pet_frame = tk.LabelFrame(root, text="Adopt Pet", padx=10, pady=10)
delete_pet_frame.grid(row=1, column=0, padx=10, pady=10)

delete_pet_id_label = tk.Label(delete_pet_frame, text="Pet ID:")
delete_pet_id_label.grid(row=0, column=0)

delete_pet_id_entry = tk.Entry(delete_pet_frame)
delete_pet_id_entry.grid(row=0, column=1)

delete_pet_button = tk.Button(delete_pet_frame, text="Adopt Pet", font=("Times new Roman",15,"bold"),fg="white",bg="#5d76cb",command=delete_pet)
delete_pet_button.grid(row=1, column=0, columnspan=2)


# Update pet section
update_frame = tk.LabelFrame(root, text="Update Pet", padx=10, pady=10)
update_frame.grid(row=0, column=1, padx=10, pady=10)

update_pet_id_label = tk.Label(update_frame, text="Pet ID:")
update_pet_id_label.grid(row=0, column=0)

update_pet_id_entry = tk.Entry(update_frame)
update_pet_id_entry.grid(row=0, column=1)

update_pet_name_label = tk.Label(update_frame, text="Name:")
update_pet_name_label.grid(row=1, column=0)

update_pet_name_entry = tk.Entry(update_frame)
update_pet_name_entry.grid(row=1, column=1)

update_pet_age_label = tk.Label(update_frame, text="Age:")
update_pet_age_label.grid(row=2, column=0)

update_pet_age_entry = tk.Entry(update_frame)
update_pet_age_entry.grid(row=2, column=1)

update_pet_breed_label = tk.Label(update_frame, text="Breed:")
update_pet_breed_label.grid(row=3, column=0)

update_pet_breed_entry = tk.Entry(update_frame)
update_pet_breed_entry.grid(row=3, column=1)

update_pet_available_var = tk.BooleanVar()
update_pet_available_check = tk.Checkbutton(update_frame, text="Available for Adoption", variable=update_pet_available_var)
update_pet_available_check.grid(row=4, column=0, columnspan=2)

update_button = tk.Button(update_frame, text="Update Pet",font=("Times new Roman",15,"bold"),fg="white",bg="#5d76cb", command=update_pet)
update_button.grid(row=5, column=0, columnspan=2)


# Search pet section
search_frame = tk.LabelFrame(root, text="Search Pets", padx=10, pady=10)
search_frame.grid(row=1, column=1, padx=10, pady=10)

search_label = tk.Label(search_frame, text="Search By:")
search_label.grid(row=0, column=0)

search_var = tk.StringVar()

search_name_radio = tk.Radiobutton(search_frame, text="Name", variable=search_var, value="name")
search_name_radio.grid(row=0, column=1)

search_breed_radio = tk.Radiobutton(search_frame, text="Breed", variable=search_var, value="breed")
search_breed_radio.grid(row=0, column=2)

search_entry = tk.Entry(search_frame)
search_entry.grid(row=1, column=0, columnspan=3)

search_button = tk.Button(search_frame, text="Search",font=("Times new Roman",15,"bold"),fg="white", bg="#5d76cb",command=search_pets)
search_button.grid(row=2, column=0, columnspan=3)

result_text = tk.Text(search_frame, height=5, width=50, state=tk.DISABLED)
result_text.grid(row=3, column=0, columnspan=3)

root.mainloop()
