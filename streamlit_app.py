# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom Smoothie!.
  """
)
# Add a Name Box for Smoothie Orders
#import streamlit as st

name_on_order = st.text_input('Name on a Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)




#adding a select box
#import streamlit as st

#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("You selected:", option)

#Importar funcion para usar en columnas FRUIT_NAME

#agregar listado de frutas desde una tabla
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

# Add a Multiselect 
ingredients_list= st.multiselect(
    'Choose up 5 ingredients:'
    , my_dataframe
    ,max_selections=5
)
#Changing the LIST to a STRING
#Create the INGREDIENTS_STRING Variable 
if ingredients_list:
   # st.text(ingredients_list)
    #st.write(ingredients_list)

 ingredients_string=''
 for fruit_choosen in ingredients_list:
    ingredients_string+=fruit_choosen+' '

# st.write(ingredients_string)


my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""
st.write(my_insert_stmt)
time_to_insert= st.button('Submit Order')


if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


