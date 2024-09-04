import tkinter as tk
from tkinter import messagebox
import os

class ContactManager:
    def __init__(self, filename="contacts.txt"):
        self.filename = filename
        self.contacts = self.load_contacts()

    def load_contacts(self):
        if not os.path.exists(self.filename):
            return []
        with open(self.filename, "r") as file:
            contacts = [line.strip().split(",") for line in file.readlines()]
        return contacts

    def save_contacts(self):
        with open(self.filename, "w") as file:
            for contact in self.contacts:
                file.write(",".join(contact) + "\n")

    def add_contact(self, name, phone, email):
        self.contacts.append([name, phone, email])
        self.save_contacts()

    def view_contacts(self):
        return self.contacts

    def edit_contact(self, index, name=None, phone=None, email=None):
        if index < 1 or index > len(self.contacts):
            return "Invalid contact index."
        if name:
            self.contacts[index - 1][0] = name
        if phone:
            self.contacts[index - 1][1] = phone
        if email:
            self.contacts[index - 1][2] = email
        self.save_contacts()
        return "Contact updated successfully!"

    def delete_contact(self, index):
        if index < 1 or index > len(self.contacts):
            return "Invalid contact index."
        self.contacts.pop(index - 1)
        self.save_contacts()
        return "Contact deleted successfully!"

class ContactManagerGUI:
    def __init__(self, root):
        self.manager = ContactManager()
        self.root = root
        self.root.title("Contact Management System")

        # GUI Components
        self.create_widgets()

    def create_widgets(self):
        # Add Contact
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Phone:").grid(row=1, column=0, padx=10, pady=5)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text="Email:").grid(row=2, column=0, padx=10, pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Add Contact", command=self.add_contact).grid(row=3, column=0, columnspan=2, pady=10)

        # Contact List
        self.contacts_listbox = tk.Listbox(self.root, height=10, width=50)
        self.contacts_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.update_contact_list()

        # Edit and Delete Buttons
        tk.Button(self.root, text="Edit Contact", command=self.edit_contact).grid(row=5, column=0, padx=10, pady=10)
        tk.Button(self.root, text="Delete Contact", command=self.delete_contact).grid(row=5, column=1, padx=10, pady=10)

    def add_contact(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        if name and phone and email:
            self.manager.add_contact(name, phone, email)
            self.update_contact_list()
            self.clear_entries()
            messagebox.showinfo("Success", "Contact added successfully!")
        else:
            messagebox.showwarning("Input Error", "All fields are required!")

    def update_contact_list(self):
        self.contacts_listbox.delete(0, tk.END)
        for idx, contact in enumerate(self.manager.view_contacts(), start=1):
            self.contacts_listbox.insert(tk.END, f"{idx}. {contact[0]} | {contact[1]} | {contact[2]}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def edit_contact(self):
        selected_contact = self.contacts_listbox.curselection()
        if selected_contact:
            index = selected_contact[0] + 1
            name = self.name_entry.get()
            phone = self.phone_entry.get()
            email = self.email_entry.get()
            result = self.manager.edit_contact(index, name if name else None, phone if phone else None, email if email else None)
            self.update_contact_list()
            self.clear_entries()
            messagebox.showinfo("Success", result)
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to edit.")

    def delete_contact(self):
        selected_contact = self.contacts_listbox.curselection()
        if selected_contact:
            index = selected_contact[0] + 1
            result = self.manager.delete_contact(index)
            self.update_contact_list()
            messagebox.showinfo("Success", result)
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagerGUI(root)
    root.mainloop()