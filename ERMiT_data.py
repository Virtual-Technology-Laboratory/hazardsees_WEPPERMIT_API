from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium import webdriver
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from percent_slope_to_coordinates import Slopes

# def run_ermit(top_slope, avg_slope, toe_slope, rock_content, length_ft,
#               cli_fn, severity, soil_type,
#               vegetation, pct_grass=None, pct_shrub=None):
#
#     assert 0 <= top_slope <= 100
#     assert 0 <= avg_slope <= 100
#     assert 0 <= toe_slope <= 100
#
#     assert 0 <= rock_content <= 50
#
#     assert length_ft >= 0
#
#     if length_ft > 300.0:
#         length_ft = 300.0
#
#     assert severity in ['l', 'm', 'h', 'u']
#     assert soil_type in ['clay', 'silt', 'sand', 'loam']
#     assert vegetation in ['forest', 'range', 'chap']
#
#     if vegetation == 'forest':
#         pct_grass = ''
#         pct_shrub = ''
#         pct_bare = ''
#     elif vegetation == 'range':
#         pct_grass = 75
#         pct_shrub = 15
#         pct_bare = 10
#     elif vegetation == 'chap':
#         pct_grass = 0
#         pct_shrub = 80
#         pct_bare = 20
#     else:
#         assert isfloat(pct_grass)
#         assert isfloat(pct_shrub)
#         assert 0 <= pct_grass <= 100.0
#         assert 0 <= pct_shrub <= 100.0
#         assert 0 <= pct_shrub + pct_grass <= 100.0
#         pct_bare = 100.0 - pct_shrub - pct_grass
#
#     return dict(achtung='Run+WEPP',
#             actionw='Running+ERMiT...',
#             top_slope=top_slope,
#             avg_slope=avg_slope,
#             toe_slope=toe_slope,
#             Climate='../climates/' + cli_fn,
#             climate_name='',
#             debug='',
#             length=length_ft,
#             me='',
#             pct_bare=pct_bare,
#             pct_grass=pct_grass,
#             pct_shrub=pct_shrub,
#             rfg=20,
#             severity=severity,
#             SoilType=soil_type,
#             units='ft',
#             Units='m',
#             vegetation=vegetation,
#             rock_content=rock_content)

