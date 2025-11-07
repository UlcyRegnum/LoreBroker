# main.py
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from generalstyles import configure_styles
import sys
import os
import re

class LoreBroker:
    def __init__(self, root):
        self.root = root
        self.root.title("Lore Broker")
        self.root.geometry("1200x680")
        self.current_book_name = ""
        self.entries = {}

        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(__file__)

        self.lore_books_dir = os.path.join(app_dir, "LoreBooks")
        os.makedirs(self.lore_books_dir, exist_ok=True)

        #TK Field Styles for ease of use
        self.root.configure(bg="#366899")
        self.widget_style = {'font': ("Arial", 10),'bg': "#B4C3D2",'fg': "black"}

        #TTK Field Styles - In General Styles file
        configure_styles(root)

        #Configure grid weights default
        for col in range(3):
            root.columnconfigure(col, weight=1)
        for row in range(8):
            root.rowconfigure(row, weight=1)

        #Lore Entry List Box and Title
        lore_title = ttk.Label(root, text="Lore Entries", style="Title.TLabel")
        lore_title.grid(row=0, column=0, sticky="S", padx=5, pady=(5, 0))

        listbox_frame = tk.Frame(root)
        listbox_frame.grid(row=1, column=0, rowspan=5, sticky="nsew", padx=5, pady=5)
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        self.listbox = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, exportselection=False, width=25, **self.widget_style)
        self.listbox.bind('<<ListboxSelect>>', self.on_entry_select)
        self.listbox.grid(row=0, column=0, sticky="nsew")

        #Lore Entry Scroll Bar
        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

        #Delete Entry Button
        delete_entry_button = ttk.Button(root, text="Delete Entry", command=self.delete_entry)
        delete_entry_button.grid(row=6, column=0, sticky="s", padx=5, pady=5)

        #Book and Entry frames
        titles_frame = ttk.Frame(root, style="Subframe.TFrame")
        titles_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        titles_frame.columnconfigure(1, weight=1)

        #Book Entry field
        book_title_title = ttk.Label(titles_frame, text="Book Title:", style="Sublabel.TLabel")
        book_title_title.grid(row=0, column=0, sticky="w")
        self.book_var = tk.StringVar()
        self.book_field = ttk.Entry(titles_frame, textvariable=self.book_var)
        self.book_field.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        #Entry Name field
        entry_title_title = ttk.Label(titles_frame, text="Entry Title:", style="Sublabel.TLabel")
        entry_title_title.grid(row=1, column=0, sticky="w")
        self.entry_var = tk.StringVar()
        self.entry_title_field = ttk.Entry(titles_frame, textvariable=self.entry_var)
        self.entry_title_field.grid(row=1, column=1, sticky="ew", padx=5)

        #Keywords frame and entry box
        keywords_frame = ttk.Frame(root, style="Subframe.TFrame")
        keywords_frame.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        keywords_frame.columnconfigure(1, weight=1)

        #Keywords entry box
        keywords_title = ttk.Label(keywords_frame, text="Keywords:", style="Sublabel.TLabel")
        keywords_title.grid(row=0, column=0, sticky="w")
        self.keywords_var = tk.StringVar()
        self.keywords_field = ttk.Entry(keywords_frame, textvariable=self.keywords_var)
        self.keywords_field.grid(row=0, column=1, sticky="ew", padx=5)

        #Secondary Keywords frame and entry box
        sec_keywords_frame = ttk.Frame(root, style="Subframe.TFrame")
        sec_keywords_frame.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        sec_keywords_frame.columnconfigure(1, weight=1)

        #Keywords Entry Box
        sec_keywords_title = ttk.Label(sec_keywords_frame, text="Secondary Keywords:", style="Sublabel.TLabel")
        sec_keywords_title.grid(row=0, column=0, sticky="w")
        self.sec_keywords_var = tk.StringVar()
        self.sec_keywords_field = ttk.Entry(sec_keywords_frame, textvariable=self.sec_keywords_var)
        self.sec_keywords_field.grid(row=0, column=1, sticky="ew", padx=5)

        #Secondary Logic and Selective
        sec_logic_frame = ttk.Frame(root, style="Subframe.TFrame")
        sec_logic_frame.grid(row=2, column=2, sticky="ew", padx=5, pady=5)
        sec_logic_frame.columnconfigure(1, weight=1)

        #Determines if the selective Logic is used or not
        sec_selective_title = ttk.Label(sec_logic_frame, text="Selective:", style="Sublabel.TLabel")
        sec_selective_title.grid(row=0, column=0, sticky="w")
        self.sec_selective_var = tk.BooleanVar(value=False)
        self.sec_selective_field = ttk.Checkbutton(sec_logic_frame,variable=self.sec_selective_var)
        self.sec_selective_field.grid(row=0, column=1, sticky="w", padx=5)

        #Determines if selective logic is AND or NOT
        #Helper functions below for get_sec_logic_value and set_sec_logic_value
        sec_logic_title = ttk.Label(sec_logic_frame, text="Secondary Logic:", style="Sublabel.TLabel")
        sec_logic_title.grid(row=1, column=0, sticky="w")
        self.sec_logic_var = tk.StringVar(value="AND")
        self.sec_logic_field = ttk.Combobox(sec_logic_frame, textvariable=self.sec_logic_var, values=["AND", "NOT"], state="readonly", width=6)
        self.sec_logic_field.grid(row=1, column=1, sticky="w", padx=5)

        # Entry Content Text Box
        #set_content_text and get_content_text helper functions created for storage
        entry_content_frame = ttk.Frame(root, style="Subframe.TFrame")
        entry_content_frame.grid(row=3, column=1, rowspan=2, columnspan=2, sticky="ew", padx=5, pady=5)
        entry_content_frame.columnconfigure(0, weight=1)
        entry_content_frame.rowconfigure(1, weight=1)

        entry_content_title = ttk.Label(entry_content_frame, text="Content:", style="Sublabel.TLabel")
        entry_content_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        self.entry_content_field = scrolledtext.ScrolledText(entry_content_frame, wrap=tk.WORD, height=10, padx=5, pady=5, **self.widget_style)
        self.entry_content_field.grid(row=1, column=0, columnspan=2, sticky="nsew")

        #Insertion and Constant Frames
        insert_opt_frame = ttk.Frame(root, style="Subframe.TFrame")
        insert_opt_frame.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        insert_opt_frame.columnconfigure(1, weight=1)

        #Insert Order entry
        #Helper functions below for set_insert_order and get_insert_order
        insert_opt_title = ttk.Label(insert_opt_frame, text="Insertion Order:", style="Sublabel.TLabel")
        insert_opt_title.grid(row=0, column=0, sticky="w")
        self.insert_order_var = tk.StringVar(value=10)
        self.insert_opt_field = ttk.Entry(insert_opt_frame, width=5, textvariable=self.insert_order_var)
        self.insert_opt_field.grid(row=0, column=1, sticky="w", padx=5)

        #Constant selection box
        constant_title = ttk.Label(insert_opt_frame, text="Constant:", style="Sublabel.TLabel")
        constant_title.grid(row=1, column=0, sticky="w")
        self.constant_var = tk.BooleanVar(value=False)
        self.constant_field = ttk.Checkbutton(insert_opt_frame,variable=self.constant_var)
        self.constant_field.grid(row=1, column=1, sticky="w", padx=5)

        #Probability and Priority Frames
        probability_frame = ttk.Frame(root, style="Subframe.TFrame")
        probability_frame.grid(row=5, column=2, sticky="ew", padx=5, pady=5)
        probability_frame.columnconfigure(1, weight=1)

        #Helper functions below for set_probability and get_probability
        probability_title = ttk.Label(probability_frame, text="Probability:", style="Sublabel.TLabel")
        probability_title.grid(row=0, column=0, sticky="w")
        self.probability_var = tk.StringVar(value=100)
        self.probability_field = ttk.Entry(probability_frame, width=5, textvariable=self.probability_var)
        self.probability_field.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        #Helper functions below for set_priority_order and get_priority_order
        priority_title = ttk.Label(probability_frame, text="Priority:", style="Sublabel.TLabel")
        priority_title.grid(row=1, column=0, sticky="w")
        self.priority_var = tk.StringVar(value=10)
        self.priority_field = ttk.Entry(probability_frame, width=5, textvariable=self.priority_var)
        self.priority_field.grid(row=1, column=1, sticky="w", padx=5)

        #Enabled and Case Frames
        enabled_frame = ttk.Frame(root, style="Subframe.TFrame")
        enabled_frame.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        enabled_frame.columnconfigure(1, weight=1)

        case_title = ttk.Label(enabled_frame, text="Case Sensitive:", style="Sublabel.TLabel")
        case_title.grid(row=0, column=0, sticky="w")
        self.case_var = tk.BooleanVar(value=False)
        self.case_field = ttk.Checkbutton(enabled_frame, variable=self.case_var)
        self.case_field.grid(row=0, column=1, sticky="w", padx=5)

        enabled_title = ttk.Label(enabled_frame, text="Enabled:", style="Sublabel.TLabel")
        enabled_title.grid(row=1, column=0, sticky="w")
        self.enabled_var = tk.BooleanVar(value=True)
        self.enabled_field = ttk.Checkbutton(enabled_frame,variable=self.enabled_var)
        self.enabled_field.grid(row=1, column=1, sticky="w", padx=5)

        #New Entry and Save Entry Buttons
        newsave_frame = ttk.Frame(root, style="Subframe.TFrame")
        newsave_frame.grid(row=6, column=2, sticky="ew", padx=5, pady=5)
        newsave_frame.columnconfigure(1, weight=1)

        newentry_button = ttk.Button(newsave_frame, text="New Entry", command=self.new_entry)
        newentry_button.grid(row=0, column=0, sticky="w", padx=5)

        saveentry_button = ttk.Button(newsave_frame, text="Save Entry", command=self.save_entry)
        saveentry_button.grid(row=0, column=1, sticky="w")

        #Import and Export JSON Buttons
        loadsave_frame = ttk.Frame(root, style="Subframe.TFrame")
        loadsave_frame.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        loadsave_frame.columnconfigure(1, weight=1)

        load_button = ttk.Button(loadsave_frame, text="Import JSON", command=self.import_json)
        load_button.grid(row=0, column=0, sticky="w", padx=5)

        export_button = ttk.Button(loadsave_frame, text="Export JSON", command=self.export_json)
        export_button.grid(row=0, column=1, sticky="w")

    #Helper functions for Content Box allowing the entry field to be stored as a string.
    def get_content_text(self):
        return self.entry_content_field.get("1.0", tk.END).rstrip('\n')

    def set_content_text(self, text):
        self.entry_content_field.delete("1.0", tk.END)
        self.entry_content_field.insert("1.0", text)

    #Further Helper Functions for the AND/OR Logic in the Selective Box.
    def get_sec_logic_value(self):
        value = self.sec_logic_var.get()
        return 0 if value == "AND" else 1

    def set_sec_logic_value(self, numeric_value):
        display_value = "AND" if numeric_value == 0 else "NOT"
        self.sec_logic_var.set(display_value)

    #Helper Functions for the Insert Order to ensure it is an int and loaded correctly.
    def get_insert_order(self):
        value = self.insert_order_var.get().strip()
        if not value:
            return 10

        try:
            return round(float(value))
        except ValueError:
            return 10

    def set_insert_order(self, value):
        self.insert_order_var.set(str(round(float(value))))

    #Helper functions for the Priority Variable to ensure it is an int and loaded correctly.
    def get_priority_order(self):
        value = self.priority_var.get().strip()
        if not value:
            return 10

        try:
            return round(float(value))
        except ValueError:
            return 10

    def set_priority_order(self, value):
        self.priority_var.set(str(round(float(value))))

    #Helper functions for the Probability to ensure it is an int and at max 100
    def get_probability(self):
        value = self.probability_var.get().strip()
        if not value:
            return 100

        try:
            numeric_value = round(float(value))
            return min(numeric_value, 100)
        except ValueError:
            return 100

    def set_probability(self, value):
        try:
            numeric_value = round(float(value))
            clamped_value = min(numeric_value, 100)
            self.probability_var.set(str(clamped_value))
        except (ValueError, TypeError):
            self.probability_var.set("100")

    #Helper Function to set the ID of an entry or grab the next available entry if one exists
    def get_next_entry_id(self):
        if not self.entries:
            return 1
        existing_ids = [int(uid) for uid in self.entries.keys()]
        return max(existing_ids) + 1 if existing_ids else 1

    #Helper Function to save the current entry or create a new one if no entry is selected
    def save_entry(self):
        selection = self.listbox.curselection()

        if selection:
            index = selection[0]
            listbox_text = self.listbox.get(index)
            entry_uid = listbox_text.split('(')[-1].rstrip(')')

            if entry_uid in self.entries:
                entry_data = {
                    "uid": int(entry_uid),
                    "key": [self.keywords_var.get()] if self.keywords_var.get() else [],
                    "keysecondary": [self.sec_keywords_var.get()] if self.sec_keywords_var.get() else [],
                    "comment": self.entry_var.get(),
                    "content": self.get_content_text(),
                    "constant": self.constant_var.get(),
                    "selective": self.sec_selective_var.get(),
                    "selectiveLogic": self.get_sec_logic_value(),
                    "position": 1,
                    "addMemo": True,
                    "excludeRecursion": True,
                    "probability": self.get_probability(),
                    "displayIndex": 1,
                    "useProbability": True,
                    "id": int(entry_uid),
                    "priority": self.get_priority_order(),
                    "insertion_order": self.get_insert_order(),
                    "enabled": self.enabled_var.get(),
                    "name": self.entry_var.get(),
                    "case_sensitive": self.case_var.get()
                }

                self.entries[entry_uid] = entry_data

                display_text = f"{self.entry_var.get()} ({entry_uid})"
                self.listbox.delete(index)
                self.listbox.insert(index, display_text)
                self.listbox.selection_set(index)

                print(f"Updated entry {entry_uid}: {entry_data['name']}")
            else:
                self.save_as_new_entry()
        else:
            self.save_as_new_entry()
            self.clear_form()

    def save_as_new_entry(self):
        new_id = self.get_next_entry_id()

        entry_data = {
            "uid": new_id,
            "key": [self.keywords_var.get()] if self.keywords_var.get() else [],
            "keysecondary": [self.sec_keywords_var.get()] if self.sec_keywords_var.get() else [],
            "comment": self.entry_var.get(),
            "content": self.get_content_text(),
            "constant": self.constant_var.get(),
            "selective": self.sec_selective_var.get(),
            "selectiveLogic": self.get_sec_logic_value(),
            "position": 1,
            "addMemo": True,
            "excludeRecursion": True,
            "probability": self.get_probability(),
            "displayIndex": 1,
            "useProbability": True,
            "id": new_id,
            "priority": self.get_priority_order(),
            "insertion_order": self.get_insert_order(),
            "enabled": self.enabled_var.get(),
            "name": self.entry_var.get(),
            "case_sensitive": self.case_var.get()
        }

        entry_uid = str(new_id)
        self.entries[entry_uid] = entry_data

        display_text = f"{self.entry_var.get()} ({new_id})"
        self.listbox.insert(tk.END, display_text)

        print(f"Saved new entry {new_id}: {entry_data['name']}")


    #Helper function to load entry on select
    def on_entry_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            listbox_text = self.listbox.get(index)
            entry_uid = listbox_text.split('(')[-1].rstrip(')')

            if entry_uid in self.entries:
                entry_data = self.entries[entry_uid]
                self.load_entry_data(entry_data)


    def load_entry_data(self, entry_data):
        self.entry_var.set(entry_data.get("comment", ""))

        keywords = entry_data.get("key", [])
        self.keywords_var.set(keywords[0] if keywords else "")

        sec_keywords = entry_data.get("keysecondary", [])
        self.sec_keywords_var.set(sec_keywords[0] if sec_keywords else "")

        self.set_content_text(entry_data.get("content", ""))

        self.set_insert_order(entry_data.get("insertion_order", 10))
        self.set_probability(entry_data.get("probability", 100))
        self.set_priority_order(entry_data.get("priority", 10))

        self.constant_var.set(entry_data.get("constant", False))
        self.sec_selective_var.set(entry_data.get("selective", False))
        self.enabled_var.set(entry_data.get("enabled", True))
        self.case_var.set(entry_data.get("case_sensitive", False))

        self.set_sec_logic_value(entry_data.get("selectiveLogic", 0))

    #Helper function to clear current form
    def clear_form(self):
        self.entry_var.set("")
        self.keywords_var.set("")
        self.sec_keywords_var.set("")
        self.set_content_text("")
        self.set_insert_order(10)
        self.constant_var.set(False)
        self.sec_selective_var.set(False)
        self.set_probability(100)
        self.set_priority_order(10)
        self.enabled_var.set(True)
        self.case_var.set(False)
        self.set_sec_logic_value(0)

    def new_entry(self):
        self.clear_form()
        self.listbox.selection_clear(0, tk.END)
        print("Ready for new entry")

    def set_book_title(self, title):
        self.book_var.set(title)

    def get_book_title(self):
        return self.book_var.get()

    def delete_entry(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an entry to delete.")
            return

        index = selection[0]
        listbox_text = self.listbox.get(index)
        entry_uid = listbox_text.split('(')[-1].rstrip(')')

        if entry_uid in self.entries:
            entry_name = self.entries[entry_uid].get("name", f"Entry {entry_uid}")
            result = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete entry '{entry_name}'?\n\nThis cannot be undone."
            )

            if result:
                del self.entries[entry_uid]

                self.listbox.delete(index)

                self.clear_form()

                print(f"Deleted entry {entry_uid}: {entry_name}")
        else:
            messagebox.showerror("Error", "Selected entry could not be found.")

    #Exports all entries into a JSON file within the LoreBooks sub-folder
    def export_json(self):
        if not self.entries:
            messagebox.showwarning("Warning", "No entries to export.")
            return

        book_name = self.book_var.get().strip()
        if not book_name:
            book_name = "lore_book"

        clean_book_name = re.sub(r'[<>:"/\\|?*]', '_', book_name)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Lore Book as JSON",
            initialdir=self.lore_books_dir,
            initialfile=f"{clean_book_name}.json"
        )

        if not file_path:
            return

        # Create the JSON structure
        json_data = {
            "name": self.book_var.get() or "Untitled Lore Book",
            "entries": {}
        }

        # Add all entries to the created JSON structure
        for uid, entry_data in self.entries.items():
            json_entry = {
                "uid": entry_data.get("uid", int(uid)),
                "key": entry_data.get("key", []),
                "keysecondary": entry_data.get("keysecondary", []),
                "comment": entry_data.get("comment", ""),
                "content": entry_data.get("content", ""),
                "constant": entry_data.get("constant", False),
                "selective": entry_data.get("selective", False),
                "selectiveLogic": entry_data.get("selectiveLogic", 0),
                "position": 1, #TODO Unsure what this entry does but in testing was always defaulted to 1
                "addMemo": True,
                "excludeRecursion": entry_data.get("excludeRecursion", True),
                "probability": entry_data.get("probability", 100),
                "displayIndex": 1, #TODO Unsure what this entry does but in testing was always defaulted to 1
                "useProbability": True,  # Always true as prob defaults to 100
                "id": entry_data.get("id", int(uid)),
                "priority": entry_data.get("priority", 10),
                "insertion_order": entry_data.get("insertion_order", 10),
                "enabled": entry_data.get("enabled", True),
                "name": entry_data.get("name", ""),
                "case_sensitive": entry_data.get("case_sensitive", False)
            }

            json_data["entries"][str(uid)] = json_entry

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            messagebox.showinfo("Success", f"Successfully exported {len(self.entries)} entries to {file_path}")
            print(f"Exported {len(self.entries)} entries to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON file:\n{str(e)}")

    # Will import ST and Chub lorebooks defaults to the LoreBooks sub-folder
    def import_json(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Lore Book from JSON",
            initialdir=self.lore_books_dir
        )

        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            # Clear current entries and listbox
            self.entries = {}
            self.listbox.delete(0, tk.END)

            # Extract book name (if available)
            book_name = json_data.get("name", "")
            if book_name:
                self.book_var.set(book_name)

            # Get entries dictionary
            entries_data = json_data.get("entries", {})

            imported_count = 0

            # Process each entry in the JSON
            for uid_str, entry_data in entries_data.items():
                uid = str(uid_str)

                # Handle case_sensitive/caseSensitive field (handle null values... thanks ST)
                case_sensitive_value = entry_data.get("case_sensitive", entry_data.get("caseSensitive", False))
                if case_sensitive_value is None:
                    case_sensitive_value = False

                new_entry = {
                    "uid": int(entry_data.get("uid", uid_str)),
                    "key": entry_data.get("key", []),
                    "keysecondary": entry_data.get("keysecondary", []),
                    "comment": entry_data.get("comment", ""),
                    "content": entry_data.get("content", ""),
                    "constant": entry_data.get("constant", False),
                    "selective": entry_data.get("selective", False),
                    "selectiveLogic": entry_data.get("selectiveLogic", 0),
                    "position": entry_data.get("position", 1),
                    "addMemo": entry_data.get("addMemo", True),
                    "excludeRecursion": entry_data.get("excludeRecursion", True),
                    "probability": entry_data.get("probability", 100),
                    "displayIndex": entry_data.get("displayIndex", 1),
                    "useProbability": entry_data.get("useProbability", True),
                    "id": entry_data.get("id", int(entry_data.get("uid", uid_str))),
                    "priority": entry_data.get("priority", 10),
                    "insertion_order": entry_data.get("insertion_order", 10),
                    "enabled": entry_data.get("enabled", True),
                    "name": entry_data.get("name", entry_data.get("comment", "")),
                    "case_sensitive": case_sensitive_value  # Use the handled value
                }

                # Handle Silly Tavern's "disable" field (opposite of "enabled") Why ST...
                if "disable" in entry_data:
                    new_entry["enabled"] = not entry_data["disable"]

                # Store the entry
                self.entries[uid] = new_entry

                # Add to listbox
                display_name = new_entry["name"] or f"Entry {uid}"
                display_text = f"{display_name} ({uid})"
                self.listbox.insert(tk.END, display_text)

                imported_count += 1

            messagebox.showinfo("Success", f"Successfully imported {imported_count} entries from {file_path}")
            print(f"Imported {imported_count} entries from {file_path}")

        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON file format.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import JSON file:\n{str(e)}")



def main():
    root = tk.Tk()
    app = LoreBroker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
