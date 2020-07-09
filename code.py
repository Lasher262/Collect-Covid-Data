import requests
import csv
from datetime import date
import datetime

class covid19api:
    """
    Gets current status of covid cases country-wise.
    - "Country" 
    - "Total cases"
    - "Total active cases" 
    - "Total deaths" 
    - "Total recovered" 
    - "Days since first confirmed case"
    """

    def __init__(self):
        self.base_url = "https://api.covid19api.com/"

    def get_summary(self):
        response = requests.get(self.base_url+"summary")
        status = response.status_code
        if status != 200:
            print(status)
            exit()
        from_url = response.json()
        countries = from_url['Countries']
        return countries
    
    def get_details(self, countries):
        data = []
        slug_ls = []
        for i in range(len(countries)):
            ls = [(datetime.datetime.strptime(countries[i]['Date'],"%Y-%m-%dT%H:%M:%SZ")).date(),countries[i]['Country'],countries[i]['TotalConfirmed'],countries[i]['TotalConfirmed']-countries[i]['TotalDeaths']-countries[i]['TotalRecovered'],countries[i]['TotalDeaths'],countries[i]['TotalRecovered']]
            slug_ls.append(countries[i]['Slug'])
            data.append(ls)
        return data, slug_ls

    def get_no_of_days(self, slug_ls):
        date_ls = []
        for i in slug_ls:
            url = self.base_url+"dayone/country/"+i+"/status/confirmed"
            response = requests.get(url)
            date_ls.append(response.json()[0]['Date'])
        
        t1 = date.today()
        days = []
        for i in range(len(date_ls)):
            t2 = datetime.datetime.strptime(date_ls[i],"%Y-%m-%dT%H:%M:%SZ")
            days.append(str(t1-t2.date())[0:4])
        return days

    def write_to_csv(self, data):
        with open("out.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Country", "Total cases","Total active cases", "Total deaths", "Total recovered", "Days since first confirmed case"])
            writer.writerows(data)
            print(" Updated succesfully ")

    def update_list(self, data, days):
        j = 0
        for i in data:
            i.append(days[j])
            j+=1
        return data


if __name__ == "__main__":
    covid = covid19api()
    countries = covid.get_summary()
    data, slug_ls = covid.get_details(countries)
    no_of_days = covid.get_no_of_days(slug_ls)
    updated_data = covid.update_list(data, no_of_days)
    covid.write_to_csv(updated_data)
    