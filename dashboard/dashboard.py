import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
#Sarah Salsabila
# Load Data


@st.cache_data
def load_data():
    # Gantilah dengan dataset Anda
    return pd.read_csv("dataset/productOrder_data.csv")
filtered_data = load_data()
    
# Konversi kolom 'order_purchase_timestamp' ke tipe data datetime
filtered_data['order_purchase_timestamp'] = pd.to_datetime(filtered_data['order_purchase_timestamp'])
pastel_lilac_purple_palette = [
    '#E6C9E8',  # Lavender Light Purple (Lavender Pastel)
    '#D8A8D5',  # Lilac Light Purple
    '#F7C8D7',  # Soft Pink (Pastel Pink)
    '#BFA0D8',  # Pastel Purple
    '#A0C4FF',  # Soft Blue (Pastel Blue)
    '#B8E5D4'   # Mint Green (Soft Mint Green)
]
palette_4 = ['#9B79B6',  # Soft Plum
             '#FFD1B3',  # Pastel Peach
             '#A0C4FF',  # Soft Blue
             '#F7C8D7',  # Soft Pink
             '#E6C9E8']  # Lavender Light Purple
# Sidebar untuk memilih analisis
with st.sidebar:
        st.title("Dashboard Menu")
    # Sidebar - Step 1: Ask if user wants to filter data
        filter_option = st.sidebar.radio(
            "Do you want to filter the data?",
            ['No', 'Yes']
        )

        # Sidebar - Step 2: If 'Yes', show the multiselect for categories
        category_filter = None
        if filter_option == 'Yes':
            category_filter = st.sidebar.multiselect('Select Category(s)', 
                                                    options=filtered_data['product_category'].unique() )
        # Filter data based on the selected categories (if any)
        if category_filter:
            filtered_data = filtered_data[filtered_data['product_category'].isin(category_filter)]
            st.success('Category Filter Applied , Showing Filtered Data')
        else:
            st.warning("No category selected, showing all data.")
            filtered_data = filtered_data  # No filter applied
        
        analysis_option = st.radio(
            "Choose an analysis",
            [
                "Homepage",
                "Data Overview",
                "Top and Bottom Categories",
                "Highest Order",
                "Order Trends Over Time",
                "Popular Payment Methods",
                "Customer Satisfaction Level",
                "RFM Analysis",
            ],
        )


if analysis_option == "Homepage":
        st.title("📊 Sales and RFM Analysis Dashboard by Sarah Salsabila")
        st.write(
            "Welcome to the dashboard! Use the sidebar to navigate through different analyses.")
        st.image(r'Image/Sarsabila_purple_dashboard_-removebg-preview (1).png')
        
        
    # Data Overview
elif analysis_option == "Data Overview":
        st.subheader("📁 Dataset Preview")
        st.write(filtered_data.head())
        num_rows, num_columns = filtered_data.shape
        num_unique_categories = filtered_data['product_category'].nunique()
        data_info = pd.DataFrame({
            'Num of Rows': [num_rows],
            'Num of Columns': [num_columns],
            'Category' : [num_unique_categories]
        })
        
        data_info_styled = data_info.style.set_properties(**{'text-align': 'center'})
        # Display the information as a table
        st.write("**Filtered Data Information**:")
        st.table(data_info)

    # Analisis 1: Penjualan Tertinggi dan Terendah per Kategori

elif analysis_option == "Top and Bottom Categories":
    
        st.subheader("📈 Top and Bottom Product Categories by Sales")

        # Hitung total penjualan per kategori
        sales_by_category = filtered_data.groupby('product_category')[
            'price'].sum().reset_index()
        sales_by_category.columns = ['Category', 'Total Sales']

        # Urutkan berdasarkan total penjualan
        top_categories = sales_by_category.sort_values(
            by='Total Sales', ascending=False).head(10)
        bottom_categories = sales_by_category.sort_values(
            by='Total Sales', ascending=True).head(10)

        # Tampilkan penjualan tertinggi
        st.write("**Top 10 Categories by Sales:**")
        st.write(top_categories)

        # Visualisasi penjualan tertinggi
        st.title('**Top 10 Categories by Sales**')
        tab1, tab2= st.tabs(['Matplotlib','Plotly'])
        with tab1:
            st.header("Matplotlib")
            st.write("**Top 10 Categories by Sales:**")
            fig, ax = plt.subplots(figsize=(10, 6),facecolor='black')
            fig.patch.set_alpha(0.0)
            sns.barplot(data=top_categories, x='Total Sales', y='Category', palette=pastel_lilac_purple_palette)

            # Menambahkan garis pembeda (misalnya garis vertikal pada x=0)
            plt.axvline(x=0, color='white', linestyle='--', linewidth=1)  # Garis vertikal hitam pada x=0
            # Set axis background to black
            plt.gca().set_facecolor('black')
