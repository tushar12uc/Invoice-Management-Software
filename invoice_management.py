import streamlit as st
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import base64

# Streamlit App Configuration
st.set_page_config(
    page_title="Invoice Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved styling
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #f4f6f9;
        color: black;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #343a40 !important;
        color: #c2c7d0;
    }

    /* Button styles */
    .stButton > button {
        background-color: #007bff; /* Primary color */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s;
    }

    .stButton > button:hover {
        background-color: #0056b3; /* Darker shade on hover */
    }

    /* Card styles */
    .card {
        background: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,.1);
        margin-bottom: 20px;
        padding: 20px;
        transition: transform 0.2s;
    }

    .card:hover {
        transform: scale(1.02);
    }

    /* Table styles */
    .dataframe {
        border-collapse: collapse;
        width: 100%;
    }

    .dataframe th, .dataframe td {
        border: 1px solid #ddd;
        padding: 8px;
    }

    .dataframe tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    .dataframe tr:hover {
        background-color: #ddd;
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
        color: #343a40;
    }
    </style>
""", unsafe_allow_html=True)


# Add custom CSS for background image
def set_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Set the background image
set_background_image("background.jpg")

# Add login authentication
def authenticate(username, password):
    return username == "tushar12uc" and password == "mehek2009@#"

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'password' not in st.session_state:
    st.session_state.password = ''

import streamlit as st

# Login Page
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Center the login box with a border and padding
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Title with a centered style
        st.markdown(
            "<h3 style='text-align: center; color: #4A90E2;'>🔐 Invoice Management System</h3>",
            unsafe_allow_html=True,
        )


        # Tabs for "Sign In" and "Sign Up"
        tabs = st.tabs(["Sign In", "Sign Up"])

        with tabs[0]:  # Default to "Sign In"
            with st.form("login_form", clear_on_submit=False):
                # Input fields with styling
                username = st.text_input("👤 Username", placeholder="Enter your Username", label_visibility="collapsed")
                password = st.text_input("🔑 Password", type="password", placeholder="Enter your password", label_visibility="collapsed")

                # Remember me checkbox and forgot password link
                col4, col5 = st.columns([1, 1])
                with col4:
                    st.checkbox("Remember me")
                with col5:
                    st.markdown("<a style='font-size: 12px; color: #4A90E2;' href='#'>Forgot Password?</a>", unsafe_allow_html=True)

                # Centered login button with a border and hover effect
                submit_button = st.form_submit_button("LOGIN", type="primary")
                
                # Submit button interaction
                if submit_button:
                    if authenticate(username, password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.password = password
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password. Please try again.")

        # Close the bordered container
        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# Logout Button
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ''
    st.session_state.password = ''


# Dashboard Layout (After Login)
if st.session_state.logged_in:
    # Top Navigation Bar
    st.markdown("""
        <div class="top-nav">
            <h3 style="margin:0;">Invoice Management System</h3>
            <div style="display:flex; align-items:center; gap:15px;">
                <span>Welcome, {username}</span>
                <a href="#" onclick="alert('Logout functionality goes here')" style="color:white;">Logout</a>
            </div>
        </div>
    """.format(username=st.session_state.username), unsafe_allow_html=True)
    
# Rest of the application (only accessible after login)
# Add logout button to sidebar
st.sidebar.title("Editors Chamber")
if st.sidebar.button("Logout"):
    logout()
    st.rerun()

# File paths for data storage
CUSTOMERS_FILE = "customers.csv"
PRODUCTS_FILE = "products.csv"
INVOICES_FILE = "invoices.csv"

# Load or initialize data
def load_data(file, default_columns):
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=default_columns)

# Save data to CSV
def save_data(df, file):
    df.to_csv(file, index=False)

# Initialize data
customers = load_data(CUSTOMERS_FILE, ["customer_id", "customer_name", "address", "mobile", "email"])
products = load_data(PRODUCTS_FILE, ["product_id", "product_name", "description", "price", "stock"])
invoices = load_data(INVOICES_FILE, ["invoice_id", "customer_id", "product_ids", "quantities", "total_amount", "payment_status"])

# Generate PDF Invoice
def generate_invoice(customer_id, product_ids, quantities, total_amount):
    customer = customers[customers['customer_id'] == customer_id].iloc[0]
    selected_products = products[products['product_id'].isin(product_ids)]

    pdf = FPDF()
    pdf.add_page()

    # Logo
    if os.path.exists("company_logo.png"):
        pdf.image("company_logo.png", x=160, y=8, w=33)

    # Title and Company Details
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="INVOICE", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt="Editors Chamber.", ln=True, align='L')
    pdf.cell(200, 10, txt="Udaipur, India", ln=True, align='L')
    pdf.cell(200, 10, txt="Pincode: 313324", ln=True, align='L')
    pdf.cell(200, 10, txt="Email: tushar@editorschamber.in", ln=True, align='L')
    pdf.ln(10)

    # Customer Details
    pdf.cell(200, 10, txt="Customer Details:-------------", ln=True)
    pdf.cell(200, 10, txt=f"Customer: {customer['customer_name']}", ln=True)
    pdf.cell(200, 10, txt=f"Address: {customer['address']}", ln=True)
    pdf.cell(200, 10, txt=f"Mobile: {customer['mobile']}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {customer['email']}", ln=True)
    pdf.ln(10)

    # Table Header
    pdf.cell(60, 10, "Product", 1)
    pdf.cell(60, 10, "Description", 1)
    pdf.cell(20, 10, "Qty", 1)
    pdf.cell(30, 10, "Unit Price", 1)
    pdf.cell(30, 10, "Total", 1)
    pdf.ln()

    total = 0
    for i, product in selected_products.iterrows():
        qty = quantities[product_ids.index(product['product_id'])]
        line_total = product['price'] * qty
        total += line_total
        pdf.cell(60, 10, product['product_name'], 1)
        pdf.cell(60, 10, product['description'], 1)
        pdf.cell(20, 10, str(qty), 1)
        pdf.cell(30, 10, f"${product['price']:.2f}", 1)
        pdf.cell(30, 10, f"${line_total:.2f}", 1)
        pdf.ln()

    pdf.cell(170, 10, "", 0)
    pdf.cell(30, 10, f"Total: ${total_amount:.2f}", 1)

    filename = f"invoice_{customer_id}_{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# Sidebar Menu
st.sidebar.title("Dashboard")
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Customer Management", "Product Management", "Invoice Management","Admin","Profile","Terms and Conditions"]
)

# Home Page
if menu == "Home":
     st.title("User Dashboard")
     # Create a row layout
     col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# Create a box for User Registrations
     with col1:
      st.markdown(
        """
        <div class="card">
            <h3 style="margin: 0;">09</h3>
            <p>User Registrations</p>
            <button style="padding: 8px 12px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">More info</button>
        </div>
        """,
        unsafe_allow_html=True
    )

# Create a second box for Pending Payments
     with col2:
      st.markdown(
        """
        <div class="card">
            <h3 style="margin: 0;">10</h3>
            <p>Pending Payments</p>
            <button style="padding: 8px 12px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer;">More info</button>
        </div>
        """,
        unsafe_allow_html=True
    )

# Create a third box for Products
     with col3:
      st.markdown(
        """
        <div class="card">
            <h3 style="margin: 0;">15</h3>
            <p>Products</p>
            <button style="padding: 8px 12px; background-color: #ff5722; color: white; border: none; border-radius: 5px; cursor: pointer;">More info</button>
        </div>
        """,
        unsafe_allow_html=True
    )

# Create a fourth box for Customers
     with col4:
      st.markdown(
        """
        <div class="card">
            <h3 style="margin: 0;">25</h3>
            <p>Customers</p>
            <button style="padding: 8px 12px; background-color: #6c757d; color: white; border: none; border-radius: 5px; cursor: pointer;">More info</button>
        </div>
        """,
        unsafe_allow_html=True
    )
      # Define the data for the graph and table
      columns = ["Registers", "Payments", "Products", "Customers"]
      data = {
    "Columns": columns,
    "Values": [9, 10, 15, 12],
}
     dataframe = pd.DataFrame(data)
    # Define the data for the sales graph
     sales_years = [2020, 2021, 2022, 2023, 2024]
     sales_values = [1000, 1500, 2000, 2500, 3000]

     # Define the data for the donut chart
     donut_labels = ["Product A", "Product B", "Product C", "Product D"]
     donut_sizes = [30, 25, 20, 25]

# Layout with two columns
     col1, col2 = st.columns([3, 2])

# Left side: Graph
     with col1:
      st.write("### Overview Graph")
      fig, ax = plt.subplots(figsize=(4, 3))  # Adjust graph size
      ax.bar(data["Columns"], data["Values"], color=["blue", "green", "orange", "red"])
      ax.set_xlabel("Categories")
      ax.set_ylabel("Values")
      ax.set_title("Column Data Overview")
      st.pyplot(fig)

      # Right side: Sales Graph
     with col2:
      st.write("### Sales Over Time")
      fig, ax = plt.subplots(figsize=(4, 3))  # Adjust graph size
      ax.plot(sales_years, sales_values, marker='o', linestyle='-', color='purple')
      ax.set_xlabel("Year")
      ax.set_ylabel("Sales")
      ax.set_title("Sales from 2020 to 2024")
      st.pyplot(fig)

      # Donut Chart
      st.write("### Product Distribution")
      fig, ax = plt.subplots(figsize=(4, 3))
      wedges, texts, autotexts = ax.pie(donut_sizes, labels=donut_labels, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
      ax.set_title("Product Sales Distribution")
      st.pyplot(fig)





# Customer Management
elif menu == "Customer Management":
    st.markdown("<h2 style='color: #4A90E2;'>📋 Customer Management</h2>", unsafe_allow_html=True)
    create_or_manage = st.radio("🛠 Choose Action", ["➕ Create", "🔧 Manage"], horizontal=True)

    if create_or_manage == "➕ Create":
        st.markdown("### 🆕 Add New Customer")

        # Two-column layout for better alignment and clearer headings
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='color: #4A90E2;'>👤 Customer Name</h4>", unsafe_allow_html=True)
            new_name = st.text_input("Customer Name")
            st.markdown("<h4 style='color: #4A90E2;'>📞 Mobile</h4>", unsafe_allow_html=True)
            new_mobile = st.text_input("Mobile")

        with col2:
            st.markdown("<h4 style='color: #4A90E2;'>🏠 Address</h4>", unsafe_allow_html=True)
            new_address = st.text_input("Address")
            st.markdown("<h4 style='color: #4A90E2;'>✉️ Email</h4>", unsafe_allow_html=True)
            new_email = st.text_input("Email")

        add_customer = st.button("✅ Add Customer", use_container_width=True)

        if add_customer:
            new_id = customers['customer_id'].max() + 1 if not customers.empty else 1
            new_customer = pd.DataFrame([[new_id, new_name, new_address, new_mobile, new_email]],
                                        columns=["customer_id", "customer_name", "address", "mobile", "email"])
            customers = pd.concat([customers, new_customer], ignore_index=True)
            save_data(customers, CUSTOMERS_FILE)
            st.success("🎉 Customer added successfully!")

    elif create_or_manage == "🔧 Manage":
        st.markdown("### 🔍 Search & Manage Customers")

        # Search Bar with Icon
        search_query = st.text_input("🔎 Search Customers by Name, Email, or Mobile")
        if search_query:
            filtered_customers = customers[
                (customers['customer_name'].str.contains(search_query, case=False)) |
                (customers['email'].str.contains(search_query, case=False)) |
                (customers['mobile'].str.contains(search_query, case=False))
            ]
            st.dataframe(filtered_customers, use_container_width=True)
        else:
            st.dataframe(customers, use_container_width=True)

        # Edit/Delete Section
        st.markdown("### ✏️ Edit or 🗑️ Delete Customer")
        customer_id_to_edit = st.number_input("Enter Customer ID to Edit/Delete", min_value=1, step=1)

        if customer_id_to_edit:
            customer_to_edit = customers[customers['customer_id'] == customer_id_to_edit]
            if not customer_to_edit.empty:
                st.markdown("#### 📌 Current Details")
                st.dataframe(customer_to_edit)

                # Two-column layout for cleaner inputs with clearer headings
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<h4 style='color: #4A90E2;'>👤 New Customer Name</h4>", unsafe_allow_html=True)
                    new_name = st.text_input("New Customer Name", value=customer_to_edit.iloc[0]['customer_name'])
                    st.markdown("<h4 style='color: #4A90E2;'>📞 New Mobile</h4>", unsafe_allow_html=True)
                    new_mobile = st.text_input("New Mobile", value=customer_to_edit.iloc[0]['mobile'])

                with col2:
                    st.markdown("<h4 style='color: #4A90E2;'>🏠 New Address</h4>", unsafe_allow_html=True)
                    new_address = st.text_input("New Address", value=customer_to_edit.iloc[0]['address'])
                    st.markdown("<h4 style='color: #4A90E2;'>✉️ New Email</h4>", unsafe_allow_html=True)
                    new_email = st.text_input("New Email", value=customer_to_edit.iloc[0]['email'])

                update_col, delete_col = st.columns(2)
                with update_col:
                    if st.button("💾 Update Customer", use_container_width=True):
                        customers.loc[customers['customer_id'] == customer_id_to_edit, 'customer_name'] = new_name
                        customers.loc[customers['customer_id'] == customer_id_to_edit, 'address'] = new_address
                        customers.loc[customers['customer_id'] == customer_id_to_edit, 'mobile'] = new_mobile
                        customers.loc[customers['customer_id'] == customer_id_to_edit, 'email'] = new_email
                        save_data(customers, CUSTOMERS_FILE)
                        st.success("✅ Customer updated successfully!")

                with delete_col:
                    if st.button("🗑️ Delete Customer", use_container_width=True):
                        customers = customers[customers['customer_id'] != customer_id_to_edit]
                        save_data(customers, CUSTOMERS_FILE)
                        st.success("🚮 Customer deleted successfully!")

            else:
                st.error("⚠️ Customer ID not found!")


# Product Management
elif menu == "Product Management":
    st.markdown("<h2 style='color: #FF7F50;'>🛒 Product Management</h2>", unsafe_allow_html=True)
    create_or_manage = st.radio("🛠 Choose Action", ["➕ Create", "📦 Manage"], horizontal=True)

    if create_or_manage == "➕ Create":
        st.markdown("### 🆕 Add New Product")

        # Two-column layout for structured input fields
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏷️ Product Name")
            new_product_name = st.text_input("Enter product name")
            st.markdown("#### 💰 Price")
            new_price = st.number_input("Enter price", min_value=0.0)

        with col2:
            st.markdown("#### 📝 Description")
            new_description = st.text_input("Enter description")
            st.markdown("#### 📦 Stock Quantity")
            new_stock = st.number_input("Enter stock quantity", min_value=0)

        add_product = st.button("✅ Add Product", use_container_width=True)

        if add_product:
            new_id = products['product_id'].max() + 1 if not products.empty else 101
            new_product = pd.DataFrame([[new_id, new_product_name, new_description, new_price, new_stock]],
                                       columns=["product_id", "product_name", "description", "price", "stock"])
            products = pd.concat([products, new_product], ignore_index=True)
            save_data(products, PRODUCTS_FILE)
            st.success("🎉 Product added successfully!")

    elif create_or_manage == "📦 Manage":
        st.markdown("### 🔍 Search & Manage Products")

        # Search Bar
        search_query = st.text_input("🔎 Search Products by Name or Description")
        if search_query:
            filtered_products = products[
                (products['product_name'].str.contains(search_query, case=False)) |
                (products['description'].str.contains(search_query, case=False))
            ]
            st.dataframe(filtered_products, use_container_width=True)
        else:
            st.dataframe(products, use_container_width=True)

        # Edit/Delete Section
        st.markdown("### ✏️ Edit or 🗑️ Delete Product")
        product_id_to_edit = st.number_input("Enter Product ID to Edit/Delete", min_value=101, step=1)

        if product_id_to_edit:
            product_to_edit = products[products['product_id'] == product_id_to_edit]
            if not product_to_edit.empty:
                st.markdown("#### 📌 Current Details")
                st.dataframe(product_to_edit)

                # Two-column layout for cleaner input fields
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🏷️ New Product Name")
                    new_name = st.text_input("New product name", value=product_to_edit.iloc[0]['product_name'])
                    st.markdown("#### 💰 New Price")
                    new_price = st.number_input("New price", value=product_to_edit.iloc[0]['price'])

                with col2:
                    st.markdown("#### 📝 New Description")
                    new_description = st.text_input("New description", value=product_to_edit.iloc[0]['description'])
                    st.markdown("#### 📦 New Stock Quantity")
                    new_stock = st.number_input("New stock quantity", value=product_to_edit.iloc[0]['stock'])

                update_col, delete_col = st.columns(2)
                with update_col:
                    if st.button("💾 Update Product", use_container_width=True):
                        products.loc[products['product_id'] == product_id_to_edit, 'product_name'] = new_name
                        products.loc[products['product_id'] == product_id_to_edit, 'description'] = new_description
                        products.loc[products['product_id'] == product_id_to_edit, 'price'] = new_price
                        products.loc[products['product_id'] == product_id_to_edit, 'stock'] = new_stock
                        save_data(products, PRODUCTS_FILE)
                        st.success("✅ Product updated successfully!")

                with delete_col:
                    if st.button("🗑️ Delete Product", use_container_width=True):
                        products = products[products['product_id'] != product_id_to_edit]
                        save_data(products, PRODUCTS_FILE)
                        st.success("🚮 Product deleted successfully!")

            else:
                st.error("⚠️ Product ID not found!")

# Invoice Management
elif menu == "Invoice Management":
    st.markdown("<h2 style='color: #4CAF50;'>📜 Invoice Management</h2>", unsafe_allow_html=True)
    create_or_manage = st.radio("🛠 Choose Action", ["➕ Create", "📂 Manage"], horizontal=True)

    if create_or_manage == "➕ Create":
        st.markdown("### 🆕 Create New Invoice")
        
        # Card 1: Customer Selection
        st.markdown("<h4 style='color: #4CAF50;'>👤 Select Customer</h4>", unsafe_allow_html=True)
        customer_names = customers['customer_name'].tolist()
        selected_customer = st.selectbox("Choose a customer", customer_names)
        customer_id = customers[customers['customer_name'] == selected_customer]['customer_id'].values[0]

        # Card 2: Product Selection
        st.markdown("<h4 style='color: #4CAF50;'>🛍️ Select Products</h4>", unsafe_allow_html=True)
        product_names = products['product_name'].tolist()
        selected_products = st.multiselect("Choose products to add to the invoice", product_names)
        product_ids = products[products['product_name'].isin(selected_products)]['product_id'].tolist()

        # Card 3: Quantity and Price Display
        if selected_products:
            st.markdown("<h4 style='color: #4CAF50;'>🔢 Enter Quantities</h4>", unsafe_allow_html=True)
            quantities = []
            col1, col2 = st.columns(2)
            for product in selected_products:
                with col1:
                    qty = st.number_input(f"Quantity for {product}", min_value=1, value=1)
                    quantities.append(qty)
                with col2:
                    price = products[products['product_name'] == product]['price'].values[0]
                    st.write(f"💰 Price per unit: ₹{price:.2f}")

        # Card 4: Discounts and Taxes
        st.markdown("<h4 style='color: #4CAF50;'>💸 Discounts & 💰 Taxes</h4>", unsafe_allow_html=True)
        discount, tax = st.columns(2)
        with discount:
            discount_value = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=0.0)
        with tax:
            tax_value = st.number_input("Tax (%)", min_value=0.0, max_value=100.0, value=0.0)

        # Card 5: Calculate and Display Total
        if selected_products:
            subtotal = sum(
                products[products['product_id'] == product_id]['price'].values[0] * qty
                for product_id, qty in zip(product_ids, quantities)
            )
            total_amount = subtotal * (1 - discount_value / 100) * (1 + tax_value / 100)
            st.markdown(f"<h3 style='color: #4CAF50;'>🧾 Subtotal: ₹{subtotal:.2f}  |  <strong style='color: #FF6347;'>Final Total: ₹{total_amount:.2f}</strong></h3>", unsafe_allow_html=True)

        # Card 6: Payment Status
        st.markdown("<h4 style='color: #4CAF50;'>💳 Payment Status</h4>", unsafe_allow_html=True)
        payment_status = st.selectbox("Select payment status", ["✅ Paid", "❌ Unpaid", "🔄 Partially Paid"])

        # Card 7: Generate Invoice
        if st.button("📄 Generate Invoice", use_container_width=True):
            filename = generate_invoice(customer_id, product_ids, quantities, total_amount)
            new_invoice = pd.DataFrame([[len(invoices) + 1, customer_id, product_ids, quantities, total_amount, payment_status]],
                                      columns=["invoice_id", "customer_id", "product_ids", "quantities", "total_amount", "payment_status"])
            invoices = pd.concat([invoices, new_invoice], ignore_index=True)
            save_data(invoices, INVOICES_FILE)
            st.success("🎉 Invoice generated successfully!")

            with open(filename, "rb") as f:
                st.download_button(
                    "📥 Download Invoice PDF",
                    data=f,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )

    elif create_or_manage == "📂 Manage":
        st.markdown("### 📋 Manage Invoices")
        st.markdown("🔎 **Search by Customer Name or Invoice ID**")
        search_query = st.text_input("Search invoices")

        if search_query:
            filtered_invoices = invoices[ 
                invoices['customer_id'].astype(str).str.contains(search_query, case=False) |
                invoices['invoice_id'].astype(str).str.contains(search_query, case=False)
            ]
            st.dataframe(filtered_invoices, use_container_width=True)
        else:
            st.dataframe(invoices, use_container_width=True)



        # Admin Section
if menu == "Admin":
    st.title("🛠 Admin Dashboard")
    st.markdown("---")

    # Restrict access to Admins only
    if st.session_state.username != "tushar12uc":  # Replace with role-based check if needed
        st.error("🚫 You do not have permission to access this section.")
        st.stop()

    USERS_FILE = "users.csv"
    if os.path.exists(USERS_FILE):
        users = pd.read_csv(USERS_FILE)
    else:
        users = pd.DataFrame(columns=["Username", "Password", "Role"])

    # Admin Actions with Tabs for Better UI
    tab1, tab2 = st.tabs(["➕ Add Users", "🔍 Manage Users"])

    with tab1:
        st.subheader("Add New User")
        st.markdown("<h5 style='color: #4CAF50;'>👤 Enter Username</h5>", unsafe_allow_html=True)
        new_username = st.text_input("", placeholder="Username")

        st.markdown("<h5 style='color: #4CAF50;'>🔑 Enter Password</h5>", unsafe_allow_html=True)
        new_password = st.text_input("", placeholder="Password", type="password")

        st.markdown("<h5 style='color: #4CAF50;'>🛠 Select Role</h5>", unsafe_allow_html=True)
        new_role = st.selectbox("", ["Admin", "Editor", "Viewer"], index=2)

        add_user_button = st.button("🚀 Add User", use_container_width=True)

        if add_user_button:
            if new_username and new_password:
                if new_username in users['Username'].values:
                    st.error("⚠️ Username already exists!")
                else:
                    new_user = pd.DataFrame([[new_username, new_password, new_role]],
                                            columns=["Username", "Password", "Role"])
                    users = pd.concat([users, new_user], ignore_index=True)
                    users.to_csv(USERS_FILE, index=False)
                    st.success(f"✅ User **{new_username}** added successfully!")
            else:
                st.error("⚠️ Username and password are required!")

    with tab2:
        st.subheader("Manage Existing Users")
        if users.empty:
            st.warning("No users found. Add users first!")
        else:
            st.dataframe(users, use_container_width=True)

            username_to_edit = st.text_input("🔍 Enter Username to Edit/Delete")
            if username_to_edit:
                user_to_edit = users[users['Username'] == username_to_edit]
                if not user_to_edit.empty:
                    st.write("📌 Current Details:")
                    st.table(user_to_edit)

                    st.markdown("<h5 style='color: #4CAF50;'>🔑 Update Password</h5>", unsafe_allow_html=True)
                    new_password = st.text_input("New Password", type="password")

                    st.markdown("<h5 style='color: #4CAF50;'>🛠 Update Role</h5>", unsafe_allow_html=True)
                    new_role = st.selectbox("", ["Admin", "Editor", "Viewer"],
                                            index=["Admin", "Editor", "Viewer"].index(user_to_edit.iloc[0]['Role']))

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Update User", use_container_width=True):
                            users.loc[users['Username'] == username_to_edit, 'Password'] = new_password
                            users.loc[users['Username'] == username_to_edit, 'Role'] = new_role
                            users.to_csv(USERS_FILE, index=False)
                            st.success(f"✅ User **{username_to_edit}** updated successfully!")

                    with col2:
                        if st.button("❌ Delete User", use_container_width=True):
                            users = users[users['Username'] != username_to_edit]
                            users.to_csv(USERS_FILE, index=False)
                            st.success(f"🗑️ User **{username_to_edit}** deleted successfully!")
                else:
                    st.error("⚠️ Username not found!")




        #Profile Details
elif menu == "Profile":
    st.title("👤 My Profile")
    USERS_FILE = "users.csv"
    
    if os.path.exists(USERS_FILE):
        users = pd.read_csv(USERS_FILE)
        user_info = users[users['username'] == st.session_state.username]
        
        if not user_info.empty:
            st.subheader("📌 Profile Details")
            st.markdown(f"**👤 Username:** {user_info.iloc[0]['username']}")
            st.markdown(f"**🔑 Role:** {user_info.iloc[0]['role']}")
            
            with st.expander("✏️ Edit Profile"):
                new_password = st.text_input("🔒 Change Password", type="password")
                if st.button("✅ Update Password"):
                    users.loc[users['username'] == st.session_state.username, 'password'] = new_password
                    users.to_csv(USERS_FILE, index=False)
                    st.success("🔑 Password updated successfully!")
        else:
            st.warning("⚠️ No profile data found.")
    else:
        st.error("⚠️ User database not found!")

elif menu == "Terms and Conditions":
    st.title("📜 Terms and Conditions")
    
    terms_content = """
    ### 1. Introduction
    Welcome to our service. By using this platform, you agree to abide by the following terms.
    
    ### 2. User Responsibilities
    - Maintain confidentiality of your account.
    - Do not misuse or exploit the platform.
    
    ### 3. Privacy Policy
    We ensure data security, but users are responsible for safeguarding their credentials.
    
    ### 4. Amendments
    The terms may be updated at any time, and users are encouraged to review them regularly.
    
    ### 5. Contact Us
    For queries, reach out to support@example.com.
    """
    
    with st.expander("📜 Read Full Terms and Conditions"):
        st.markdown(terms_content)

