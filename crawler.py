from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.common.by import By
from collections import defaultdict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd


url = 'https://www.espn.in/football/fixtures'

src = webdriver.chrome.service.Service(executable_path=binary_path)
driver = webdriver.Chrome(service=src)

home_data = defaultdict(lambda : None)
away_data = defaultdict(lambda : None)
driver.get(url)

# data
data = {
    "home_club_name": [],
    "away_goal_mean": [],
    "away_goal_std": [],
    "away_assist_mean": [],
    "away_assist_std": [],
    "home_club_name": [],
    "home_goal_mean": [],
    "home_goal_std": [],
    "home_assist_mean": [],
    "home_assist_std":[]
}

data = pd.DataFrame(data)


try:
    sleep(15)
    wait = WebDriverWait(driver, 10)

    league_boss = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/div/section/div/div[3]')))

    # print(league_boss)
    league_wait = WebDriverWait(league_boss, 5)
    leagues = league_wait.until(EC.visibility_of_all_elements_located((By.XPATH, './div')))


    # print(leagues)

    for i in range(len(leagues)):
        league = leagues[i]
        league_name = league.find_element(By.CLASS_NAME, "Table__Title").text
        # print(league_name)
        # if league_name == ""
        # if league_name.strip() not in ["English Premier League", "English League Championship", "English League One", "English League Two", "English FA Cup", "French Ligue 1", "Spanish LALIGA", "Italian Serie A", "German Bundesliga", "Irish Premier Division", "UEFA Europa Conference League", "UEFA Champions League", "UEFA Europa League", "English FA Cup", "MLS", "English Carabao Cup"]:
        #     continue
        matches = league.find_elements(By.CLASS_NAME, 'Table__TR.Table__TR--sm.Table__even')
        # print("leagues and matches read")
        for j in range(len(matches)):
            match = matches[j]
            home_team = match.find_element(By.CLASS_NAME, 'events__col.Table__TD')
            # print(driver.window_handles)
            away_team = match.find_element(By.CLASS_NAME, 'colspan__col.Table__TD')
            away_team_name = away_team.text.strip()
            home_team_name = home_team.text.strip()
            print(home_team_name, away_team_name, league_name)
            if away_team_name[0] == "v":
                away_team_name = away_team_name.split()
                away_team_name.pop(0)
                away_team_name = " ".join(away_team_name)
                if away_team_name != "TBD" and home_team_name != "TBD":
                    driver.get(WebDriverWait(home_team,10).until(EC.visibility_of_element_located((By.XPATH, "./div/span/a[2]"))).get_attribute("href"))
                    sleep(15)
                    # print("home team clicked")
                    # driver.refresh()
                    wait = WebDriverWait(driver, 10)
                    all_buttons = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/div[2]/nav/ul/li')
                    
                    for button in all_buttons:
                        if button.text == "Squad":
                            button.find_element(By.XPATH, "./a").click()
                            break
                    # talha script
                    sleep(15)
                    wait = WebDriverWait(driver, 5)
                    Table_name = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,'Table__Title')))
                    if Table_name[0].text!='No Data Available':

                        # Locate the dropdown element using its ID, name, XPath, or other locator
                        squad_rows = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME,'tr')))


                        # Loop through each row and extract the data
                        for row in squad_rows:

                            player=cells = row.find_elements(By.TAG_NAME, "td")

                            if len(player)>0:
                                a=player[0]
                                s=''
                                for ele in a.text:
                                    if ele>='0' and ele<='9':
                                        pass
                                    else:
                                        s+=ele
                                
                                letters_part = s
                                
                                player_name=letters_part;player_pos=player[1].text
                                if player_pos!='AGE':
                                    if player_pos!= "G" and player_pos != "D":
                                        goals=player[8].text
                                        if goals=='--':
                                            goals=0
                                        assist=player[9].text
                                        if assist=='--':
                                            assist=0
                                        matches=player[6].text
                                        if matches=='--':
                                            matches=0
                                        home_data[player_name] = [int(matches),player_pos,int(goals),int(assist)]

                        if len(squad_rows) != 0:

                            dropdown = Select(driver.find_element(By.XPATH, '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/section/div[3]/div/select[1]'))

                            num_options = len(dropdown.options)
                            if num_options>1:
                                dropdown_element = driver.find_element(By.XPATH, '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/section/div[3]/div/select[1]')
                                dropdown_element.click()
                                index = 1
                                dropdown.select_by_index(index)
                                sleep(15)
                                squad_rows = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME,'tr')))


                                # Loop through each row and extract the data
                                for row in squad_rows:

                                    player=cells = row.find_elements(By.TAG_NAME, "td")
                                    
                                    if len(player)>0:
                                        a=player[0]
                                        s=''
                                        for ele in a.text:
                                            if ele>='0' and ele<='9':
                                                pass
                                            else:
                                                s+=ele
                                        
                                        letters_part = s
                                        
                                        player_name=letters_part;player_pos=player[1].text
                                        if player_pos!='AGE':
                                            if player_pos!= "G" and player_pos != "D" and home_data[player_name] != None:

                                                goals=player[8].text
                                                if goals=='--':
                                                    goals=0
                                                assist=player[9].text
                                                if assist=='--':
                                                    assist=0
                                                matches=player[6].text
                                                if matches=='--':
                                                    matches=0
                                                home_data[player_name][0] += int(matches)
                                                home_data[player_name][2] += int(goals)
                                                home_data[player_name][3] += int(assist)
                            # print(home_data)
                    # talha script end

                    
                    driver.get(url)

                    sleep(15)
                    wait = WebDriverWait(driver, 10)
                    league_boss = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/div/section/div/div[3]')))

                    league_wait = WebDriverWait(league_boss, 5)
                    leagues = league_wait.until(EC.visibility_of_all_elements_located((By.XPATH, './div')))
                    league = leagues[i]
                    matches = league.find_elements(By.CLASS_NAME, 'Table__TR.Table__TR--sm.Table__even')
                    match = matches[j]
                    # print("leagues and matches read again")


                    away_team = match.find_element(By.CLASS_NAME, 'colspan__col.Table__TD')
                    driver.get(WebDriverWait(away_team, 10).until(EC.visibility_of_element_located((By.XPATH, "./div/span/a[2]"))).get_attribute("href"))
                    sleep(15)
                    # print("away team clicked")
                    
                    wait = WebDriverWait(driver, 10)
                    all_buttons = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div/main/div[2]/div[2]/nav/ul/li')
                    
                    # print(all_buttons)
                    for button in all_buttons:
                        # print("Button text=",button.text)
                        if button.text == "Squad":
                            
                            button.find_element(By.XPATH, "./a").click()
                            break
                    # Talha script
                    sleep(15)

                    wait = WebDriverWait(driver, 5)
                    Table_name = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,'Table__Title')))
                    if Table_name[0].text!='No Data Available':

                        # Locate the dropdown element using its ID, name, XPath, or other locator
                        squad_rows = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME,'tr')))


                        # Loop through each row and extract the data
                        for row in squad_rows:

                            player=cells = row.find_elements(By.TAG_NAME, "td")

                            if len(player)>0:
                                a=player[0]
                                s=''
                                for ele in a.text:
                                    if ele>='0' and ele<='9':
                                        pass
                                    else:
                                        s+=ele
                                
                                letters_part = s
                                
                                player_name=letters_part;player_pos=player[1].text
                                if player_pos!='AGE':
                                    if player_pos!= "G" and player_pos != "D":
                                        goals=player[8].text
                                        if goals=='--':
                                            goals=0
                                        assist=player[9].text
                                        if assist=='--':
                                            assist=0
                                        matches=player[6].text
                                        if matches=='--':
                                            matches=0
                                        away_data[player_name] = [int(matches),player_pos,int(goals),int(assist)]

                        if len(squad_rows) != 0:
                            dropdown = Select(driver.find_element(By.XPATH, '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/section/div[3]/div/select[1]'))

                            num_options = len(dropdown.options)
                            if num_options>1:
                                dropdown_element = driver.find_element(By.XPATH, '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/section/div[3]/div/select[1]')
                                dropdown_element.click()
                                index = 1
                                dropdown.select_by_index(index)
                                sleep(15)
                                squad_rows = wait.until(EC.visibility_of_all_elements_located((By.TAG_NAME,'tr')))


                                # Loop through each row and extract the data
                                for row in squad_rows:

                                    player=cells = row.find_elements(By.TAG_NAME, "td")
                                    
                                    if len(player)>0:
                                        a=player[0]
                                        s=''
                                        for ele in a.text:
                                            if ele>='0' and ele<='9':
                                                pass
                                            else:
                                                s+=ele
                                        
                                        letters_part = s
                                        
                                        player_name=letters_part;player_pos=player[1].text
                                        if player_pos!='AGE':
                                            if player_pos!= "G" and player_pos != "D" and away_data[player_name] != None:

                                                goals=player[8].text
                                                if goals=='--':
                                                    goals=0
                                                assist=player[9].text
                                                if assist=='--':
                                                    assist=0
                                                matches=player[6].text
                                                if matches=='--':
                                                    matches=0
                                                away_data[player_name][0] += int(matches)
                                                away_data[player_name][2] += int(goals)
                                                away_data[player_name][3] += int(assist)
                            # print(away_data)


                    # talha script end
                    
                    # saving the data
                    
                    dummy_df1 = {"name": [], "goal_ratio": [], "assist_ratio": []}
                    
                    for name, info in home_data.items():
                        if home_data[name] != None and home_data[name][0] != 0:
                            dummy_df1["name"].append(name)
                            dummy_df1["goal_ratio"].append(info[2]/info[0])
                            dummy_df1["assist_ratio"].append(info[3]/info[0])
                    
                    dummy_df2 = {"name": [], "goal_ratio": [], "assist_ratio": []}
                    
                    for name, info in away_data.items():
                        if away_data[name] != None and away_data[name][0] != 0:
                            dummy_df2["name"].append(name)
                            dummy_df2["goal_ratio"].append(info[2]/info[0])
                            dummy_df2["assist_ratio"].append(info[3]/info[0])

                    dummy_df1 = pd.DataFrame(dummy_df1)
                    dummy_df2 = pd.DataFrame(dummy_df2)
                    print(dummy_df1)
                    print(dummy_df2)
                    
                    
                    
                    data = pd.concat([data, pd.DataFrame({
                        "home_club_name": [home_team_name],
                        "away_goal_mean": [dummy_df2["goal_ratio"].mean()],
                        "away_goal_std": [dummy_df2["goal_ratio"].std()],
                        "away_assist_mean": [dummy_df2["assist_ratio"].mean()],
                        "away_assist_std": [dummy_df2["assist_ratio"].std()],
                        "away_club_name": [away_team_name],
                        "home_goal_mean": [dummy_df1["goal_ratio"].mean()],
                        "home_goal_std": [dummy_df1["goal_ratio"].std()],
                        "home_assist_mean": [dummy_df1["assist_ratio"].mean()],
                        "home_assist_std":[dummy_df1["assist_ratio"].std()]
                    })],axis=0)

                    data.to_csv("new_ball_data.csv", index=False)

                    driver.get(url)
                    wait = WebDriverWait(driver, 10)
                    league_boss = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div[3]/div/div/section/div/div[3]')))

                    league_wait = WebDriverWait(league_boss, 10)
                    leagues = league_wait.until(EC.visibility_of_all_elements_located((By.XPATH, './div')))
                    league = leagues[i]
                    matches = league.find_elements(By.CLASS_NAME, 'Table__TR.Table__TR--sm.Table__even')
                    match = matches[j]
                    # print("Going to next")

except Exception as e:
    print(e)

driver.quit()