#sarah salsabila
            # Change tick labels to white
            plt.xticks(color='white')
            plt.yticks(color='white')
            # Menambahkan garis horizontal pada beberapa titik (berdasarkan posisi y Category)
            for i, y_value in enumerate(top_categories['Category']):
                plt.axhline(y=i, color='gray', linestyle='--', linewidth=0.7)

            # Pengaturan lainnya
            plt.xlabel('Total Sales',color = 'white')
            plt.ylabel('Category',color = 'white')
                # Remove the borders or any additional box around the plot
            plt.gca().spines['top'].set_visible(False)  # Hide the top spine (border)
            plt.gca().spines['right'].set_visible(False)  # Hide the right spine (border)
            plt.gca().spines['left'].set_visible(False)  # Hide the left spine (border)
            plt.gca().spines['bottom'].set_visible(False)  # Hide the bottom spine (border)
            plt.tight_layout()  # Adjust layout to prevent cutting off labels
            plt.show()
            st.pyplot(plt)
        with tab2:
             st.header("Plotly")
             fig_top = px.bar(top_categories, 
                    x='Total Sales', 
                    y='Category', 
                    title='Top Categories by Sales :',
                    color='Category',
                    color_discrete_sequence=pastel_lilac_purple_palette)
             st.plotly_chart(fig_top)
             
        # Tampilkan penjualan terendah
        st.write("**Bottom 10 Categories by Sales:**")
        st.write(bottom_categories)

        # Visualisasi penjualan terendah
        st.title('**Bottom 10 Categories by Sales**')
        tab1, tab2= st.tabs(['Matplotlib','Plotly'])
        with tab1:
            st.header("Matplotlib")#sarah salsabila
            st.write("**Bottom 10 Categories by Sales:**")
            fig, ax = plt.subplots(figsize=(10, 6),facecolor='black')
            fig.patch.set_alpha(0.0)
            sns.barplot(data=bottom_categories, x='Total Sales', y='Category', palette=pastel_lilac_purple_palette)

            # Menambahkan garis pembeda (misalnya garis vertikal pada x=0)
            plt.axvline(x=0, color='white', linestyle='--', linewidth=1)  # Garis vertikal hitam pada x=0
            # Set axis background to black
            plt.gca().set_facecolor('black')

            # Change tick labels to white
            plt.xticks(color='white')
            plt.yticks(color='white')
            # Menambahkan garis horizontal pada beberapa titik (berdasarkan posisi y Category)
            for i, y_value in enumerate(bottom_categories['Category']):
                plt.axhline(y=i, color='gray', linestyle='--', linewidth=0.7)

            # Pengaturan lainnya
            plt.xlabel('Total Sales',color = 'white')
            plt.ylabel('Category',color = 'white')
                # Remove the borders or any additional box around the plot
            plt.gca().spines['top'].set_visible(False)  # Hide the top spine (border)
            plt.gca().spines['right'].set_visible(False)  # Hide the right spine (border)
            plt.gca().spines['left'].set_visible(False)  # Hide the left spine (border)
            plt.gca().spines['bottom'].set_visible(False)  # Hide the bottom spine (border)
            plt.tight_layout()  # Adjust layout to prevent cutting off labels
            plt.show()
            st.pyplot(plt)
            
        with tab2:
             st.header("Plotly")
             fig_bottom = px.bar(bottom_categories, 
                    x='Total Sales', 
                    y='Category', 
                    title='Top Categories by Sales :',
                    color='Category',
                    color_discrete_sequence=pastel_lilac_purple_palette)
             st.plotly_chart(fig_bottom)
        # Analisis 2: Pesanan Tertinggi
