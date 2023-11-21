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

