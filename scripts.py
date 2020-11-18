#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.io import curdoc
from bokeh.models import HoverTool, Select, Div
from bokeh.plotting import figure, show, output_notebook,ColumnDataSource,curdoc
from bokeh.layouts import row, column
from bokeh.transform import dodge

state_total = pd.read_csv("latimes-state-totals.csv", parse_dates=['date'])


start_date = "2020-08-01"
end_date = "2020-08-31"
after_start_date = state_total["date"] >= start_date
before_end_date = state_total["date"] <= end_date
between_two_dates = after_start_date & before_end_date
filtered_month = state_total.loc[between_two_dates]

new_cases = filtered_month[["date","new_confirmed_cases"]]

case_plot = figure(x_axis_type='datetime',
             title='New Cases in August',
             plot_width=1400, plot_height=900,
             x_axis_label='Date', y_axis_label='New Cases'
            )


# In[2]:



case_plot.line('date', 'new_confirmed_cases', 
         color='red', legend='New Cases', 
         source=new_cases)
case_plot.circle('date', 'new_confirmed_cases', 
           fill_color="red", line_color='red', 
           size=8, source=new_cases)

case_plot.add_tools(HoverTool(tooltips=[
    ("new cases: ", "@new_confirmed_cases"),
    ("date: ","@date{%Y-%m-%d}"),],
    formatters = {'@date': 'datetime'}))

case_plot.legend.location = 'top_right'


# In[3]:





# In[ ]:





# In[4]:


race_data = pd.read_csv('cdph-race-ethnicity.csv')
race_data['date_time']=pd.to_datetime(race_data['date'])
race_data = race_data[race_data.age == "all"]
race_data = race_data[["date","date_time", "race","confirmed_cases_percent", "deaths_percent","population_percent"]]
race_data = race_data.set_index(['date_time'])

race_data.fillna("no record", inplace = True)

date_list = sorted(set(race_data.date), reverse=True)
sel_date = date_list[0]
races = ['asian', 'black', 'cdph-other', 'latino', 'other', 'white']
def get_dataset (date):
    df2 = race_data.loc[date]

    data = {'races' : races,
            'confirmed' : list(df2['confirmed_cases_percent']),
            'death' : list(df2['deaths_percent']),
            'population' : list(df2['population_percent'])
           }

    return ColumnDataSource(data=data)

def make_race_plot(source):
    p = figure(x_range=races, y_range=(0, 1), plot_height=250, title="Coronavirus cases and deaths percentage of each races in California",
               toolbar_location=None) #, tools="hover", tooltips="$name: @$name")

    p.vbar(x=dodge('races', -0.25, range=p.x_range), top='confirmed', width=0.2, source=source,
           color="blue", legend_label="confirmed percentage")

    p.vbar(x=dodge('races',  0.0,  range=p.x_range), top='death', width=0.2, source=source,
           color="red", legend_label="death percentage")

    p.vbar(x=dodge('races',  0.25, range=p.x_range), top='population', width=0.2, source=source,
           color="orange", legend_label="population percentage")

    p.add_tools(HoverTool(
        tooltips=[
            ("race", "@races"),
            ("confirmed", "@confirmed{0,0.000}"+"%"),
            ("death", "@death{0,0.000}"+"%"),
            ("population", "@population{0,0.000}"+"%"),

        ]
    ))
    p.x_range.range_padding = 0.1
    p.xgrid.grid_line_color = None
    p.legend.location = "top_right"
    p.legend.orientation = "horizontal"

    return p

def update_plot(attrname, old, new):
    src = get_dataset(date_select.value)
    source.data.update(src.data)

source = get_dataset (sel_date)
race_plot = make_race_plot(source)

date_select = Select(value=sel_date, title='Select Date', options=date_list)
date_select.on_change('value', update_plot)


# In[5]:


type(row(race_plot,date_select))


# In[9]:

div = Div(text="""<b>California State Covid-19 Case Visualization</b><br>
Data Source by California Department of Public Health daily release also accessible at <a href="https://github.com/datadesk/california-coronavirus-data">Github repository</a> with file names as cdph-state-totals.csv and cdph-race-etnicity.csv<br> 
<ul>
<li>Accumulative Cases and Deaths data (cdph-state-totals.csv) was originated from <a href="https://www.cdph.ca.gov/Programs/OPA/Pages/New-Release-2020.aspx">https://www.cdph.ca.gov/Programs/OPA/Pages/New-Release-2020.aspx</a></li>
<li>Race and etnicity data (cdph-race-etnicity.csv) was originated from <a href="https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/Race-Ethnicity.aspx">https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/Race-Ethnicity.aspx</a></li>
</ul>
Note: Downloaded the data from the source on <strong>November 6, 2020</strong><br>
<strong>New Cases in August line plot</strong><br>:
""",
width=1000, height=150)

div2 = Div(text="""
<h1> Histogram of Cases, deaths and population percentage of each race in California State</h1>
""")

curdoc().add_root(column(div,case_plot,div2,row(date_select, race_plot)))

