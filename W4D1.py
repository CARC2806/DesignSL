import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

data = pd.read_csv("rest.csv")

def navigation_menu():
    menu = ["About Us", "Locations", "EDA"]
    choice = st.sidebar.radio("Navigate to", menu)
    return choice

def about_us():
    st.header("About Us")
    st.write("""
   Welcome to Where Can I Eat?! This site is your go-to resource for finding restaurants of all price ranges, no matter where you are in the world.
    """)
    st.image("image.png",caption='OpenAI. (2024). A minimalist illustration featuring a fork and knife crossed on a plate [Digital image]. DALL·E.', use_column_width=True)

def locations():
    st.header("Locations")
    st.write("Explore restaurants by selecting a city.")

    city_options = data['City'].unique()
    selected_city = st.selectbox("Choose a city:", city_options)

    city_data = data[data['City'] == selected_city]

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=city_data,
        get_position='[Longitude, Latitude]',
        get_color='[200, 30, 0, 160]',
        get_radius=500,
        pickable=True,
    )

    if not city_data.empty:
        initial_view_state = pdk.ViewState(
            latitude=city_data['Latitude'].mean(),
            longitude=city_data['Longitude'].mean(),
            zoom=10,  # Zoom level for city view
            pitch=0
        )
    else:
        initial_view_state = pdk.ViewState(
            latitude=data['Latitude'].mean(),
            longitude=data['Longitude'].mean(),
            zoom=2,  # Default zoom level
            pitch=0
        )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=initial_view_state,
        tooltip={"text": "{Name}\nCuisine: {Cuisine}\nRating: {Rating}"}
    )
    st.pydeck_chart(r)

    st.write(f"Restaurants in {selected_city}:")
    st.write(city_data)

def eda():
    st.header("Exploratory Data Analysis")
    st.write("Explore data insights and visualizations.")

    st.subheader("Cuisine Distribution")
    cuisine_counts = data['Cuisine'].value_counts().reset_index()
    cuisine_counts.columns = ['Cuisine', 'Count']
    fig_cuisine = px.bar(
        cuisine_counts,
        x='Cuisine',
        y='Count',
        title="Number of Restaurants by Cuisine",
        labels={'Cuisine': 'Cuisine Type', 'Count': 'Number of Restaurants'},
        text='Count',
        height=600
    )
    fig_cuisine.update_layout(
        xaxis={'categoryorder': 'total descending', 'tickangle': 45},
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
    )
    st.plotly_chart(fig_cuisine)

    st.subheader("Ratings Distribution")
    fig_ratings = px.histogram(
        data,
        x='Rating',
        nbins=5,
        title="Distribution of Ratings",
        labels={'Rating': 'Rating', 'Count': 'Frequency'},
        height=600
    )
    fig_ratings.update_layout(
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
    )
    st.plotly_chart(fig_ratings)

    st.subheader("Average Meal Price by Country")
    avg_price_by_country = data.groupby('Country')['Average Meal Price'].mean().reset_index()
    avg_price_by_country = avg_price_by_country.sort_values(by='Average Meal Price', ascending=False)
    fig_price = px.bar(
        avg_price_by_country,
        x='Country',
        y='Average Meal Price',
        title="Average Meal Price by Country",
        labels={'Country': 'Country', 'Average Meal Price': 'Average Price'},
        text='Average Meal Price',
        height=600
    )
    fig_price.update_layout(
        xaxis={'categoryorder': 'total descending', 'tickangle': 45},
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
    )
    st.plotly_chart(fig_price)

def set_background_color(color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
def main():
    set_background_color("#fff5e6")

    st.image("banner.png", use_column_width=True)

    st.markdown(
        """
        <style>
        .button-row {
            display: flex;
            justify-content: space-between; /* Space buttons evenly across the width */
            align-items: center;
            width: 100%; /* Full width of the container */
            max-width: 1200px; /* Align to the banner width */
            margin: 0 auto; /* Center the button row */
            padding: 10px 0; /* Add spacing */
        }
        .stButton>button {
            width: 150px; /* Consistent button size */
            height: 50px; /* Consistent button size */
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            background-color: #f7e7ce;
            border: 1px solid #d5bbaa;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #edd8b7;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="button-row">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1], gap="large")

    with col1:
        if st.button("About Us", key="about_us"):
            st.session_state["current_page"] = "About Us"
    with col2:
        if st.button("Locations", key="locations"):
            st.session_state["current_page"] = "Locations"
    with col3:
        if st.button("EDA", key="eda"):
            st.session_state["current_page"] = "EDA"

    st.markdown('</div>', unsafe_allow_html=True)

    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "About Us"

    if st.session_state["current_page"] == "About Us":
        about_us()
    elif st.session_state["current_page"] == "Locations":
        locations()
    elif st.session_state["current_page"] == "EDA":
        eda()
        
if __name__ == "__main__":
    main()