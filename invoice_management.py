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
    ["Home", "Customer Management", "Product Management", "Invoice Management","Admin","Master Form","Order Management"]
)

#Home Section
if menu == "Home":
    st.title("User Dashboard")
    
    # Create the first row for year selection and submit button
    col1, col2 = st.columns(2)  # Make both columns equal in size
    with col1:
     selected_year = st.selectbox("Select Financial Year", ["2024-2025", "2023-2024", "2022-2023"])
    with col2:
     submit_clicked = st.button("Submit")  # Store the button click state
    if submit_clicked:  # Check if the button is clicked
        st.write(f"You selected the financial year: {selected_year}")
    
    # Create the second row for summary cards
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
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
    st.markdown("<h2 style='color: #4CAF50; text-align:center;'>📜 Invoice Management</h2>", unsafe_allow_html=True)
    action = st.radio("🛠 Choose Action", ["➕ Create", "📂 Manage"], horizontal=True)

    if action == "➕ Create":
        st.markdown("<h3 style='color: #4CAF50;'>🆕 Create Invoice</h3>", unsafe_allow_html=True)

        # Customer, Payment Status, and Invoice ID
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**👤 Customer**", unsafe_allow_html=True)
            customer_names = customers['customer_name'].tolist()
            selected_customer = st.selectbox("Select", customer_names)
            customer_id = customers.loc[customers['customer_name'] == selected_customer, 'customer_id'].values[0]
        
        with col2:
            st.markdown("**💳 Payment Status**", unsafe_allow_html=True)
            payment_status = st.selectbox("", ["✅ Paid", "❌ Unpaid", "🔄 Partially Paid"])
        
        with col3:
            st.markdown("**🧾 Invoice ID**", unsafe_allow_html=True)
            invoice_id = len(invoices) + 1
            st.markdown(f"<h4 style='color: #FF5733;'>#{invoice_id}</h4>", unsafe_allow_html=True)

        # Product Selection
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("**🛍️ Select Products**", unsafe_allow_html=True)  
        selected_products = st.multiselect("➕ Add", products['product_name'].tolist())

        # Product Table
        if selected_products:
            st.markdown("### 📦 Product Details")
            product_details = []
            for product in selected_products:
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    qty = st.number_input(f"{product}", min_value=1, value=1, key=product)
                with col2:
                    price = products.loc[products['product_name'] == product, 'price'].values[0]
                    st.markdown(f"**💰 ₹{price:.2f}**")
                with col3:
                    total_price = qty * price
                    st.markdown(f"**🔄 ₹{total_price:.2f}**")
                product_details.append((product, qty, price))

        # Discount & Tax
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            discount_value = st.number_input("💸 Discount (%)", min_value=0.0, max_value=100.0, value=0.0)
        with col2:
            tax_options = {"18%": 1.18, "28%": 2.28, "12%": 3.12}
            tax_label = st.selectbox("📊 GST Tax", list(tax_options.keys()))
            tax_value = tax_options[tax_label]
        with col3:
            if selected_products:
                subtotal = sum(p * q for _, q, p in product_details)
                total = subtotal * (1 - discount_value / 100) * (1 + tax_value / 100)
                st.markdown(f"<h3 style='color: #4CAF50;'>🧾 Subtotal: ₹{subtotal:.2f} | <strong style='color: #FF5733;'>Total: ₹{total:.2f}</strong></h3>", unsafe_allow_html=True)

        # Generate Invoice
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("📄 Generate Invoice", use_container_width=True):
            filename = generate_invoice(customer_id, [p[0] for p in product_details], [p[1] for p in product_details], total)
            new_invoice = pd.DataFrame([[invoice_id, customer_id, [p[0] for p in product_details], [p[1] for p in product_details], total, payment_status]],
                                       columns=["invoice_id", "customer_id", "products", "quantities", "total_amount", "payment_status"])
            invoices = pd.concat([invoices, new_invoice], ignore_index=True)
            save_data(invoices, INVOICES_FILE)
            st.success("🎉 Invoice generated!")

            with open(filename, "rb") as f:
                st.download_button("📥 Download PDF", data=f, file_name=filename, mime="application/pdf", use_container_width=True)

    elif action == "📂 Manage":
        st.markdown("<h3 style='color: #4CAF50;'>📋 Manage Invoices</h3>", unsafe_allow_html=True)
        search_query = st.text_input("🔎 Search by Customer Name or Invoice ID")
        filtered_invoices = invoices[
            invoices['customer_id'].astype(str).str.contains(search_query, case=False) | 
            invoices['invoice_id'].astype(str).str.contains(search_query, case=False)
        ] if search_query else invoices
        st.dataframe(filtered_invoices, use_container_width=True)






