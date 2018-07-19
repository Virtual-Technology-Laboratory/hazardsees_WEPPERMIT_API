from flask import Flask, jsonify, request
# from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Selenium automating browser to load JS
options = webdriver.ChromeOptions()
# options.add_argument('headless')
# driver = webdriver.Chrome(chrome_options=options)

driver = webdriver.Chrome() # <-- uncomment in the case that headless doesn't work
# BS4 trying to access these values
input_url = "https://forest.moscowfsl.wsu.edu/cgi-bin/fswepp/ermit/ermit.pl"
output_url = "https://forest.moscowfsl.wsu.edu/cgi-bin/fswepp/ermit/erm.pl"

driver.maximize_window()
driver.get(input_url)
time.sleep(3)

# content = driver.page_source.encode('utf-8').strip()
# soup = BeautifulSoup(content, 'html.parser')

# Extracting hillslope data based on USER INPUT to  ERMIT w/ BS4
# At this  point, BS seems totally unnecesary because Selenium offers the same data scraping functionality, so this has been refactored into selenium

# top_slope = int(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > b:nth-of-type(1) > input[type='text']")['value'])
# avg_slope = int(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > b:nth-of-type(2) > input[type='text']")['value'])
# toe_slope = int(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > b:nth-of-type(3) > input[type='text']")['value'])
# length_ft = int(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(3) > b > input[type='text']")['value'])
# cli_fn = soup.select_one("body > font > center > form > table > tbody > tr:nth-of-type(2) > td:nth-of-type(1) > select").find('option', selected=True)['value']
# severity = soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(4) > input[checked='checked']")['value']
# soil_type = soup.select_one("body > font > center > form > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > select").find('option', selected=True)['value']
# vegetation = soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(2) > td:nth-of-type(1) > select").find('option', selected=True)['value']
# rock_content = int(soup.select_one("body > font > center > form > table > tbody > tr:nth-of-type(4) > td > input[type='text']")['value'])
# pct_grass = str(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(4) > td:nth-of-type(2) > input[type='text']"))
# pct_shrub = str(soup.select_one("body > font > center > form > p > table > tbody > tr:nth-of-type(4) > td:nth-of-type(1) > input[type='text']"))

top_slope_form = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[2]/b[1]/input")
avg_slope_form = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[2]/b[2]/input")
toe_slope_form = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[2]/b[3]/input")
length_ft_form = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[3]/b/input")
pct_bare_form = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[4]/td[3]/input")
pct_grass_form = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[4]/td[2]/input")
pct_shrub_form = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[4]/td[1]/input")
rock_content_form = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[4]/td/input")


birmingham_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[1]/select/option[1]")
charleston_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[1]/select/option[2]")
denver_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[1]/select/option[3]")
flagstaff_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[1]/select/option[4]")
moscow_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[1]/select/option[5]")
mount_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[1]/select/option[6]")
sexton_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[1]/select/option[7]")
cli_fn_select = [birmingham_option, charleston_option, denver_option, flagstaff_option, moscow_option, mount_option, sexton_option]

clay_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[2]/select/option[1]")
silt_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[2]/select/option[2]")
sand_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[2]/select/option[3]")
loam_option = driver.find_element(By.XPATH, "/html/body/font/center/form/table/tbody/tr[2]/td[2]/select/option[4]")
soil_type_select = [clay_option, silt_option, sand_option, loam_option]

forest_option = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[1]/select/option[1]")
range_option = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[1]/select/option[2]")
chap_option = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[1]/select/option[3]")
vegetation_select = [forest_option, range_option, chap_option]

high_sev = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[4]/input[1]")
moderate_sev = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[4]/input[2]")
low_sev = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[4]/input[3]")
unburned_sev = driver.find_element(By.XPATH, "/html/body/font/center/form/p/table/tbody/tr[2]/td[4]/input[4]")
severity_radios = [high_sev, moderate_sev, low_sev, unburned_sev]

def get_input():

    top_slope = top_slope_form.get_attribute("value")
    avg_slope = avg_slope_form.get_attribute("value")
    toe_slope = toe_slope_form.get_attribute("value")
    length_ft = length_ft_form.get_attribute("value")
    pct_bare = pct_bare_form.get_attribute("value")
    pct_grass = pct_grass_form.get_attribute("value")
    pct_shrub = pct_shrub_form.get_attribute("value")
    rock_content = rock_content_form.get_attribute("value")
    cli_fn = cli_fn_select[0].get_attribute("value")
    soil_type = soil_type_select[0].get_attribute("value")
    vegetation = vegetation_select[0].get_attribute("value")
    severity = severity_radios[0].get_attribute("value")

    return {
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


def writeErmitValues():

    top_slope_form.clear()
    avg_slope_form.clear()
    toe_slope_form.clear()
    length_ft_form.clear()
    pct_bare_form.clear()
    pct_grass_form.clear()
    pct_shrub_form.clear()
    rock_content_form.clear()

    top_slope_form.send_keys(20)
    avg_slope_form.send_keys(20)
    toe_slope_form.send_keys(20)
    length_ft_form.send_keys(200)
    pct_bare_form.send_keys(20)
    pct_grass_form.send_keys(30)
    pct_shrub_form.send_keys(50)
    rock_content_form.send_keys(20)
    cli_fn_select[1].click()
    soil_type_select[1].click()
    vegetation_select[1].click()
    severity_radios[1].click()

def submitErmitValues():
    submit = driver.find_element(By.XPATH, "/html/body/font/center/form/p/input[3]")
    submit.click()

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def query_ermit():

    if request.method not in ['GET', 'POST']:
        return jsonify({"Error:", "Expecting GET or POST"})

    if request.method == 'POST':

        writeErmitValues()

        get_submitted_values = get_input()

        for key, value in get_submitted_values.items():
            if value is None:
                errors['%s Error' % key.capitalize()] = '%s not supplied' % key

        # I want to get this data from Angular Form and post it to the ermit site
        # Then I want to run the ERMiT procedure (selenium, "click" submit button (selector path:body > font > center > form > p > input[type="SUBMIT"]:nth-child(5))
        # TODO: Finish refactoring this to work with BS -> Selenium changes
        hillslope_input = run_ermit(top_slope, avg_slope, toe_slope, rock_content, length_ft,
                  cli_fn, severity, soil_type,
                  vegetation, pct_grass=None, pct_shrub=None)

        submitErmitValues()

        if errors:
            return jsonify(errors, hillslope_input)

        return jsonify(hillslope_data)


    if request.method == 'GET':

        writeErmitValues()

        get_submitted_values = get_input()

        for key, value in get_submitted_values.items():
            if value is None:
                errors['%s Error' % key.capitalize()] = '%s not supplied' % key

        # I want to run this with the ERMIT output (after it has processed the Angular Form input),
        # then shoot this data over to the JS visualization thing


        submitErmitValues()

        return jsonify(get_submitted_values)

if __name__ == '__main__':
    app.run()
