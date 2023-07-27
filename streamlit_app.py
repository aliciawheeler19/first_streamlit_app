# using just streamlit
import streamlit

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# adding in python
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Adding the header for the fruityvice api response 
streamlit.header("Fruityvice Fruit Advice!")

# Textbox to ask which fruit the user is looking for
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
# Screen text to show what the user asked for
streamlit.write('The user entered ', fruit_choice)

# Adding the Fruityvice API to the Streamlit App
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# showed the stream of raw data on the screen: streamlit.text(fruityvice_response.json())

# import the data from fruityvice into a table
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# creates a view for the table on the page
streamlit.dataframe(fruityvice_normalized)

# Adding in the Snowflake connector to the streamlit app
import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Add data into snowflake table
# Textbox to ask which fruit the user is looking for
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
my_cur.execute("insert into fruit_load_list value ('"+ add_my_fruit+  "');")
streamlit.write('Thanks for adding ', add_my_fruit)
