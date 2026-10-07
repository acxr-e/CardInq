import os
import streamlit as st

# --- CLASS DEFINITIONS (OOP & Inheritance) ---
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
    """Subclass inheriting from Item for course-tagged entries (Inheritance)."""
    def __init__(self, item_id, name, price, stock, location="Main Bookstore", course_code="GEN"):
        super().__init__(item_id, name, price, stock, location)
        self.course_code = course_code

    def to_file_string(self):
        return f"{self.item_id},{self.name},{self.price},{self.stock},{self.location},{self.course_code}\n"


# --- FILE HANDLING & DATA FUNCTIONS ---
FILE_NAME = "inventory.txt"

DEFAULT_DATA = [
    "001,Drawing Paper 12'x 18',18.0,200,Main Bookstore,DRAW10W\n",
    "002,Drawing Paper 12'x 9',10.0,300,Main Bookstore,DRAW10W\n",
    "003,Drawing Paper Case,50.0,90,Main Bookstore,DRAW10W\n",
    "004,PE Shirt Uniform (Small),450.0,0,Main Bookstore,PATHFIT\n",
    "005,PE Pants Uniform (Medium),500.0,0,Main Bookstore,PATHFIT\n",
    "006,Mapua Yellow Pad (100s),65.0,120,Main Bookstore,GEN\n",
    "007,Booklet,80.0,15,Main Bookstore,DRAW10W\n"
]

def load_inventory():
    """Reads inventory data into session state for cross-environment compatibility."""
    if "inventory" in st.session_state:
        return st.session_state["inventory"]

    inventory = {}
    lines = []

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except Exception:
            lines = DEFAULT_DATA
    else:
        lines = DEFAULT_DATA

    for line in lines:
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

    st.session_state["inventory"] = inventory
    return inventory


def save_inventory(inventory):
    """Saves inventory state in session memory and attempts file persistence if allowed."""
    st.session_state["inventory"] = inventory
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for item in inventory.values():
                file.write(item.to_file_string())
        st.toast("Inventory database updated successfully!", icon="✅")
    except Exception:
        st.toast("Updated inventory state in session memory!", icon="ℹ️")


