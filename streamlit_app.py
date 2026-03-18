import streamlit as st
import snowflake.snowpark.functions as F
import requests as r
from snowflake.snowpark.context import get_active_session


cnx = st.connection("snowflake")
session = cnx.session()

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)
name_on_smoothie = st.text_input(
    "Name on the Smoothie:"
)


my_dataframe = session.table("smoothies.public.fruit_options").select(F.col("SEARCH_ON"))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections = 5
)

if ingredient_list:
    ingredient_string = ""

    for fruit_chosen in ingredient_list:
        ingredient_string += fruit_chosen + ""
        st.subheader(fruit_chosen + " Nutrition Information")
        smoothiefroot_response = r.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    #st.write(ingredient_string)

    my_insert_stmt = """
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('""" + ingredient_string + """',
                '""" + name_on_smoothie + """')
    """

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(f"Your Smoothie is ordered, {name_on_smoothie}!", icon="✅")



