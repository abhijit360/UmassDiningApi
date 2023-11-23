import requests
from bs4 import BeautifulSoup
import datetime
Dining_commons = [("Berkshire", "https://umassdining.com/locations-menus/berkshire/menu"), ("Worcester", "https://umassdining.com/locations-menus/worcester/menu"), ("Franklin", "https://umassdining.com/locations-menus/franklin/menu"), ("Hampshire", "https://umassdining.com/locations-menus/hampshire/menu")]


#div containers that contain each individual food list
Menu_class_tags = ['breakfast_fp',"lunch_fp","dinner_fp","grabngo","latenight_fp"]

# h2 children of menu_class_tags have a class="menu_category_name" for the station name
# li children with class="lightbox-nutrition" contain an a tag with the following attributes

food_attributes = ['data-healthfulness','data-carbon-list','data-ingredient-list','data-allergens','data-recipe-webcode','data-clean-diet-str','data-serving-size','data-calories','data-caloried-from-fat','data-total-fat','data-total-fat-dv','data-sat-fat','data-sat-fat-dv data-trans-fat','data-cholesterol','data-cholesterol dv data-sodium', 'data-sodium-dv','data-total-carb', 'data-total-carb-dv','data-dietary-fiber','data-dietary-fiber-dv', 'data-sugars','data-sugars-dv data-protein','data-protein-dv','data-dish-name',]
#the dv attributes are % of daily value

def FormattingFoodMetaData(menu_tag, station, food_item):
    today = datetime.date.today()
    meal_time = menu_tag.split("_")[0]
    formatted_data =  {
        "meal_time": meal_time,
        'station': station,
        "date": today,
    }
    for attribute in food_attributes:
        meta_data_tag = attribute.split('data-')[1]
        meta_data = food_item.get(attribute)
        if(meta_data != None):
            formatted_data[meta_data_tag] = meta_data.strip()

    return formatted_data


for (dining, diningURL) in Dining_commons:
    print(dining + '\n')
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
                    print(FormattingFoodMetaData(menu_tag=menu_tag, station=station, food_item=food_item))
                    curr_element = curr_element.next_sibling
                    # function to extract meta data for each
    
                
