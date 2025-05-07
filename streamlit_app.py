# Import Python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# App Title
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!.""")

# Name input for the smoothie order
name_on_order = st.text_input('Name on a Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# Connect to Snowflake and load the fruit options table
cnx = st.connection("snowflake")
session = cnx.session()

# Select only the fruit name column from the table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Multiselect for choosing ingredients
ingredients_list = st.multiselect(
    'Choose up 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Process selected ingredients and show nutrition info
if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # Call the external API for fruit nutrition
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

# Construct the SQL insert statement
my_insert_stmt = (
    """INSERT INTO smoothies.public.orders(ingredients, name_on_order)
       VALUES ('""" + ingredients_string + """', '""" + name_on_order + """')"""
)

st.write(my_insert_stmt)

# Submit button
time_to_insert = st.button('Submit Order')

# Execute the insert on button click
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
