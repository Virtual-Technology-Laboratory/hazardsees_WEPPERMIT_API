from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

# Selenium automating browser to load JS
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

# driver = webdriver.Chrome() # <-- uncomment in the case that headless doesn't work
# BS4 trying to access these values
url= "https://forest.moscowfsl.wsu.edu/cgi-bin/fswepp/ermit/ermit.pl"
driver.maximize_window()
driver.get(url)
time.sleep(5)

content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content, 'html.parser')
# return str(soup) #Shows entire ERMIT app

# Extracting hillslope data from ERMIT w/ BS4
top_slope = int(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > b:nth-of-type(1) > input[type='text']")['value'])
avg_slope = int(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > b:nth-of-type(2) > input[type='text']")['value'])
toe_slope = int(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > b:nth-of-type(3) > input[type='text']")['value'])
length_ft = int(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(3) > b > input[type='text']")['value'])
cli_fn = soup.select_one("body > font > center > form > table > tbody > tr:nth-of-type(2) > td:nth-of-type(1) > select").find('option', selected=True)['value']
severity = soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(4) > input[checked='checked']")['value']
soil_type = soup.select_one("body > font > center > form > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > select").find('option', selected=True)['value']
vegetation = soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(1) > select").find('option', selected=True)['value']
rock_content = int(soup.select_one("body > font > center > form > table > tbody > tr:nth-of-type(4) > td > input[type='text']")['value'])
pct_grass = str(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2) > input[type='text']"))
pct_shrub = str(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(4) > td:nth-of-type(1) > input[type='text']"))
# TODO: Don't know how to pull data from grass and shrub (because it is calculated based on js function onchange)

# Returning errors given that any of these attributes are not found
attributes = {
    "top_slope": top_slope,
    "avg_slope": avg_slope,
    "toe_slope": toe_slope,
    "length_ft": length_ft,
    "cli_fn": cli_fn,
    "severity": severity,
    "soil_type": soil_type,
    "vegetation": vegetation,
    "rock_content": rock_content,
    "pct_grass": pct_grass,
    "pct_shrub": pct_shrub
    }

errors = {}

def run_ermit(top_slope, avg_slope, toe_slope, rock_content, length_ft,
              cli_fn, severity, soil_type,
              vegetation, pct_grass=None, pct_shrub=None):

    assert 0 <= top_slope <= 100
    assert 0 <= avg_slope <= 100
    assert 0 <= toe_slope <= 100

    assert 0 <= rock_content <= 50

    assert length_ft >= 0

    if length_ft > 300.0:
        length_ft = 300.0

    assert severity in ['l', 'm', 'h', 'u']
    assert soil_type in ['clay', 'silt', 'sand', 'loam']
    assert vegetation in ['forest', 'range', 'chap']

    if vegetation == 'forest':
        pct_grass = ''
        pct_shrub = ''
        pct_bare = ''
    elif vegetation == 'range':
        pct_grass = 75
        pct_shrub = 15
        pct_bare = 10
    elif vegetation == 'chap':
        pct_grass = 0
        pct_shrub = 80
        pct_bare = 20
    else:
        assert isfloat(pct_grass)
        assert isfloat(pct_shrub)
        assert 0 <= pct_grass <= 100.0
        assert 0 <= pct_shrub <= 100.0
        assert 0 <= pct_shrub + pct_grass <= 100.0
        pct_bare = 100.0 - pct_shrub - pct_grass

    return dict(achtung='Run+WEPP',
            actionw='Running+ERMiT...',
            top_slope=top_slope,
            avg_slope=avg_slope,
            toe_slope=toe_slope,
            Climate='../climates/' + cli_fn,
            climate_name='',
            debug='',
            length=length_ft,
            me='',
            pct_bare=pct_bare,
            pct_grass=pct_grass,
            pct_shrub=pct_shrub,
            rfg=20,
            severity=severity,
            SoilType=soil_type,
            units='ft',
            Units='m',
            vegetation=vegetation,
            rock_content=rock_content)

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def query_ermit():
    if request.method not in ['GET', 'POST']:
        return jsonify({"Error:", "Expecting GET or POST"})

    if request.method == 'POST':
        for key, value in attributes.items():
            if value is None:
                errors['%s Error' % key.capitalize()] = '%s not supplied' % key

        # I want to get this data from Angular Form and post it to the ermit site
        # Then I want to run the ERMiT procedure (selenium, "click" submit button (selector path:body > font > center > form > p > input[type="SUBMIT"]:nth-child(5))
        hillslope_data = run_ermit(top_slope, avg_slope, toe_slope, rock_content, length_ft,
                  cli_fn, severity, soil_type,
                  vegetation, pct_grass=None, pct_shrub=None)

        if errors:
            return jsonify(errors, hillslope_data)

        return jsonify(hillslope_data)

    if request.method == 'GET':

        for key, value in attributes.items():
            if value is None:
                errors['%s Error' % key.capitalize()] = '%s not supplied' % key

        # I want to run this with the ERMIT output (after it has processed the Angular Form input),
        # then shoot this data over to the JS visualization thing
        hillslope_data = run_ermit(top_slope, avg_slope, toe_slope, rock_content, length_ft,
                  cli_fn, severity, soil_type,
                  vegetation, pct_grass=None, pct_shrub=None)

        if errors:
            return jsonify(errors, hillslope_data)

        return jsonify(hillslope_data)

if __name__ == '__main__':
    app.run()
