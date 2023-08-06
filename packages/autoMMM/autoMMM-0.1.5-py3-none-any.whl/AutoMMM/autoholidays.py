import pandas as pd
import holidays
from datetime import datetime

class HolidayExtractor:
    def __init__(self, country, start_date, end_date):
        self.country = country
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')
        self.holiday_dict = self.get_holidays_by_nation()

    def get_holidays_by_nation(self):
        holiday_dict = {}
        start_year, end_year = self.start_date.year, self.end_date.year
        for year in range(start_year, end_year + 1):
            for date, name in sorted(holidays.CountryHoliday(self.country, years=year).items()):
                holiday_dict[date] = name
        return holiday_dict
    
    def week_start_to_int(self, week_start):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return days.index(week_start)


    def get_holidays_by_region(self, region):
        regional_holiday_dict = {}
        start_year, end_year = self.start_date.year, self.end_date.year
        for year in range(start_year, end_year + 1):
            for date, name in sorted(holidays.CountryHoliday(self.country, prov=region, years=year).items()):
                regional_holiday_dict[date] = name
        return regional_holiday_dict

    def generate_timeseries(self, holiday_dict=None, week_start='Monday', custom_holiday_list=None):
        if holiday_dict is None:
            holiday_dict = self.holiday_dict

        week_start_int = self.week_start_to_int(week_start)

        date_range = pd.date_range(self.start_date, self.end_date, freq='D')
        timeseries_df = pd.DataFrame(date_range, columns=['Date'])

        timeseries_df['Week Commencing'] = timeseries_df['Date'] - pd.to_timedelta((timeseries_df['Date'].dt.weekday - week_start_int) % 7, unit='d')
        timeseries_df['Holiday'] = timeseries_df['Date'].map(holiday_dict)
        timeseries_df['Is Holiday'] = (timeseries_df['Holiday'].notna()).astype(int)

        if custom_holiday_list is not None:
            timeseries_df['Custom Holiday'] = timeseries_df['Holiday'].isin(custom_holiday_list).astype(int)

        weekly_timeseries_df = timeseries_df.groupby('Week Commencing').agg({'Is Holiday': 'sum', 'Custom Holiday': 'max'}).reset_index()

        weekly_timeseries_df['Weeks Since Last Holiday'] = 0
        last_holiday_week = None

        for index, row in weekly_timeseries_df.iterrows():
            if row['Is Holiday'] > 0:
                if last_holiday_week is not None:
                    weeks_since_last_holiday = (row['Week Commencing'] - last_holiday_week).days // 7
                    weekly_timeseries_df.at[index, 'Weeks Since Last Holiday'] = weeks_since_last_holiday
                last_holiday_week = row['Week Commencing']

        return weekly_timeseries_df
