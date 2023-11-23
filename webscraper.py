import requests
from bs4 import BeautifulSoup
import datetime, csv, os, json
from dotenv import load_dotenv
from supabase_py import create_client

load_dotenv()
TABLE_NAME = 'meals'
SUPABASE_URL, SUPABASE_KEY = os.getenv('SUPABASE_URL'), os.getenv("SUPABASE_KEY")

SUPABASE = create_client(SUPABASE_URL,SUPABASE_KEY)

Dining_commons = [("Berkshire", "https://umassdining.com/locations-menus/berkshire/menu"), ("Worcester", "https://umassdining.com/locations-menus/worcester/menu"), ("Franklin", "https://umassdining.com/locations-menus/franklin/menu"), ("Hampshire", "https://umassdining.com/locations-menus/hampshire/menu")]


#div containers that contain each individual food list
Menu_class_tags = ['breakfast_fp',"lunch_fp","dinner_fp","grabngo","latenight_fp"]

# h2 children of menu_class_tags have a class="menu_category_name" for the station name
# li children with class="lightbox-nutrition" contain an a tag with the following attributes

food_attributes = ['data-healthfulness','data-carbon-list','data-ingredient-list','data-allergens','data-recipe-webcode','data-clean-diet-str','data-serving-size','data-calories','data-caloried-from-fat','data-total-fat','data-total-fat-dv','data-sat-fat','data-sat-fat-dv', 'data-trans-fat','data-cholesterol','data-cholesterol_dv' 'data-sodium', 'data-sodium-dv','data-total-carb', 'data-total-carb-dv','data-dietary-fiber','data-dietary-fiber-dv', 'data-sugars','data-sugars-dv', 'data-protein','data-protein-dv','data-dish-name',]
#the dv attributes are % of daily value

def FormattingFoodMetaData(menu_tag, station, food_item, diningCommon):
    today = datetime.date.today().strftime('%Y-%m-%d')
    meal_time = menu_tag.split("_")[0]
    formatted_data =  {
        "meal_time": meal_time,
        'station': station.text,
        "date": today,
        "dining_common": diningCommon
    }
    for attribute in food_attributes:
        meta_data = food_item.get(attribute)
        meta_data_tag = attribute.split('data-')[1].replace("-","_")
        if(meta_data != None):
            formatted_data[meta_data_tag] = meta_data.strip()
    
    for (key, value) in formatted_data.items():
        if value == "" or value == '':
            formatted_data[key] = None

    return formatted_data

# async def InsertIntoDB(data):
#     return await SUPABASE.table(TABLE_NAME).insert(data)
    

def FormatToCSV(data,diningCommon):
    headers = data.keys()
    has_header = False
    file_path = f'./data/{diningCommon}.csv'
    try:
        with open(file_path, "r") as file:
            has_header = csv.Sniffer().has_header(file.read(100))
    except:
        # bad except block
        # Unsure why this code runs right now
        print("facing an error with file!")

    with open(file_path, "a", newline="", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        if not has_header:
            writer.writeheader()
        writer.writerow(data)
    

input_data = []    

for (diningCommon, diningURL) in Dining_commons:
    print(diningCommon + '\n')
    req = requests.get(diningURL)
    soup = BeautifulSoup(req.content,"html.parser")

    # this loops through all the individual components
    for menu_tag in Menu_class_tags:
        menu_container= soup.find('div', {"class": menu_tag, "id":"content_text"})
        if menu_container != None:
            stations = menu_container.findAll('h2',{'class':'menu_category_name'})
            for station in stations:
                # print(station.text + '\n')
                    curr_element = station.find_next_sibling()
                    while curr_element not in stations and curr_element != None:
                        food_item = curr_element.find("a")
                        data =FormattingFoodMetaData(menu_tag=menu_tag, station=station, food_item=food_item, diningCommon=diningCommon)
                        # input_data.append(data)
                        # print(input_data[0])
                        # curr_element = curr_element.next_sibling
                        data_values = list(data.values())
                        response = SUPABASE.table(TABLE_NAME).insert(data).execute()
                        # print(response)
                        if response["status_code"] == 201:
                            print("success")
                            curr_element = curr_element.next_sibling
                        else:
                            print(f"Error: {response.text}")
                        # FormatToCSV(data,diningCommon)


