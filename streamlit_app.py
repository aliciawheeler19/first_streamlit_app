# using just streamlit
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# adding in python
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Adding the header for the fruityvice api response 
streamlit.header("Fruityvice Fruit Advice!")

# create a helper function
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# new version
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  
## Old Code
# Textbox to ask which fruit the user is looking for
# fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
# Screen text to show what the user asked for
# streamlit.write('The user entered ', fruit_choice)

# Adding the Fruityvice API to the Streamlit App
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# showed the stream of raw data on the screen: streamlit.text(fruityvice_response.json())

# import the data from fruityvice into a table
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# creates a view for the table on the page
#streamlit.dataframe(fruityvice_normalized)

# New Code
streamlit.header("The fruit load list contains:")
# Snowflake related function
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

# Add a button to load the fruit data
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('"+ new_fruit + "')")
    return "Thanks for adding " + new_fruit

add_my_fruit =  streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function =  insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)
  
# doesn't run anything past here
streamlit.stop()

## Old Code
# Adding in the Snowflake connector to the streamlit app
# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from fruit_load_list")
# my_data_rows = my_cur.fetchall()
# streamlit.header("The fruit load list contains:")
# streamlit.dataframe(my_data_rows)

# Add data into snowflake table
# Textbox to ask which fruit the user is looking for
# add_my_fruit = streamlit.text_input('What fruit would you like to add?')
# my_cur.execute("insert into fruit_load_list values ('"+ add_my_fruit+  "');")
# streamlit.write('Thanks for adding ', add_my_fruit)
# my_cur.excute("insert into fruit_load_list values ('from streamlit')")