elif analysis_option == "Highest Order":
        st.subheader("📅 Highest Order")

        # Hitung jumlah pesanan per bulan
        filtered_data['order_month'] = filtered_data['order_purchase_timestamp'].dt.to_period(
            'M').astype(str)
        Monthly_orders = filtered_data.groupby('order_month')[
            'order_id'].nunique().reset_index()
        Monthly_orders.columns = ['Month', 'Number of Orders']

        top_5_months = Monthly_orders.sort_values(by='Number of Orders',ascending=False).head(5)
        
        # Tampilkan pesanan tertinggi
        st.write("**Monthly Sales with Highest Orders:**")
        st.write(top_5_months)#Sarah Salsabila

            # Create the plot
        st.title('**Monthly Sales with Highest Orders:**')
        tab1, tab2= st.tabs(['Matplotlib','Plotly'])
        with tab1:
            st.header("Matplotlib")
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)  # Make axis background transparent
            # Plot the line chart
            ax.plot(top_5_months['Month'], top_5_months['Number of Orders'], color="#BFA0D8", label='Orders', linewidth=2)
            # Add title and labels
            ax.set_xlabel('Month',color='white')
            ax.set_ylabel('Number of Orders',color='white')
            for i, x_value in enumerate(top_5_months['Month']):
                plt.axvline(x=i, color='gray', linestyle='--', linewidth=0.7)
            # Rotate the x-axis labels for better readability
            plt.xticks(rotation=45,color='white')
            plt.yticks(color="white")
            plt.gca().set_facecolor('black')
            # Plot the points on the line (scatter)
            ax.scatter(top_5_months['Month'], top_5_months['Number of Orders'], color="#6A4C9C", zorder=5, label="Titik")

            # Tight layout to avoid cut-off
            plt.tight_layout()
            ax.spines['top'].set_visible(False)  # Show the top border (axis line)
            ax.spines['right'].set_visible(False)  # Show the right border (axis line)
            ax.spines['left'].set_visible(False)  # Show the left border (axis line)
            ax.spines['bottom'].set_visible(False)  # Show the bottom border (axis line)
            # Display the plot in Streamlit
            st.write("**Visualization of Monthly Sales with the Top 5 Highest Orders :**")
            st.pyplot(fig)
        
        with tab2:
            st.header("Plotly")
            fig_highest = px.line(top_5_months, 
                        x='Month',
                        y='Number of Orders', 
                        title='Visualization of Monthly Sales with the Top 5 Highest Orders :',markers=True)
            fig_highest.update_traces(
                line=dict(color="#BFA0D8",width=2),
                marker=dict(color="#6A4C9C",size=8))
            st.plotly_chart(fig_highest) #Sarah Salsabila

    # Analisis 3: Tren Jumlah Pesanan dari Waktu ke Waktu
elif analysis_option == "Order Trends Over Time":
        st.subheader("📅 Order Trends Over Time")      
        # Hitung jumlah pesanan per bulan
        filtered_data['order_month'] = filtered_data['order_purchase_timestamp'].dt.to_period(
            'M').astype(str)
        Monthly_orders = filtered_data.groupby('order_month')[
            'order_id'].nunique().reset_index()
        Monthly_orders.columns = ['Month', 'Number of Orders']

        # Tampilkan tren pesanan
        st.write("**Number of Orders Over Time:**")
        st.write(Monthly_orders)
        
        tab1,tab2 = st.tabs(['Maplotlib','Plotly'])
        with tab1:
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)  # Make axis background transparent
            # Plot the line chart
            ax.plot(Monthly_orders['Month'], Monthly_orders['Number of Orders'], color="#BFA0D8", label='Orders', linewidth=2)
            # Add title and labels
            ax.set_xlabel('Month',color='white')
            ax.set_ylabel('Number of Orders',color='white')
            for i, x_value in enumerate(Monthly_orders['Month']):
                plt.axvline(x=i, color='gray', linestyle='--', linewidth=0.7)
            # Rotate the x-axis labels for better readability
            plt.xticks(rotation=45,color='white')
            plt.yticks(color="white")
            plt.gca().set_facecolor('black')
            # Plot the points on the line (scatter)
            ax.scatter(Monthly_orders['Month'], Monthly_orders['Number of Orders'], color="#6A4C9C", zorder=5, label="Titik")
            # Tight layout to avoid cut-off
            plt.tight_layout()
            ax.spines['top'].set_visible(False)  # Show the top border (axis line)
            ax.spines['right'].set_visible(False)  # Show the right border (axis line)
            ax.spines['left'].set_visible(False)  # Show the left border (axis line)
            ax.spines['bottom'].set_visible(False)  # Show the bottom border (axis line)
            # Display the plot in Streamlit
            st.write("**Order Trends Over Time :**")
            st.pyplot(fig)
        with tab2:
            # Visualisasi tren pesanan
            fig_trend = px.line(Monthly_orders, x='Month',
                                y='Number of Orders', title='Order Trends Over Time :')
            fig_trend.update_traces(line=dict(color="#6A4C9C")) 
            st.plotly_chart(fig_trend)

    # Analisis 4: Metode Pembayaran Terfavorit