# --- STREAMLIT USER INTERFACE ---
def main():
    st.set_page_config(
        page_title="CardInq | Mapúa Bookstore Portal",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # --- SAFE STYLING FOR CLOUD HOSTING ---
    st.markdown("""
        <style>
            /* Header Banner */
            .main-header {
                background: linear-gradient(135deg, #800000 0%, #B22222 100%);
                padding: 1.8rem 2rem;
                border-radius: 12px;
                color: white;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            }
            .main-header h1 {
                color: #FFFFFF !important;
                font-weight: 700;
                margin: 0;
                font-size: 2.2rem;
            }
            .main-header p {
                color: #FFD700 !important;
                margin-top: 0.3rem;
                font-weight: 500;
                font-size: 1.05rem;
            }

            /* Sidebar Parent Background */
             section[data-testid="stSidebar"] {
                 background: linear-gradient(135deg, #800000 0%, #B22222 100%) !important;
                 border-right: 1px solid #EAEAEA;
             }
            
             /* Default state for all sidebar text elements */
             section[data-testid="stSidebar"] h1,
             section[data-testid="stSidebar"] h2,
             section[data-testid="stSidebar"] h3,
             section[data-testid="stSidebar"] label,
             section[data-testid="stSidebar"] span,
             section[data-testid="stSidebar"] p { 
                 color: #FFFFFF !important;
             }
            
             /* Header Text Label above the options ("Select:") */
             section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
                 color: #F2A900 !important;
                 font-weight: 600;
             }
            
             /* ACTIVE State: Selected option text and radio button icon */
             section[data-testid="stSidebar"] [data-checked="true"] {
             background-color: #F2A900 !important;
             border-color: #F2A900 !important;
             }
             section[data-testid="stSidebar"] [data-checked="true"] ~ div p {
                 color: #F2A900 !important;
                 font-weight: 700 !important;
             }
            
             /* HOVER State: Unselected items on hover */
             section[data-testid="stSidebar"] label:hover [data-checked="false"] {
                 border-color: #F2A900 !important;
             }
             section[data-testid="stSidebar"] label:hover p {
                 color: #F2A900 !important;
             }

            /* Metric Card Custom Accent */
            [data-testid="stMetric"] {
                background-color: #F8F9FA;
                border: 1px solid #E9ECEF;
                padding: 1rem 1.2rem;
                border-radius: 10px;
                border-left: 5px solid #800000;
            }

            /* Status Pill Badges */
            .status-in {
                background-color: #D4EDDA;
                color: #155724;
                padding: 3px 10px;
                border-radius: 12px;
                font-weight: 600;
            }
            .status-out {
                background-color: #DC3545;
                color: #FFFFFF;
                padding: 3px 10px;
                border-radius: 12px;
                font-weight: 600;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- HEADER BANNER ---
    st.markdown("""
        <div class="main-header">
            <h1>📚 Mapúa University Bookstore</h1>
            <p>CardInq: Central Inventory Inquiry & Management Portal</p>
        </div>
    """, unsafe_allow_html=True)

    inventory = load_inventory()

    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("Navigation Menu")
    menu_choice = st.sidebar.radio(
        "Select Portal Module:",
        [
            "Inventory Stock Catalog",
            "Search Item Availability",
            "Log Daily Sales/Update Stock (Admin Only)"
        ]
    )
    
    st.sidebar.divider()
    st.sidebar.caption("Mapúa University Bookstore System\n\nPowered by Python & Streamlit")

    # --- TOP METRIC OVERVIEW ---
    total_items = len(inventory)
    in_stock_items = sum(1 for item in inventory.values() if item.stock > 0)
    out_of_stock_items = sum(1 for item in inventory.values() if item.stock == 0)

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Cataloged Items", total_items, help="Total number of unique items registered in the database")
    m2.metric("Available In Stock", in_stock_items, help="Items currently available for immediate purchase")
    m3.metric("Out of Stock Alert", out_of_stock_items, delta_color="inverse", help="Items requiring immediate inventory restock")
    
    st.divider()

    # --- MODULE 1: CATALOG VIEW ---
    if menu_choice == "Inventory Stock Catalog":
        st.header("📋 Full Inventory Stock Catalog")
        st.caption("Real-time Availability of All Bookstore Supplies.")

        table_data = []
        for item in inventory.values():
            table_data.append({
                "Item ID": item.item_id,
                "Description": item.name,
                "Price (PHP)": f"₱{item.price:.2f}",
                "Stock Level": item.stock,
                "Course Tag": getattr(item, 'course_code', 'GEN'),
                "Status": "🟢 IN STOCK" if item.stock > 0 else "🔴 OUT OF STOCK",
                "Available Location": item.location
            })

        st.dataframe(
            table_data,
            use_container_width=True,
            column_config={
                "Stock Level": st.column_config.NumberColumn("Stock Level", format="%d units"),
                "Price (PHP)": st.column_config.TextColumn("Price (PHP)"),
            }
        )

    # --- MODULE 2: SEARCH INQUIRY ---
    elif menu_choice == "Search Item Availability":
        st.header("🔍 Quick Item Availability Inquiry")
        st.caption("Search by Item ID, Item Description, or Course Tag).")

        search_query = st.text_input("Search catalog:", placeholder="Enter item name, ID, or course code...").strip().lower()

        if search_query:
            results = []
            for item in inventory.values():
                if (search_query in item.item_id.lower() or 
                    search_query in item.name.lower() or 
                    search_query in getattr(item, 'course_code', '').lower()):
                    results.append(item)

            if results:
                st.success(f"Found {len(results)} matching item(s):")
                for item in results:
                    status_badge = f'<span class="status-in">IN STOCK</span>' if item.stock > 0 else f'<span class="status-out">OUT OF STOCK</span>'
                    
                    with st.expander(f"📦 [{item.item_id}] {item.name} — Stock: {item.stock}"):
                        st.markdown(f"### {item.name} &nbsp; {status_badge}", unsafe_allow_html=True)
                        st.write("")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Unit Price", f"₱{item.price:.2f}")
                        c2.metric("Remaining Stock", f"{item.stock} units")
                        c3.metric("Course Tag", getattr(item, 'course_code', 'GEN'))
                        st.info(f"📍 **Available Location:** {item.location}")
            else:
                st.warning("No matching items found in the Mapúa Bookstore inventory.")

    # --- MODULE 3: ADMIN SALES & STOCK UPDATE ---
    elif menu_choice == "Log Daily Sales/Update Stock (Admin Only)":
        st.header("⚙️ Admin Sales Logging & Stock Adjustment")
        st.caption("Deduct daily sales quantities directly from the central database.")

        item_options = {f"[{item.item_id}] {item.name} (Current Stock: {item.stock})": item.item_id for item in inventory.values()}
        selected_display = st.selectbox("Select Item to Update:", list(item_options.keys()))

        if selected_display:
            selected_id = item_options[selected_display]
            selected_item = inventory[selected_id]

            st.info(f"**Selected Item:** {selected_item.name} &nbsp;|&nbsp; **Current Available Stock:** {selected_item.stock} units")

            with st.form("sales_update_form", border=True):
                st.subheader("Record Daily Transaction")
                sold_qty = st.number_input(
                    "Enter quantity sold today:",
                    min_value=0,
                    max_value=max(0, selected_item.stock),
                    value=0,
                    step=1,
                    help="Quantity sold will be deducted from current stock."
                )
                
                submit_button = st.form_submit_button("Confirm Sales & Deduct Stock", type="primary")

                if submit_button:
                    if sold_qty > selected_item.stock:
                        st.error(f"Cannot sell {sold_qty} units. Only {selected_item.stock} in stock.")
                    elif sold_qty <= 0:
                        st.warning("Please enter a quantity greater than 0.")
                    else:
                        selected_item.stock -= sold_qty
                        save_inventory(inventory)
                        st.success(f"Successfully deducted {sold_qty} unit(s). New stock for {selected_item.name}: {selected_item.stock}")
                        st.rerun()

if __name__ == "__main__":
    main()
