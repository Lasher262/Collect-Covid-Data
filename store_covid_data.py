import requests
import csv
import datetime
from datetime import date
from config_parser import CustomConfigParser as cp

class Covid19:
    """
    Collects current status of covid cases country-wise and stores them in a csv file.
    """

    def __init__(self, config):
        self.column_names = config.get("columns").split(",")
        self.output_file = config.get("out_csv")
        self.base_url = "https://api.covid19api.com/"

    def get_summary(self):
        """Returns country-wise summary"""
        response = requests.get(self.base_url+"summary")
        status = response.status_code
        if status != 200:
            print(status)
            exit()
        from_url = response.json()
        countries = from_url['Countries']
        return countries
    
    def get_details(self, countries):
        """Formats data"""
        data = []
        slug_ls = []        #to store slug of each country
        for i in range(len(countries)):
            # ls = [(datetime.datetime.strptime(countries[i]['Date'],"%Y-%m-%dT%H:%M:%SZ")).date(),countries[i]['Country'],countries[i]['TotalConfirmed'],countries[i]['TotalConfirmed']-countries[i]['TotalDeaths']-countries[i]['TotalRecovered'],countries[i]['TotalDeaths'],countries[i]['TotalRecovered']]
            ls = []
            for column in self.column_names:
                if column == "Date":
                    ls.append((datetime.datetime.strptime(countries[i][column],"%Y-%m-%dT%H:%M:%SZ")).date())
                elif column == "TotalActiveCases":
                    ls.append(countries[i]['TotalConfirmed']-countries[i]['TotalDeaths']-countries[i]['TotalRecovered'])
                else:
                    ls.append(countries[i][column])
            slug_ls.append(countries[i]['Slug'])
            data.append(ls)
        return data, slug_ls

    def get_no_of_days(self, slug_ls):
        """Fetches no of days since first case confirmed"""
        date_ls = []
        #for each country get first case confirmed date
        for i in slug_ls:
            url = self.base_url+"dayone/country/"+i+"/status/confirmed"
            response = requests.get(url)
            date_ls.append(response.json()[0]['Date'])
        
        t1 = date.today()
        days = []
        #Calculate 'days since first case' for each country
        for i in range(len(date_ls)):
            t2 = datetime.datetime.strptime(date_ls[i],"%Y-%m-%dT%H:%M:%SZ")
            days.append(str(t1-t2.date())[0:4])
        return days

    def update_list(self, data, days):
        """Appends no_of_days_since_first_confirmed_case to data"""
        j = 0
        for i in data:
            i.append(days[j])
            j+=1
        return data

    def write_to_csv(self, data):
        """Writes data to a csv file"""
        with open("out.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.column_names)
            writer.writerows(data)
            print(" Updated succesfully ")


if __name__ == "__main__":

    CONFIG = cp.config_parser('config.ini')

    obj = Covid19(CONFIG)
    countries = obj.get_summary()
    data, slug_ls = obj.get_details(countries)
    # no_of_days = obj.get_no_of_days(slug_ls)
    # updated_data = obj.update_list(data, no_of_days)
    obj.write_to_csv(data)
    