app = Flask(__name__)
CORS(app)
@app.route('/', methods=['GET', 'POST'])
def query_ermit():

    if request.method not in ['GET', 'POST']:
        return jsonify({"Error:", "Expecting GET or POST"})

    if request.method == 'POST':

        errors = {}

        def writeErmitValues(top_slope_num, avg_slope_num, toe_slope_num, length_ft_num, pct_bare_num, pct_grass_num, pct_shrub_num, rock_content_num, cli_select_num, soil_select_num, veg_select_num, sev_radio_num):
            top_slope_form.clear()
            avg_slope_form.clear()
            toe_slope_form.clear()
            length_ft_form.clear()
            pct_bare_form.clear()
            pct_grass_form.clear()
            pct_shrub_form.clear()
            rock_content_form.clear()

            top_slope_form.send_keys(top_slope_num)
            avg_slope_form.send_keys(avg_slope_num)
            toe_slope_form.send_keys(toe_slope_num)
            length_ft_form.send_keys(length_ft_num)
            pct_bare_form.send_keys(pct_bare_num)
            pct_grass_form.send_keys(pct_grass_num)
            pct_shrub_form.send_keys(pct_shrub_num)
            rock_content_form.send_keys(rock_content_num)
            cli_fn_select[cli_select_num].click()
            soil_type_select[soil_select_num].click()
            vegetation_select[veg_select_num].click()
            severity_radios[sev_radio_num].click()

        def getInputValues(cli_select_num, soil_select_num, veg_select_num, sev_radio_num):
            top_slope = top_slope_form.get_attribute("value")
            avg_slope = avg_slope_form.get_attribute("value")
            toe_slope = toe_slope_form.get_attribute("value")
            length_ft = length_ft_form.get_attribute("value")
            pct_bare = pct_bare_form.get_attribute("value")
            pct_grass = pct_grass_form.get_attribute("value")
            pct_shrub = pct_shrub_form.get_attribute("value")
            rock_content = rock_content_form.get_attribute("value")
            cli_fn = cli_fn_select[cli_select_num].get_attribute("value")
            soil_type = soil_type_select[soil_select_num].get_attribute("value")
            vegetation = vegetation_select[veg_select_num].get_attribute("value")
            severity = severity_radios[sev_radio_num].get_attribute("value")

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
                "pct_shrub": pct_shrub,
                "pct_bare": pct_bare
                }

        def submitErmitValues():
            submit = driver.find_element(By.XPATH, "/html/body/font/center/form/p/input[3]")
            submit.click()

        def retrieveErmitValues():
            annual_precipitation = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[3]/td[1]/b").text
            annual_runoff_rain = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[4]/td[1]/b").text
            annual_runoff_winter = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[5]/td[1]/b").text
            storm_number = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[3]/td[4]").text
            rain_events = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[4]/td[4]").text
            winter_events = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[5]/td[4]").text
            prob_sediment_yield_exceeded = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/form/table/tbody/tr[2]/th[1]/input").get_attribute("value")

            return {
                "annual_precipitation": annual_precipitation,
                "annual_runoff_rain": annual_runoff_rain,
                "annual_runoff_winter": annual_runoff_winter,
                "storm_number": storm_number,
                "rain_events": rain_events,
                "winter_events": winter_events,
                "prob_sediment_yield_exceeded": prob_sediment_yield_exceeded
                }

        input_dict = request.json

        top_slope_num = input_dict['top_slope']
        avg_slope_num = input_dict['avg_slope']
        toe_slope_num = input_dict['toe_slope']
        length_ft_num = input_dict['length_ft']
        pct_bare_num = input_dict['pct_bare']
        pct_grass_num = input_dict['pct_grass']
        pct_shrub_num = input_dict['pct_shrub']
        rock_content_num = input_dict['rock_content']

        cli_str = input_dict['cli_fn']
        cli_choices_dict = {
            "../climates/al010831": 0,
            "../climates/wv461570": 1,
            "../climates/co052220": 2,
            "../climates/az023010": 3,
            "../climates/id106152": 4,
            "../climates/ca045983": 5,
            "../climates/or357698": 6
        }
        cli_select_num = cli_choices_dict[cli_str]

        sev_char = input_dict['severity']
        sev_choices_dict = {
            'h': 0,
            'm': 1,
            'l': 2,
            'u': 3,
        }
        sev_radio_num = sev_choices_dict[sev_char]

        soil_string = input_dict['soil_type']
        soil_choices_dict = {
            "clay": 0,
            "silt": 1,
            "sand": 2,
            "loam": 3
        }
        soil_select_num = soil_choices_dict[soil_string]

        veg_string = input_dict['vegetation']
        veg_choices_dict = {
                "forest": 0,
                "range": 1,
                "chap": 2
        }
        veg_select_num = veg_choices_dict[veg_string]

        print("POST works")

        # Selenium automating browser to load JS
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chrome_options=options)

        # driver = webdriver.Chrome() # <-- uncomment in the case that headless doesn't work
        input_url = "https://forest.moscowfsl.wsu.edu/cgi-bin/fswepp/ermit/ermit.pl"
        output_url = "https://forest.moscowfsl.wsu.edu/cgi-bin/fswepp/ermit/erm.pl"

        driver.maximize_window()
        driver.get(input_url)
        time.sleep(2)

        #ERMiT INPUT values
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

        writeErmitValues(top_slope_num, avg_slope_num, toe_slope_num, length_ft_num, pct_bare_num, pct_grass_num, pct_shrub_num, rock_content_num, cli_select_num, soil_select_num, veg_select_num, sev_radio_num)

        sent_data = getInputValues(cli_select_num, soil_select_num, veg_select_num, sev_radio_num)

        for key, value in sent_data.items():
            if value is None:
                errors['%s Error' % key.capitalize()] = '%s not supplied' % key

        submitErmitValues()

        print("SUBMIT DATA works")

        # ERMiT OUTPUT values
        time.sleep(2)

        # ERMiT response values after the site input gets processed
        annual_precipitation = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[3]/td[1]/b")
        annual_runoff_rain = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[4]/td[1]/b")
        annual_runoff_winter = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[5]/td[1]/b")
        storm_number = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[3]/td[4]")
        rain_events = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[4]/td[4]")
        winter_events = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/table/tbody/tr[5]/td[4]")
        prob_sediment_yield_exceeded = driver.find_element(By.XPATH, "/html/body/font/blockquote/center/center/form/table/tbody/tr[2]/th[1]/input")

        returned_data = retrieveErmitValues()

        print("RETRIEVE DATA works")

        hillslope = Slopes(top_slope_num, avg_slope_num, toe_slope_num, 0, 0, length_ft_num)
        hillslope.slope_calculations()

        coordinates = hillslope.current_data()

        print("COORDINATE CALC works")

        all_data = dict(sent_data, **returned_data, **coordinates)

        print("JSONIFY DATA works")
        print(all_data)

        resp = jsonify(all_data)
        resp.status_code = 200
        resp.headers['Link'] = 'localhost:4200'

        return resp

    if request.method == 'GET':
        return "get is invoked"

if __name__ == '__main__':
    app.run()