elif analysis_option == "Popular Payment Methods":
        st.subheader("💳 Most Popular Payment Methods")
        
        # Hitung jumlah penggunaan metode pembayaran
        payment_methods = filtered_data['payment_type'].value_counts().reset_index()
        payment_methods.columns = ['Payment Method', 'sales']
        
        # Add Streamlit widgets for filtering (e.g., by Payment Method)
        payment_method_filter = st.selectbox('Select Payment Method', ['All'] + payment_methods['Payment Method'].tolist())

        # Filter the data based on the selected payment method
        if payment_method_filter != 'All':
            filtered_data = payment_methods[payment_methods['Payment Method'] == payment_method_filter]
        else:
            filtered_data = payment_methods
        
        # Tampilkan metode pembayaran terfavorit
        st.write("**Most Popular Payment Methods:**")
        st.write(filtered_data)

        # Visualisasi metode pembayaran terfavorit
        fig_payment = px.pie(filtered_data, values='sales',
                            names='Payment Method', title='Payment Method Distribution',color_discrete_sequence=pastel_lilac_purple_palette)
        fig_payment.update_traces(textinfo='percent+label',  # This shows percentage and label (payment method)
                            pull=[0.1, 0, 0, 0, 0])  # Optionally, you can "pull" slices out for emphasis
        st.plotly_chart(fig_payment)
 
            # Analisis 4: Customer Satisfaction Level
elif analysis_option == "Customer Satisfaction Level":
        st.subheader("📊 Customer Satisfaction Level")
        review_data = pd.read_csv('dataset/order_reviews_dataset.csv')
        merged_data = pd.merge(filtered_data, review_data, on='order_id', how='left')
        # Get the review score distribution
        reviewrate = merged_data['review_score'].value_counts().sort_values(ascending=False)
    
    # Identify the most common score
        most_common_score = reviewrate.idxmax()
        reviewrate_df = reviewrate.reset_index()
        reviewrate_df.columns = ['Review Score', 'Count']
    
        st.write("**Customer Satisfaction Level:**")
        st.write( most_common_score )
        st.write('Customers Satifaction Tabel')
        st.write(reviewrate_df)#sarah Salsabila
        
        fig_rating = px.bar(reviewrate_df, 
                        x='Review Score', 
                        y='Count', 
                        title='Customer Satisfaction Level Distribution',
                        color='Review Score',  
                        color_discrete_sequence = pastel_lilac_purple_palette)
        st.plotly_chart(fig_rating)

    
    # Analisis 5: RFM Analysis
elif analysis_option == "RFM Analysis":
        st.subheader("📊 RFM Analysis")

        # Hitung RFM Metrics
        latest_date = filtered_data['order_purchase_timestamp'].max()
        rfm_df = filtered_data.groupby('customer_id').agg({
            # Recency
            'order_purchase_timestamp': lambda x: (latest_date - x.max()).days,
            'order_id': 'count',  # Frequency
            'payment_value': 'sum'  # Monetary
        })

        # Ganti nama kolom agar lebih jelas
        rfm_df.rename(columns={
            'order_purchase_timestamp': 'Recency',
            'order_id': 'Frequency',
            'payment_value': 'Monetary'
        }, inplace=True)

        # Tampilkan RFM Metrics
        st.write("RFM Metrics:")
        st.write(rfm_df.head())

        # Terapkan RFM Segmentation
        st.subheader("📌 RFM Segmentation")
        rfm_df['R_Score'] = pd.cut(rfm_df['Recency'].rank(
            method="first"), bins=3, labels=[3, 2, 1])
        rfm_df['F_Score'] = pd.cut(rfm_df['Frequency'].rank(
            method="first"), bins=3, labels=[1, 2, 3])
        rfm_df['M_Score'] = pd.cut(rfm_df['Monetary'].rank(
            method="first"), bins=3, labels=[1, 2, 3])

        # Gabungkan skor menjadi RFM Score
        rfm_df['RFM_Score'] = (
            rfm_df['R_Score'].astype(str) +
            rfm_df['F_Score'].astype(str) +
            rfm_df['M_Score'].astype(str)
        )

        # Buat RFM Segmentation
        def segment_customer(row):
            r, f, m = int(row['R_Score']), int(row['F_Score']), int(row['M_Score'])

            if r == 3 and f == 3 and m == 3:
                return 'Loyal Customers'
            elif r == 3 and (f < 3 or m < 3):
                return 'Promising'
            elif r < 3 and f >= 2 and m >= 2:
                return 'Customers Needing Attention'
            else:
                return 'Hibernating'

        # Buat kolom baru untuk segmentasi
        rfm_df['Segment'] = rfm_df.apply(segment_customer, axis=1)

        # Tampilkan RFM Segmentation
        st.write("RFM Segmentation:")
        st.write(rfm_df.head())

        # Visualisasi Segmentasi Pelanggan
        st.subheader("📊 Customer Segmentation Distribution")
        segmentation_counts = rfm_df['Segment'].value_counts().reset_index()
        segmentation_counts.columns = ['Segment', 'Count']
        fig_seg = px.bar(segmentation_counts, x='Segment', y='Count',
                        color='Segment', title='Customer Segmentation',color_discrete_sequence=pastel_lilac_purple_palette)
        st.plotly_chart(fig_seg)
