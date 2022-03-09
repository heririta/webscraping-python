import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs4

continents_page = requests.get(
    "https://simple.wikipedia.org/wiki/List_of_countries_by_continents").text
# print(continents_page)


continents_countries_soup = bs4(continents_page, "lxml")
# <span class="mw-headline" id="Africa">Africa</span>
continents = continents_countries_soup.find_all(
    'h2' > 'span', {"class": "mw-headline"})
# print(continents)

unwanted_words = ["Antarctica", "Oceania", "References", "Other websites", ]
target_continents = [
    continents.text for continents in continents if continents.text not in unwanted_words]
# print(target_continents)


# <ol>
#     <li><a href="/wiki/Algeria" title="Algeria">Algeria</a> - <a href="/wiki/Algiers" title="Algiers">Algiers</a></li>
ol_html = continents_countries_soup.find_all('ol')
all_countries = [countries.find_all(
    'li', {"class": None, "id": None}) for countries in ol_html]
# print(all_countries)


# <li><a href="/wiki/Sulawesi" title="Sulawesi">Sulawesi</a></li>, <li><a href="/wiki/Sumbawa" title="Sumbawa">Sumbawa</a></li>,
countries_in_continents = []
for items in all_countries:
    countries = []
    if items:
        for country in items:
            countries = [country.find(
                'a').text for country in items if country.find('a')]
        countries_in_continents.append(countries)
# print(countries_in_continents)

countries_continent_category_df = pd.DataFrame(
    zip(countries_in_continents, target_continents), columns=['Country', 'Continent'])
# print(countries_continent_category_df)

countries_continent_category_df = countries_continent_category_df.explode(
    'Country').reset_index(drop=True)
# print(countries_continent_category_df)




countries_score_page = requests.get(
    "https://en.wikipedia.org/wiki/World_Happiness_Report#2020_report")
countries_score_soup = bs4(countries_score_page.content, 'lxml')
# print(countries_score_soup)

countries_score_table = countries_score_soup.find('table',{"class":"wikitable"})
# print(countries_score_table)

countries_score_df = pd.read_html(str(countries_score_table))
# print(countries_score_df)

countries_score_df = countries_score_df[0]
countries_score_df = countries_score_df.rename(columns={"Country or region" : "Country"})
# print(countries_score_df)

merged_df = pd.merge(countries_score_df, countries_continent_category_df, how='inner', on='Country')
merged_df.to_csv('final_result.csv')


