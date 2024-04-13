# imports
from flask import Flask, render_template
import fandom
from mediawiki import MediaWiki
import re

# Setting the wiki I want to use
fandom.set_wiki("rct")

# Here I am getting to the RCT 2 Game with all the rides listed
fandom.search("Tycoon")
page = fandom.page(title = "RollerCoaster Tycoon 2")

# I have to use Media Wiki to get the proper image urls
rct_fandom = MediaWiki(url='https://rct.fandom.com/api/php')
rct2 = rct_fandom.page('RollerCoaster Tycoon 2')
rct2Images = rct2.images

# This is here for the first load
temp_list = []

def getAttraction(attaction):
    temp = page.section(attaction)
    temp_list = [line.replace('RCT2 Icon','') for line in temp.split('\n')[1:]]
    processed_entries = []
    processed_entries = process_entries(temp_list)
    return processed_entries

def process_entries(entries):
    # Process each entry and create key-value pairs
    result = [process_entry(entry) for entry in entries]
    return result

# ``````````````````````````````````````````````````````````````
def process_entry(entry):
    count = 0
    parCheck = 0
    name = ''
    game = ''
    ride_type = ''
    imgURL = ''

    for char in entry:
        if char == '(':
            count +=1
            
    if count == 1:
        ride_type = re.search(r'\(([^)]+)\)', entry).group(1)
        end_index = entry.find(')')
        game = entry[end_index + 1:].strip()
        name = entry.split('(')[0].strip()
        imgURL = assignImage(name)
    elif count == 2:
        for index, par in enumerate(entry):
            if par == '(':
                start_index = index + 1
            elif par == ')':
                end_index = index
                parCheck += 1
                if parCheck == 2:
                    ride_type = entry[start_index:end_index]
                    game = entry[end_index + 1:].strip()
    elif count == 3:
        parts = entry.split('(')
        if len(parts) >= 4:
            ride_type = parts[2].split(')')[0].strip()
            game = parts[3].split(')')[1].strip()     
    elif count == 4:
        parts = entry.split('(')
        if len(parts) >= 5:
            ride_type = parts[3].split(')')[0].strip(')')
            game = parts[4].split(')')[1].strip()        

    # Create key-value pair
    return {'name': name, 'ride_type': ride_type, 'game': game, 'imageURL': imgURL}
# ````````````````````````````````````````````````````````````

def assignImage(name):
    picURL = ''
    for pic in rct2Images:
        first_split = pic.split('/', 7)
        second_part = first_split[-1]
        final_split = second_part.split('_RCT')
        result = final_split[0]
        result = result.replace("_", " ")
        if name == result:
            dot_index = pic.rfind('.')
            picURL = pic[:dot_index + 4]
            break
    return picURL

app = Flask(__name__)

@app.route('/transportrides')
def transportrides():
    attractions = getAttraction('Transport Rides ')
    return attractions

@app.route('/gentlerides')
def gentlerides():
    attractions = getAttraction('Gentle Rides ')
    return attractions

@app.route('/rollercoasters')
def rollercoasters():
    attractions = getAttraction('Roller Coasters ')
    return attractions

@app.route('/thrillrides')
def thrillrides():
    attractions = getAttraction('Thrill Rides ')
    return attractions

@app.route('/waterrides')
def waterrides():
    attractions = getAttraction('Water Rides ')
    return attractions

@app.route('/shops_stalls')
def shops_stalls():
    attractions = getAttraction('Shops & Stalls ')
    return attractions

# ````````````````````````````````````````````````````````````````
# These serve a web page

@app.route('/page/transportrides')
def transportrides_Page():
    attractions = getAttraction('Transport Rides ')
    return render_template('index.html', data = attractions)

@app.route('/page/gentlerides')
def gentlerides_Page():
    attractions = getAttraction('Gentle Rides ')
    return render_template('index.html', data = attractions)

@app.route('/page/rollercoasters')
def rollercoasters_Page():
    attractions = getAttraction('Roller Coasters ')
    return render_template('index.html', data = attractions)

@app.route('/page/thrillrides')
def thrillrides_Page():
    attractions = getAttraction('Thrill Rides ')
    return render_template('index.html', data = attractions)

@app.route('/page/waterrides')
def waterrides_Page():
    attractions = getAttraction('Water Rides ')
    return render_template('index.html', data = attractions)

@app.route('/page/shops_stalls')
def shops_stalls_Page():
    attractions = getAttraction('Shops & Stalls ')
    return render_template('index.html', data = attractions)

if __name__ == '__main__':
    app.run()