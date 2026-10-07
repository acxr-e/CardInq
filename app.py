import os
import streamlit as st

# --- CLASS DEFINITIONS (OOP & Bonus: Inheritance) ---
class Item:
    """Base Class representing a general bookstore item."""
    def __init__(self, item_id, name, price, stock, location="Main Bookstore"):
        self.item_id = item_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.location = location

    def to_file_string(self):
        """Converts object details into a formatted comma-separated string for file storage."""
        return f"{self.item_id},{self.name},{self.price},{self.stock},{self.location}\n"

    def get_status(self):
        """Returns availability status string."""
        if self.stock > 0:
            return f"IN STOCK ({self.stock} available)"
        else:
            return "OUT OF STOCK"


class BookItem(Item):
    """Subclass inheriting from Item for course-tagged entries (Bonus Feature: Inheritance)."""
    def __init__(self, item_id, name, price, stock, location="Main Bookstore", course_code="GEN"):
        super().__init__(item_id, name, price, stock, location)
        self.course_code = course_code

    def to_file_string(self):
        return f"{self.item_id},{self.name},{self.price},{self.stock},{self.location},{self.course_code}\n"


# --- FILE HANDLING & DATA FUNCTIONS ---
FILE_NAME = "inventory.txt"

def load_inventory():
    """Reads inventory data from text file into a dictionary."""
    inventory = {}
    
    # If text file does not exist, initialize with exact Mapúa dataset
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as f:
            f.write("001,Drawing Paper 12'x 18',18.0,200,Main Bookstore,DRAW10W\n")
            f.write("002,Drawing Paper 12'x 9',10.0,300,Main Bookstore,DRAW10W\n")
            f.write("003,Drawing Paper Case,50.0,90,Main Bookstore,DRAW10W\n")
            f.write("004,PE Shirt Uniform (Small),450.0,0,Main Bookstore,PATHFIT\n")
            f.write("005,PE Pants Uniform (Medium),500.0,0,Main Bookstore,PATHFIT\n")
            f.write("006,Mapua Yellow Pad (100s),65.0,120,Main Bookstore,GEN\n")
            f.write("007,Booklet,80.0,15,Main Bookstore,DRAW10W\n")

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                line_data = line.strip()
                if not line_data:
                    continue
                
                data = line_data.split(",")
                if len(data) >= 5:
                    item_id = data[0].strip()
                    name = data[1].strip()
                    price = float(data[2].strip())
                    stock = int(data[3].strip())
                    location = data[4].strip()
                    course = data[5].strip() if len(data) == 6 else "GEN"
                    
                    inventory[item_id] = BookItem(item_id, name, price, stock, location, course)
    except Exception as e:
        st.error(f"Error reading database file: {e}")
    
    return inventory


def save_inventory(inventory):
    """Saves the current inventory dictionary back to the text file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for item in inventory.values():
                file.write(item.to_file_string())
        st.toast("Inventory database updated successfully!", icon="✅")
    except Exception as e:
        st.error(f"Error saving inventory: {e}")


# --- STREAMLIT USER INTERFACE ---
def main():
    st.set_page_config(
        page_title="CardInq - Mapúa Bookstore System",
        page_icon="📚",
        layout="wide"
    )

    st.title("📚 Mapúa University Bookstore System")
    st.subheader("CardInq: Inventory Inquiry & Management Portal")
    st.divider()

    # Load inventory data into session state or refresh
    inventory = load_inventory()

    # Sidebar Navigation
    st.sidebar.header("Navigation")
    menu_choice = st.sidebar.radio(
        "Select Portal Module:",
        [
            "1. View Full Stock Catalog",
            "2. Search Item Availability",
            "3. Log Daily Sales / Update Stock (Admin)",
            "4. System Information"
        ]
    )

    # Top Metric Overview
    total_items = len(inventory)
    in_stock_items = sum(1 for item in inventory.values() if item.stock > 0)
    out_of_stock_items = sum(1 for item in inventory.values() if item.stock == 0)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Cataloged Items", total_items)
    m2.metric("Available In Stock", in_stock_items)
    m3.metric("Out of Stock Alert", out_of_stock_items, delta_color="inverse")
    st.divider()

    # --- MODULE 1: CATALOG VIEW ---
    if menu_choice == "1. View Full Stock Catalog":
        st.header("📋 Full Inventory Stock Catalog")
        st