# Admin Section as a collapsible button
if menu == "Admin":
    with st.sidebar.expander("Admin", expanded=False):
        admin_menu = st.radio("Admin Options", ["Add Users", "Manage Users", "Profile", "Terms and Conditions"])

    # Add Users Section
    if admin_menu == "Add Users":
        st.title("🔒 Add New User")
        st.write("Fill in the details below to add a new user.")

        # Form to collect user details
        with st.form(key='add_user_form'):
            col1, col2 = st.columns(2)  # Two columns layout for the form
            with col1:
                username = st.text_input("Username", placeholder="Enter username", max_chars=20)
                email = st.text_input("Email Address", placeholder="Enter email address")
            with col2:
                password = st.text_input("Password", type="password", placeholder="Enter password", max_chars=20)
                role = st.selectbox("Role", ["Admin", "User", "Manager", "Customer"], index=1)

            submit_button = st.form_submit_button("Add User")

        # Handle form submission
        if submit_button:
            if not username or not password or not email:
                st.error("⚠️ All fields are required. Please fill in all the fields.")
            else:
                # Assuming a CSV file for storing users
                USERS_FILE = "users.csv"

                if os.path.exists(USERS_FILE):
                    users = pd.read_csv(USERS_FILE)
                else:
                    users = pd.DataFrame(columns=["username", "password", "role", "email"])

                # Check if the username already exists
                if username in users['username'].values:
                    st.error(f"⚠️ User `{username}` already exists. Please choose a different username.")
                else:
                    # Append the new user details to the dataframe
                    new_user = pd.DataFrame([[username, password, role, email]], columns=["username", "password", "role", "email"])
                    users = pd.concat([users, new_user], ignore_index=True)

                    # Save the updated user list back to the CSV file
                    users.to_csv(USERS_FILE, index=False)

                    # Success message
                    st.success(f"✅ User `{username}` added successfully!")

    # Manage Users Section
    elif admin_menu == "Manage Users":
        st.title("⚙️ Manage Users")
        st.write("List and management options for existing users.")

        # Load users from the CSV file
        USERS_FILE = "users.csv"

        if os.path.exists(USERS_FILE):
            users = pd.read_csv(USERS_FILE)
            st.write(f"### Existing Users (Total: {len(users)})")
            st.dataframe(users)

            # Edit User Section
            st.subheader("✏️ Edit User")
            edit_user = st.selectbox("Select User to Edit", users['username'])
            edit_user_info = users[users['username'] == edit_user]

            if edit_user_info.empty:
                st.warning("⚠️ User not found!")
            else:
                col1, col2 = st.columns(2)  # Two columns layout for edit form
                with col1:
                    new_password = st.text_input("New Password", value=edit_user_info.iloc[0]['password'], type="password")
                    new_email = st.text_input("New Email Address", value=edit_user_info.iloc[0]['email'])
                with col2:
                    new_role = st.selectbox("New Role", ["Admin", "User", "Manager", "Customer"], index=["Admin", "User", "Manager", "Customer"].index(edit_user_info.iloc[0]['role']))

                if st.button("✅ Update User"):
                    # Update the user details
                    users.loc[users['username'] == edit_user, 'password'] = new_password
                    users.loc[users['username'] == edit_user, 'role'] = new_role
                    users.loc[users['username'] == edit_user, 'email'] = new_email

                    # Save the updated users list back to the CSV file
                    users.to_csv(USERS_FILE, index=False)

                    st.success(f"✅ User {edit_user} updated successfully!")

            # Delete User Section
            st.subheader("🗑️ Delete User")
            delete_user = st.selectbox("Select User to Delete", users['username'])

            if st.button("✅ Delete User"):
                if delete_user:
                    # Remove the selected user from the dataframe
                    users = users[users['username'] != delete_user]

                    # Save the updated users list back to the CSV file
                    users.to_csv(USERS_FILE, index=False)

                    st.success(f"✅ User {delete_user} deleted successfully!")
        else:
            st.error("⚠️ User database not found!")

    # Profile Section
    elif admin_menu == "Profile":
        st.title("👤 Admin Profile")
        st.write("Admin profile information and settings.")
        st.markdown("Edit your profile information here.")
        st.text_area("Bio", placeholder="Write a short bio", height=200)

    # Terms and Conditions Section
    elif admin_menu == "Terms and Conditions":
        st.title("📜 Admin Terms and Conditions")
        terms_content = """
        ### 1. Introduction
        Welcome to our service. By using this platform, you agree to abide by the following terms.
        
        ### 2. Admin Responsibilities
        - Ensure platform security and proper user management.
        - Comply with privacy regulations and data handling policies.
        
        ### 3. Amendments
        The terms may be updated at any time, and admins are encouraged to review them regularly.
        """
        st.markdown(terms_content)

        # Add a checkbox to confirm acceptance of terms
        agree_terms = st.checkbox("I agree to the Terms and Conditions")

        if agree_terms:
            st.success("You have agreed to the terms and conditions!")
        else:
            st.warning("Please read and agree to the terms to proceed.")




