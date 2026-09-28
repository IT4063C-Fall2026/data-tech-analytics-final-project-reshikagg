#!/usr/bin/env python
# coding: utf-8

# # {The Relationship Between Educational Achievements and Quality of Life in Rural Nepal}📝
# 
# ![Banner](./assets/banner.jpeg)

# ## Education and Quality of Life in Rural Communities in Nepal
# *What problem are you (or your stakeholder) trying to address?*
# 📝 <!-- Answer Below -->
# The problem I want to look into is whether there is a correlation between educational achievements and the quality of life in rural communities in Nepal. In the rural communities, many families have difficulty with poverty, hard land, and limited schools. There are government groups and non-profit organizations that help out money towards education, hoping that it will help lead to a better life for families. But we do not really know whether going to school is leading people to a better life in rural areas, like higher wealth, better jobs, or basic needs.

# ## Project Question
# *What specific question are you seeking to answer with this project?*
# *This is not the same as the questions you ask to limit the scope of the project.*
# 📝 <!-- Answer Below -->
# 1. Is higher educational achievement associated with employment status among adults in rural Nepal?
# 2. Which quality of life factor has the strongest relationship with educational achievement?
# 3. Is educational achievement associated with access to basic household services?
# 4. How does household wealth vary across different levels of educational achievement?

# ## What would an answer look like?
# *What is your hypothesized answer to your question?*
# 📝 <!-- Answer Below -->
# I plan to use charts and statistics to answer my questions. 
# 
# For the relationship between household wealth and educational achievement, I can create a boxplot/scatter plot. This can show whether households with higher educational achievement have different wealth levels.
# 
# For education and employment, I can create a grouped bar chart that compares the percentage of working adults in different employment types.
# 
# For education and access to basic services, I will create a stacked bar chart that compares the percentage of the different education groups to their access to electricity, drinking water, or sanitation.

# ## Data Sources
# *What 3 data sources have you identified for this project?*
# *How are you going to relate these datasets?*
# 📝 <!-- Answer Below -->
# 1. Nepal Demographic and Health Survey (2022) - This is the main dataset for education, household wealth, location, employment, and household services.
# 2. World Bank Data - Helps support information on education, employment, and poverty.
# 3. UNESCO Institute for Statistics - Supports education and educational achievement data.
# 
# The DHS data contains household information for each individual, while the World Bank and UNESCO datasets contain national-level economic and education indicators. I will aggregate the DHS household data by year (2022) and region, and connect the regional average to the World Bank and UNESCO datasets by year(2022) and country (Nepal) as the matching key.

# In[7]:


import pandas as pd
import urllib.request
import json


# SOURCE 1: Local Microdata File (.DTA)

dhs = pd.read_stata(
    r"C:\Users\reshi\OneDrive\Desktop\Fall 2026\Data Tech Analytics\NPPR82FL.DTA"
)


# SOURCE 2: API Import (World Bank API via urllib)

wb_url = "http://api.worldbank.org/v2/country/NPL/indicator/NY.GDP.PCAP.CD?date=2015:2022&format=json"
req_wb = urllib.request.urlopen(wb_url)
wb_data = json.loads(req_wb.read().decode('utf-8'))[1]
worldbank_df = pd.DataFrame(wb_data)[['date', 'value']].rename(columns={'value': 'gdp_per_capita'})


# SOURCE 3: Web-Scraped / JSON Endpoint Data (UNESCO/SDG Indicator Data via urllib)

# Pulling SDG 4 / Education indicator JSON directly from web source
unesco_api_url = "http://api.worldbank.org/v2/country/NPL/indicator/SE.PRM.CMPT.ZS?date=2015:2022&format=json"
req_unesco = urllib.request.urlopen(unesco_api_url)
unesco_data = json.loads(req_unesco.read().decode('utf-8'))[1]
unesco_df = pd.DataFrame(unesco_data)[['date', 'value']].rename(columns={'value': 'primary_completion_rate'})


# Check all 3 distinct source operations

print("1. DHS File Shape:", dhs.shape)
print("2. World Bank API Shape:", worldbank_df.shape)
print("3. UNESCO / SDG Web Data Shape:", unesco_df.shape)


# ## Approach and Analysis
# *What is your approach to answering your project question?*
# *How will you use the identified data to answer your project question?*
# 📝 <!-- Start Discussing the project here; you can add as many code cells as you need -->
# I will begin by cleaning and organizing the DHS 2022 data and filtering to focus more on rural households in Nepal. I plan to group participants by their education and compare household wealth, employment status, and access to basic services. I plan to use charts, correlations, and statistics to identify any trends, patterns, or relationships. The DHS will be my main dataset; the World Bank and UNESCO will be used to support the information.

# In[1]:


# Start your code here


# ## Resources and References
# *What resources and references have you used for this project?*
# 📝 <!-- Answer Below -->
# 1. DHS Program :https://dhsprogram.com/data/dataset_admin/index.cfm 
# 2. World Bank: https://data.worldbank.org/country/nepal 
# 3. UNESCO UIS: https://www.uis.unesco.org/en/data/sdg4-country-profiles? 

# In[8]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')

