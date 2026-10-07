import os

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
    
    # If the text file does not exist, initialize it with your exact dataset
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
                    
                    # Store in dictionary using item_id as the key
                    inventory[item_id] = BookItem(item_id, name, price, stock, location, course)
    except Exception as e:
        print(f"[!] Error reading database file: {e}")
    
    return inventory


def save_inventory(inventory):
    """Saves the current inventory dictionary back to the text file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for item in inventory.values():
                file.write(item.to_file_string())
        print(">> Inventory database successfully saved to 'inventory.txt'.")
    except Exception as e:
        print(f"[!] Error saving inventory: {e}")


# --- USER INTERFACE FUNCTIONS ---
def display_all_items(inventory):
    """Displays all items in tabular format."""
    print("\n" + "="*80)
    print(f"{'ID':<5} | {'Item Description':<30} | {'Price (PHP)':<11} | {'Status':<22}")
    print("="*80)
    if not inventory:
        print("No items found in system database.")
    else:
        for item in inventory.values():
            print(f"{item.item_id:<5} | {item.name:<30} | ₱{item.price:<10.2f} | {item.get_status():<22}")
    print("="*80)


def search_item(inventory):
    """Allows students/staff to quickly query item stock without queuing."""
    query = input("\nEnter Item ID, Description, or Course Tag to search: ").strip().lower()
    found = False
    
    print("\n--- Search Results ---")
    for item in inventory.values():
        if (query in item.item_id.lower() or 
            query in item.name.lower() or 
            query in getattr(item, 'course_code', '').lower()):
            
            print(f"\n[+] Match Found:")
            print(f"    Item ID:     {item.item_id}")
            print(f"    Description: {item.name}")
            print(f"    Price:       ₱{item.price:.2f}")
            print(f"    Course Tag:  {getattr(item, 'course_code', 'GEN')}")
            print(f"    Status:      {item.get_status()}")
            print(f"    Location:    {item.location}")
            found = True
            
    if not found:
        print("[-] No matching items found in the Mapúa Bookstore records.")


def update_daily_sales(inventory):
    """Admin feature: Record daily sales and deduct stock levels."""
    item_id = input("\nEnter Item ID to update stock (e.g., 001): ").strip()
    
    if item_id in inventory:
        item = inventory[item_id]
        print(f"\nSelected: {item.name}")
        print(f"Current Stock: {item.stock} units")
        
        try:
            sold_qty = int(input("Enter quantity sold today: "))
            if sold_qty < 0:
                print("[!] Error: Quantity sold cannot be negative.")
            elif sold_qty > item.stock:
                print(f"[!] Warning: Sales quantity ({sold_qty}) exceeds available stock ({item.stock}).")
            else:
                item.stock -= sold_qty
                print(f"[✓] Success! Updated remaining stock: {item.stock}")
                save_inventory(inventory)
        except ValueError:
            print("[!] Invalid input. Please enter a valid whole number.")
    else:
        print(f"[!] Item ID '{item_id}' not found in inventory.")


# --- MAIN PROGRAM LOOP ---
def main():
    inventory = load_inventory()
    
    while True:
        print("\n" + "="*48)
        print("   Mapúa Bookstore Inventory & Inquiry System   ")
        print("="*48)
        print("1. View Full Inventory Stock Catalog")
        print("2. Search Item Availability")
        print("3. Log Daily Sales/Update Stock (Admin Only)")
        print("4. Exit System")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            display_all_items(inventory)
        elif choice == '2':
            search_item(inventory)
        elif choice == '3':
            update_daily_sales(inventory)
        elif choice == '4':
            print("\nThank you for using CardInq. Have a great day!")
            break
        else:
            print("\n[!] Invalid selection. Please enter a choice between 1 and 4.")


if __name__ == "__main__":
    main()