# Simulate menu selection (Replace with actual logic)
menu = "Master Form"  

# Default value for master_option
master_option = "🛠 Services"  # A default safe option

# CSV file paths
SERVICE_FILE = "services.csv"
TAX_FILE = "taxes.csv"
PRODUCT_FILE = "products.csv"
PARTY_FILE = "partymaster.csv"

# Function to load data
def load_data(file_path, columns):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame(columns=columns)

# Function to save data
def save_data(file_path, df):
    df.to_csv(file_path, index=False)

# Load all master data
service_df = load_data(SERVICE_FILE, ["service_id", "service_name", "description", "price"])
tax_df = load_data(TAX_FILE, ["tax_id", "tax_type", "rate"])
product_df = load_data(PRODUCT_FILE, ["product_id", "product_name", "description", "price", "stock"])
party_df = load_data(PARTY_FILE, ["Party ID", "Party Name", "Phone Number", "Party Address"])


# Sidebar with compact UI and icons
if menu == "Master Form":
    with st.sidebar.expander("📜 Master Form", expanded=False):
        master_option = st.radio(
            "Select a Master Form Section",
            ["🛠 Services", "📊 Tax Master", "📦 Item Master", "🏢 Party Master"],
            index=0  # Default selection
        )

# Tab navigation with spacing
tab1, tab2 = st.tabs(["➕ Add", "📂 Manage"])

# Service Master Form
if master_option == "🛠 Services":
    with tab1:
        st.header("➕ Add New Service")
        
        with st.form("add_service_form"):
            col1, col2 = st.columns(2)
            with col1:
                service_name = st.text_input("Service Name", placeholder="Enter service name", max_chars=100)
            with col2:
                price = st.number_input("Price", min_value=0.0, format="%.2f", placeholder="Enter price")
            
            description = st.text_area("Description", placeholder="Provide a detailed description of the service", max_chars=300)
            
            submit_button = st.form_submit_button("Add Service", disabled=not service_name or not description or price <= 0)

        if submit_button:
            if service_name and description and price > 0:
                new_entry = {"service_id": len(service_df) + 1, "service_name": service_name, "description": description, "price": price}
                service_df = service_df.append(new_entry, ignore_index=True)
                save_data(SERVICE_FILE, service_df)
                st.success("✅ Service added successfully!")
                st.experimental_rerun()
            else:
                st.error("⚠️ Please fill out all fields correctly! Ensure the price is greater than 0.")

    with tab2:
        st.header("📂 Manage Services")
        
        edited_service_df = st.data_editor(
            service_df, 
            num_rows="dynamic",  
            use_container_width=True,
            key="service_editor"
        )

        save_button = st.button("💾 Save Changes", disabled=edited_service_df.equals(service_df))
        if save_button:
            save_data(SERVICE_FILE, edited_service_df)
            st.success("✅ Services updated successfully!")
            st.experimental_rerun()

        service_to_delete = st.selectbox("🗑️ Select a Service to Delete", service_df["service_id"].astype(str), index=None, placeholder="Choose a service...")
        if service_to_delete:
            delete_button = st.button("Delete Service")
            if delete_button:
                confirm_delete = st.checkbox("Are you sure you want to delete this service?", value=False)
                if confirm_delete:
                    service_df = service_df[service_df["service_id"].astype(str) != service_to_delete]
                    save_data(SERVICE_FILE, service_df)
                    st.warning("❌ Service deleted!")
                    st.experimental_rerun()
                else:
                    st.info("❕ Please confirm before deleting.")

# Tax Master Form
elif master_option == "📊 Tax Master":
    with tab1:
        st.header("➕ Add New Tax")
        
        with st.form("add_tax_form"):
            tax_type = st.selectbox("Tax Type", ["GST", "IGST"])
            tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, format="%.2f", placeholder="Enter tax rate")
            submit_tax = st.form_submit_button("Add Tax")

        if submit_tax:
            if tax_rate > 0:
                new_entry = {"tax_id": len(tax_df) + 1, "tax_type": tax_type, "rate": tax_rate}
                tax_df = tax_df.append(new_entry, ignore_index=True)
                save_data(TAX_FILE, tax_df)
                st.success("✅ Tax added successfully!")
                st.experimental_rerun()
            else:
                st.error("⚠️ Please enter a valid tax rate!")

    with tab2:
        st.header("📂 Manage Taxes")

        edited_tax_df = st.data_editor(
            tax_df, 
            num_rows="dynamic",
            key="tax_editor"
        )

        if st.button("💾 Save Changes"):
            save_data(TAX_FILE, edited_tax_df)
            st.success("✅ Taxes updated successfully!")
            st.experimental_rerun()

        tax_to_delete = st.selectbox("🗑️ Select a Tax to Delete", tax_df["tax_id"].astype(str), index=None, placeholder="Choose a tax...")
        if st.button("Delete Tax"):
            if tax_to_delete:
                tax_df = tax_df[tax_df["tax_id"].astype(str) != tax_to_delete]
                save_data(TAX_FILE, tax_df)
                st.warning("❌ Tax deleted successfully!")
                st.experimental_rerun()

# Item Master Form
elif master_option == "📦 Item Master":
    with tab1:
        st.header("➕ Add New Item")
        
        with st.form("add_item_form"):
            product_name = st.text_input("📝 Item Name")
            description = st.text_area("📜 Description", max_chars=300)
            price = st.number_input("💲 Price", min_value=0.0, format="%.2f")
            stock = st.number_input("📦 Stock Quantity", min_value=0, step=1)
            submit_item = st.form_submit_button("➕ Add Item")

        if submit_item:
            if product_name and price > 0:
                new_entry = {
                    "product_id": len(product_df) + 1, 
                    "product_name": product_name, 
                    "description": description, 
                    "price": price, 
                    "stock": stock
                }
                product_df = product_df.append(new_entry, ignore_index=True)
                save_data(PRODUCT_FILE, product_df)
                st.success("✅ Item added successfully!")
                st.experimental_rerun()
            else:
                st.error("⚠️ Please enter valid details!")

    with tab2:
        st.header("📂 Manage Items")

        edited_product_df = st.data_editor(
            product_df, 
            num_rows="dynamic",
            key="product_editor"
        )

        if st.button("💾 Save Changes"):
            save_data(PRODUCT_FILE, edited_product_df)
            st.success("✅ Items updated successfully!")
            st.experimental_rerun()

        item_to_delete = st.selectbox("🗑️ Select an Item to Delete", product_df["product_id"].astype(str), index=None, placeholder="Choose an item...")
        if st.button("Delete Item"):
            if item_to_delete:
                product_df = product_df[product_df["product_id"].astype(str) != item_to_delete]
                save_data(PRODUCT_FILE, product_df)
                st.warning("❌ Item deleted successfully!")
                st.experimental_rerun()

# Party Master Form
elif master_option == "🏢 Party Master":
    with tab1:
        st.header("➕ Add New Party")
        
        with st.form("add_party_form"):
            col1, col2 = st.columns(2)
            with col1:
                party_name = st.text_input("Party Name", placeholder="Enter party name")
            with col2:
                phone = st.text_input("Phone Number", placeholder="Enter phone number")
            
            address = st.text_area("Party Address", placeholder="Provide party address")

            submit_button = st.form_submit_button("Add Party", disabled=not party_name or not phone or not address)

        if submit_button:
            if party_name and phone and address:
                new_entry = {"Party ID": len(party_df) + 1, "Party Name": party_name, "Phone Number": phone, "Party Address": address}
                party_df = party_df.append(new_entry, ignore_index=True)
                save_data(PARTY_FILE, party_df)
                st.success("✅ Party added successfully!")
                st.experimental_rerun()
            else:
                st.error("⚠️ Please fill out all fields correctly!")

    with tab2:
        st.header("📂 Manage Parties")
        
        edited_party_df = st.data_editor(
            party_df, 
            num_rows="dynamic",  
            use_container_width=True,  
            key="party_editor"
        )

        save_button = st.button("💾 Save Changes", disabled=edited_party_df.equals(party_df))
        if save_button:
            save_data(PARTY_FILE, edited_party_df)
            st.success("✅ Parties updated successfully!")
            st.experimental_rerun()

        party_to_delete = st.selectbox("🗑️ Select a Party to Delete", party_df["Party ID"].astype(str), index=None, placeholder="Choose a party...")
        if st.button("Delete Party"):
            if party_to_delete:
                confirm_delete = st.checkbox("Are you sure you want to delete this party?", value=False)
                if confirm_delete:
                    party_df = party_df[party_df["Party ID"].astype(str) != party_to_delete]
                    save_data(PARTY_FILE, party_df)
                    st.warning("❌ Party deleted!")
                    st.experimental_rerun()
                else:
                    st.info("❕ Please confirm before deleting.")

# Display the selected option
st.write(f"Selected Master Option: {master_option}")

