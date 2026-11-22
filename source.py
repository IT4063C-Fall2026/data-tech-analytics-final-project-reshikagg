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
# *What specific question are you seeking to answer with this project? This is not the same as the questions you ask to limit the scope of the project. 📝* <!-- Answer Below -->
# 
# Is higher educational achievement associated with employment status among adults in rural Nepal?
# Which quality of life factor has the strongest relationship with educational achievement?
# Is educational achievement associated with access to basic household services?
# How does household wealth vary across different levels of educational achievement?

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

# In[1]:


import pandas as pd
import urllib.request
import json


# SOURCE 1: Local Microdata File (.DTA)

dhs = pd.read_stata(
    r"C:\Users\reshi\OneDrive\Desktop\Fall 2026\Data Tech Analytics\NPPR82FL.DTA"
)


# SOURCE 2: API Import (World Bank API via urllib)

wb_url = ("https://api.worldbank.org/v2/country/NPL/indicator"
            "/NY.GDP.PCAP.CD?date=2015:2022&format=json")
with urllib.request.urlopen(wb_url,timeout=30) as repsonse:
    wb_data = json.loads(repsonse.read().decode('utf-8'))[1]

worldbank_df = pd.DataFrame(wb_data)[['date', 'value']].rename(
    columns={'value': 'gdp_per_capita'})


# SOURCE 3: Web-Scraped / JSON Endpoint Data (UNESCO/SDG Indicator Data via urllib)

# Pulling SDG 4 / Education indicator JSON directly from web source
unesco_api_url = ("http://api.worldbank.org/v2/country/NPL/indicator"
                    "/SE.PRM.CMPT.ZS?date=2015:2022&format=json")
with urllib.request.urlopen(unesco_api_url, timeout=30) as repsonse:
    unesco_reponse =json.loads(repsonse.read().decode("utf-8"))
unesco_data =unesco_reponse[1]

unesco_df = pd.DataFrame(unesco_data)[['date', 'value']].rename(
    columns={
        "date": "year",
        'value': "primary_completion_rate"})

unesco_df["year"] = pd.to_numeric(
    unesco_df["year"], errors="coerce"
)

unesco_df["primary_completion_rate"]= pd.to_numeric(
    unesco_df["primary_completion_rate"],errors="coerce"
)
unesco_data=unesco_df.sort_values("year").reset_index(drop=True)

# Check all 3 distinct source operations

print("1. DHS File Shape:", dhs.shape)
print("2. World Bank API Shape:", worldbank_df.shape)
print("3. UNESCO / SDG Web Data Shape:", unesco_df.shape)


# In[2]:


## Data Inspection

#DHS dataset
print("DHS first five rows:")
display(dhs.head())

print("\nDHS dimensions:")
print(dhs.shape)

print("\nDHS data types:")
print(dhs.dtypes.value_counts())

#World Bank GDP dataset
print("\nWorld Bank GDP Data:")
display(worldbank_df)


#World bank main completion dataset
print("\nUNESCO sourced Priamry Completion Dataset:")
display(unesco_df)


# In[3]:


#MissinG Values in DHS dataset
missing_count=dhs.isna().sum().sum()
total_cells = dhs.shape[0]* dhs.shape[1]
missing_percentage=(missing_count /total_cells)* 100

print("Total missinf DHS cells:",missing_count)
print("Total DHS cells:",total_cells)
print(f"Overall missingness:{missing_percentage:2f}%")

#No data columns
empty_columns = dhs.columns[dhs.isna().all()].tolist()
print("Empty Columnss:",len(empty_columns))

#Duplicate Rows
print("Duplicate Rowsa:",dhs.duplicated().sum())

#Check imporant columns
important_columns=[
    "hv025","hv106","hv107","hv270",
    "hv271","hv201","hv206"
]
for column in important_columns:
    if column in dhs.columns:
        print(f"\n{column}value counts:")
        display(dhs[column].value_counts(dropna=False).head(15))


# ## Exploratory Data Analysis (EDA)
# 
# The purpose of EDA is to understand the Nepal Demographic and Health Survey (DHDS) dataset and identify any patterns between educational achievement and quality-of-life indicators in rural Nepal. I will inspect the distribution of education, household wealth, electricity access, and drinking water sources. I will look into the missing values, duplicate records, abnormalities, and data types that need attention,
# 
# The DHS is my primary source of demographic and household information. The World Bank indicator will support the context about Nepal's economic and education conditions. Because these data represent different levels of information, the indicator will be analyzed separately from individual DHS records.

# In[4]:


## Rural Dataset

import matplotlib.pyplot as plt
import seaborn as sns

# Create temporary dataset for EDA
eda_df=dhs.copy()

#Remove columns with no data
eda_df =eda_df.dropna(axis=1,how="all")


# Check residence labels 
print("Residence type value:")
display(eda_df["hv025"].value_counts(dropna=False))

print("\nEducation level values:")
display(eda_df["hv106"].value_counts(dropna=False))

#Keeping rural records
rural_eda = eda_df[
    eda_df["hv025"].astype(str).str.strip().str.lower() == "rural"
].copy()

print("\nRural dataset shape:",rural_eda.shape)


# Rename columns
rename_columns={
    "hv025": "residence_type",
    "hv106": "education_level",
    "hv107": "education_grade",
    "hv270": "wealth_index_category",
    "hv271": "wealth_index_score",
    "hv201": "drinking_water_source",
    "hv206": "electricity_access"
}
rural_eda =rural_eda.rename(columns={
    old: new for old, new in rename_columns.items()
    if old in rural_eda.columns
})

# Scale wealth index score
rural_eda["wealth_index_score_scaled"]=(
    rural_eda["wealth_index_score"] /100000
)
print("Rural dataset shape:", rural_eda.shape)
display(rural_eda.head())


# ## 1. Exploratory Data Analysis (EDA)
# 
# 1. Insights and Distribution
# 
# In the rural dataset, the largest category was basic education with 12,138 records. I explored whether there was any relation between education and household wealth, electricity access, and drinking water using visualization. 
# 
# 2. Correlations 
# 
# The chart showed the relationship between education achievement and living conditions.
# 
# 3. Outliers or Data issues
# 
# I had to remove 76 empty columns. The weight score has both negative and positive values. I have not identified any outliers.
# 
# 4. Missing Values
# 
# Education level has 2,270 missing records in the rural dataset, and education grade has 9,628 missing records. I excluded missing and unknown education.
# 
# 5. Duplicates 
# 
# There were no exact duplicate rows. It is expected to have multiple house IDs because a household can contain multiple records.
# 
# 6. Data types
# 
# I have renamed the important variables for clarity and scaled the wealth score by dividing it by 100,00. 

# In[5]:


# Visualization 1: Education-Level Distribution in Rural Nepal

education_data=rural_eda[
    rural_eda["education_level"].notna()
].copy()
plt.Figure(figsize=(10,6))

sns.countplot(
    data=education_data,
    y="education_level",
    order=education_data["education_level"].value_counts().index,
    color="steelblue"
)

plt.title("Distribution of Education Levels in Rural Nepal")
plt.xlabel("Number of Records")
plt.ylabel("education_level")

plt.tight_layout
plt.show


# Visualization 1: Education-Level Distribution in Rural Nepal
# 
# 
# This bar chart shows the distribution of education level within rural Nepal. The chart helps show which education level is the most common and which is less represented. Records that do not have missing education level values are excluded. This is the starting point to examine whether there is a correlation with education achievement and household health and access to basic services.

# In[6]:


# Visualization 2: Household Wealth by Education Level

wealth_plot_df=rural_eda[
    rural_eda["education_level"].notna()
    & rural_eda["wealth_index_score_scaled"].notna()
].copy()

plt.Figure(figsize=(11,6))
sns.boxplot(
    data=wealth_plot_df,
    x="education_level",
    y="wealth_index_score_scaled",
    color="lightblue"
)

plt.title("Household Wealth by Education Level in Rural Neapl")
plt.xlabel("Education Level")
plt.ylabel("Scaled DHS Wealth Index Score")
plt.xticks(rotation=25, ha="right")
plt.tight_layout
plt.show


# Visualization 2: Household Wealth by Education Level
# 
# This boxplot compares the wealth index based on education achievement in rural Nepal. This shows the difference in each category in the median wealth score. The boxplots show that the higher the education, the higher the wealth index.

# In[7]:


# Visualization 3: Electricity Access by Education Level

electricity_df =rural_eda[
    rural_eda["education_level"].notna()
    & rural_eda["electricity_access"].notna()
].copy()

electricity_pct =pd.crosstab(
    electricity_df["education_level"],
    electricity_df["electricity_access"],
    normalize="index"
)*100

ax=electricity_pct.plot(
    kind="bar",
    stacked=True,
    figsize=(10,6),
    colormap="Set2"
)

ax.set_title("Electricity Access by Education Level in Rural Nepal")
ax.set_xlabel("Education Level")
ax.set_ylabel("Percentage of Records")
ax.legend(
    title="Electricity Access",
    bbox_to_anchor=(1.02,1),
    loc="upper left"
)

plt.xticks(rotation=25,ha="right")
plt.tight_layout()
plt.show()


# Visualization 3: Electricity Access by Education Level
# 
# The stacked bar chart compares electricity access across all education level categories in rural Nepal. The percentages show the proportion with and without electricity in each group. The visualization shows that the higher the education, the greater the electricity access they received.

# In[8]:


# Visualization 4: Drinking Water Sources by Education Level
water_df=rural_eda[
    rural_eda["education_level"].notna()
    &rural_eda["drinking_water_source"].notna()
]

water_pct = pd.crosstab(
    water_df["education_level"],
    water_df["drinking_water_source"],
    normalize="index"
)*100

plt.figure(figsize=(13, 6))

sns.heatmap(
    water_pct,
    cmap="YlGnBu",
    annot=True,
    fmt=".1f"
)

plt.title("Drinking Water Sources by Education Level in Rural Nepal")
plt.xlabel("Drinking Water Source")
plt.ylabel("Highest Education Level Attended")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ## 2. Data Cleaning 
# In this section, I have prepared the Nepal DHS 2022 data for analysis. I noticed that there were missing values, duplicate records, unusual values, and data type issues. I removed columns that had no data, checked for duplicate records, cleaned up variable names, and prepared a subset of rural records for the reach questions. Rather than automatically replacing or deleting scores, I maintained the missing values and usual records. These cleaning decisions improved the consistency of the data while maintaining the information.

# In[9]:


# 2.1 Create a copy and removed empty columns

dhs_clean=dhs.copy()

print("Original dataset shape:",dhs_clean.shape)

dhs_clean=dhs_clean.dropna(axis=1,how="all")
print("Shape after removing empty columns:",dhs_clean.shape)

duplicate_count=dhs_clean.duplicated().sum()
print("Duplicate rows:",duplicate_count)

important_columns=[
    "hv025","hv106","hv107","hv270",
    "hv271","hv201","hv206"
]
print("\nMissing values in importnat columns")
for column in important_columns:
    if column in dhs_clean.columns:
            missing_count=dhs_clean[column].isna().sum()
            print(f"{column}:{missing_count:,} missing values"
        ) 
    else:
       print(f"{column}:Column not found")   


# In[10]:


# 2.2 Rename Variables and Scale Wealth Index
rename_columns = {
    "hv025":"residence_type",
    "hv106":"education_level",
    "hv107":"education_grade",
    "hv270": "wealth_index_category",
    "hv271": "wealth_index_score",
    "hv201": "drinking_water_source",
    "hv206": "electricity_access"
}

dhs_clean=dhs_clean.rename(
    columns=rename_columns
)

dhs_clean["wealth_index_score"]=pd.to_numeric(
    dhs_clean["wealth_index_score"], errors="coerce")
dhs_clean["wealth_index_score_scaled"]=(
    dhs_clean["wealth_index_score"] / 100000
)
print("Updated dataset shape:",dhs_clean.shape)

display(
    dhs_clean[
        [
        "residence_type",
        "education_level",
        "education_grade",
        "wealth_index_category",
        "wealth_index_score",
        "wealth_index_score_scaled",
        "drinking_water_source",
        "electricity_access"
        ]
    ].head()
)


# In[11]:


# 2.3 prepare rural dataset

rural_clean =dhs_clean[
    dhs_clean["residence_type"]=="rural"
].copy()

print("Rural dataset shape:",rural_clean.shape)
print("\nResidence type counts:")
display(rural_clean["residence_type"].value_counts())

rural_columns=[
    "education_level",
    "education_grade",
    "wealth_index_category",
    "wealth_index_score_scaled",
    "drinking_water_source",
    "electricity_access"
]
print("\nMissing Values in rural dataset:")
display(rural_clean[rural_columns].isna().sum())


# In[12]:


## 2.4 Investigate Missing Edcuation Values

print("Education level counts:")
display(rural_clean["education_level"].value_counts(dropna=False))

print("\neducation grade summary:")
display(rural_clean["education_grade"].describe())

print("\n)Education grdae missing count:")
print(rural_clean["education_grade"].isna().sum())

print("\nMissingness Comparsion:")

display(
    pd.crosstab(
        rural_clean["education_level"].isna(),
        rural_clean["education_grade"].isna(),
        margins=True
    )
)


# In[13]:


# 2.5 Preapre date fro education level analysis

rural_eda=rural_clean[
    rural_clean["education_level"].notna()
].copy()

print("Originla rural dataset:",rural_clean.shape)
print("Education-level analysis dataset:", rural_eda.shape)

print("\nMissing Education level:")
print(rural_eda["education_level"].isna().sum())

print("\nEducation level categories:")
display(rural_eda["education_level"].value_counts())


# In[14]:


#2.6 finally edcaution analysis dataset
rural_analysis=rural_clean[
    rural_clean["education_level"].notna()
    &(rural_clean["education_level"]!="don't know")
].copy()

print("Final Education analysis dataset:",rural_analysis.shape)

print("\nEducation level categories:")
display(rural_analysis["education_level"].value_counts())

print("\nMissing education levels:")
print(rural_analysis["education_level"].isna().sum())


# In[15]:


# 2.7 finally data check

print("Final analysis dataset shape:",rural_analysis.shape)

print("\nDuplicate rows:",rural_analysis.duplicated().sum())

analysis_column=[
    "education_level",
    "wealth_index_category",
    "wealth_index_score_scaled",
    "drinking_water_source",
    "electricity_access"
]

print("\nMissing values in analysis variables:")
display(rural_analysis[analysis_column].isna().sum())

print("\nScaled wealth index summary")
display(rural_analysis["wealth_index_score_scaled"].describe())

print("\nEdcuation level counts:")
display(rural_analysis["education_level"].value_counts())


# ## 3. Machine Learning Plan
# 
# 3.1 What type of machine learning model are you planning to use?
# 
# I plan to use the decision tree classifier to dive more into the relationship between household living conditions and education level in rural Nepal. The model can help predict expected education level based on the household wealth score, drinking water, and electricity access.
# 
# 3.2 What are the challenges have you identified/are you anticipating in building your machine learning model?
# 
# One main challenge is the missing data. Another would be that some education categories have more records than others. The dataset also contains multiple records with the same household.
# 
# 3.3 How are you planning to address these challenges?
# 
# I plan to record unknown education levels and exclude the "don't know" from the model. I will change categorical variables to numerical values before training the model. I also plan to compare the model's accuracy with a baseline model using precision and recall to evaluate the predictions. If possible, I want to report the household identifier when splitting the data. Rather than seeing it as cause and effect, I will see the results as associations.
# 
# 1. Ask
#  The goal of this project is to see whether educational attainment is associated with the quality of life in rural communities in Nepal. I want to get a better understanding of whether people with higher educational attainment tend to have better housing conditions, like better health or access to basic services.
# 
# 2. Prepare
# I will use the Nepal Demographic and Health Survey (2022) as my main dataset. I will focus on rural areas and use education level as the target variable. Predictor variables will consist of health score, drinking water source, and electricity access. Any records with missing or unknown education level will be excluded. I will continue to use the dataset split into training and testing sets while keeping individuals from the same household together.
# 
# 3. Process
# I will use scikit-learn pipelines to prepare the dataset for machine learning. Missing numerical values will be replaced using the median, and missing categorical values will be handled using the most frequent value.
# 
# 4. Analyze
# I will use multiple classification models like Decision Tree Classifier, Random Forest Classifier, Logistic Regression, and baseline models. My main model will be the Decision Tree. I will also review which household characteristics contribute the most to predicting educational achievement.
# 
# 5. Evaluate
# I will evaluate the model using F1 score, recall, precision, and accuracy. I will correlate this performance with the testing dataset and use confusion matrices to see how accurately each model will classify the different education levels.
# 
# 6. Share
# The summary will consist of results and discuss whether household wealth and access to basic services are related to education achievement in rural Nepal. I will explain the dataset limitations and interpret the findings as associations rather than cause and effect.

# 3.1  Prepare Machine Learning Dataset
# 
# In this section, the cleaned rural Nepal DHS dataset is being prepared for machine learning classification. The main goal is to see if living conditions can help explain differences in educational achievement. The prepared dataset is going to be used to train and evaluate multiple classification models. 
# 

# In[16]:


# 3.1 Import Machine Learning Libraries
import numpy as np

from sklearn.model_selection import GroupShuffleSplit
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    ConfusionMatrixDisplay,
    confusion_matrix,
    classification_report
)   

print("Machine Learning Libraries Imported Successfully")


# 3.2 Selecting Targets and Features
# 
# Education level is a key variable as it examines the relationship with household condition. The features selected for the classification models include: wealth index score, drinking water source, and electricity access. These variables represent the different aspects of the living condition. 
# 

# In[17]:


#3.2 Prepare Features and Target Variables

ml_df=rural_analysis.copy()

feature_columns=[
    "wealth_index_score_scaled",
    "drinking_water_source",
    "electricity_access"
]

#create feature and target variables

X=ml_df[feature_columns].copy()
y=ml_df["education_level"].copy()

#convert wealth index score to numeric
X["wealth_index_score_scaled"]=pd.to_numeric(
    X["wealth_index_score_scaled"], errors="coerce"
)

#Create household groups by cluster household number
groups=(
    ml_df["hv001"].astype(str)
    +"_"
    +ml_df["hv002"].astype(str)
)
print("Dataset Shape:",ml_df.shape)
print("Feature Shape:",X.shape)
print("Target Shape:",y.shape)

print("\nEducation Categories:")
display(y.value_counts())

print("\nMissing Values in Features:")
display(X.isna().sum())


# 3.3 Testing Data and Split Training
# 
# The dataset is split into two sets: training and testing. These sets are split 80/20. The GroupShuffleSplit is used to make sure members in the same households are not appearing in both sets. This makes sure the models are evaluated on data they are not trained on.

# In[18]:


#3.3 Split Data into Training and Testing Sets
group_split=GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42
)

train_idx, test_idx = next(group_split.split(X, y, groups=groups))
x_train, x_test = X.iloc[train_idx].copy(), X.iloc[test_idx].copy()
y_train, y_test = y.iloc[train_idx].copy(), y.iloc[test_idx].copy()

group_train, group_test = (
    groups.iloc[train_idx].copy(),
    groups.iloc[test_idx].copy()
)

print("Training Set Shape:", x_train.shape, y_train.shape)
print("Testing Set Shape:", x_test.shape, y_test.shape)

print("\nHouseholds appearing in both sets:",
      len(set(group_train).intersection(set(group_test))))



# 3.4 Check Class Distribution
# 
# For the training and testing datasets, the educational category distribution was checked. The result indicates that basic education has the largest category, while higher education has the lowest representation. The imbalance in the class is important when evaluating the model because some categories can be harder to predict than others.

# In[19]:


# 3.4 Check Education Category 
print("Training Set Education Distribution:")
display(y_train.value_counts())

print("\nTesting Set Education Distribution:")
display(y_test.value_counts())

print("\nTraining Education Percentage Distribution:")
display((y_train.value_counts(normalize=True) * 100).round(2))

print("\nTesting Education Percentage Distribution:")
display((y_test.value_counts(normalize=True) * 100).round(2))


# 3.5 Build Preporcessing Pipeline
# 
# Using Scikit-leran to reoare numerical dn catgroeis feurea, i was able to create prepocressin gpioline. For the msiing nuemricla vlues, it was replcaed using medican impiratopn followed by StandardScaler. With msiing catgroical clayes, ti was handled by suing the freuwetes vlaue an donHOtEndcoder. To amke sure the asme preocporssing setps was applied fo the modela dn tersing apip;ine was used.

# In[20]:


#3.5 Create Preprocessing Pipelines for Numerical and Categorical Features

#Numerical Features
numerical_features = x_train.select_dtypes(include=['int64', 'float64']).columns.tolist()

#Categorical Features
categorical_features = x_train.select_dtypes(include=['object', 'category']).columns.tolist()

#Process numerical data
numerical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),   
    ('scaler', StandardScaler())
])

#Process categorical data
categorical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

#combine both preprocessing pipelines
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_pipeline, numerical_features),
        ('cat', categorical_pipeline, categorical_features)
    ]
)

print("Preprocessing Pipelines Created Successfully")
print("\nNumerical Features:", numerical_features)
print("\nCategorical Features:", categorical_features)


# 3.6 Define Classification Models
# 
# The four classification models used for the approximation are: Baseline, Logistic Regression, Random Forest, and Decision Tree. Each model uses a different approach to categorize education achievement based on household living conditions. Having multiple models lets us compare performance and see which approach works best with the datasets.

# In[21]:


#3.6 Create Classifcation Models

models = {
    "Baseline": DummyClassifier(strategy='most_frequent', random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42),
    "DecisionTreeClassifier": DecisionTreeClassifier(class_weight='balanced', random_state=42),
}

print("Classification Models Created Successfully")


# 3.7 Train Classification Models
# 
# Each classification model has a combination with the preprocessing pipeline and is trained using the training dataset. The models have learned the patterns between the living condition and the education categories. After training, the models will be stored so they can be used to create predictions on the testing datasets. 

# In[22]:


#3.7 Train Classfifcation Models

trained_models = {}
for model_name, model in models.items():
    # Create a pipeline with preprocessing and the model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

    # Train the model
    pipeline.fit(x_train, y_train)

    # Store the trained model
    trained_models[model_name] = pipeline

    print(f"{model_name} trained successfully.")


# 3.8 Evaluate Classification Model
# 
# The trained models were evaluated using the testing dataset to measure how well the predictions for education categories are. For each model, accuracy, weighted precision, weighted recall, and macro F1-score were calculated. These metrics give a different view of the model performance, plus the macro F1-score helps address the imbalance between the education categories.

# In[23]:


#3.8 Evaluate Classification Models

results = {}
for model_name, pipeline in trained_models.items():
    # Make predictions on the test set
    y_pred = pipeline.predict(x_test)

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    macro_f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)

    # Store the results
    results[model_name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': macro_f1
    }

    print(f"{model_name} evaluated successfully.")


# In[24]:


results_df = pd.DataFrame(results).T
display(results_df.round(3))


# 3.9 Classification Reports
# 
# The classification report was created to inspect the precision, recall, and F1 score for each education category. With this it can shoe amore detailed view of the model performance than overall accuracy. The report can also show which educational categories were harder for the model to estimate.

# In[25]:


#3.9 Classfication Reports
for model_name, pipeline in trained_models.items():
    y_pred = pipeline.predict(x_test)
    print(f"\nClassification Report for {model_name}:")
    print(classification_report(y_test, y_pred, zero_division=0))


# 3.10 Confusion Matrices
# 
# The confusion matrix was created to provide a visual overview of the actual and predicted education category for each classification model. The diagonal values show correct predictions, while the values off the diagonal show incorrect classifications. This visualization makes it easier to identify which equation categories the models were most confused about.

# In[26]:


#3.10 Confusion Matrices
for model_name, pipeline in trained_models.items():
    y_pred = pipeline.predict(x_test)
    cm = confusion_matrix(y_test, y_pred, labels=pipeline.classes_)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=pipeline.classes_, yticklabels=pipeline.classes_)
    plt.title(f'Confusion Matrix for {model_name}')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()


# 3.11 Select the best model
# 
# To select the strongest trained model, the classification model was compared by the macro F1-score. Random Forest was selected because it has the highest macro F1-score. The metric was used to select the model because it gave each education category equal importance.

# In[30]:


#3.11 Select Best Model 

model_comparison = results_df.drop(index='Baseline')
best_model_name = model_comparison['f1_score'].idxmax()

best_model = trained_models[best_model_name]

print(f"Best Model Selected: {best_model_name}")
print(f"Best Model F1 Score: {results_df.loc[best_model_name, 'f1_score']:.3f}")


# 3.12 Final Model Evaluation Summary
# 
# There were four classified models that were evaluated with accuracy, precision, recall, and macro F1-score. The models included are Baseline, Logistic Regression, Random Forest, and Decision Tree.
# 
# Ultimately, Random Forest was chosen as the best-performing trained model because it has the highest macro F1-score of 0.264 and an accuracy of 0.344. The classification reports and confusion matrices help give additional insight into each model's predictions.
# 
# These results suggest that living conditions like household wealth, drinking water source, and electricity access have limited predictive power for education achievement.

# # 4. Prior Feedback and Updates
# 
# 1. What feedback did you receive from your peers and/or the teaching team?
# 
# Based on the feedback I have received, I now think more carefully about organizing my dataset and handling missing values. It also made me realize how important it is to connect my EDA to my machine learning plan.
# 
# 2. What changes have you made to your project based on this feedback?
# 
# I have removed empty columns, checked for duplicates, renamed variables, and created a separate dataset for rural households. I checked for missing values and created visualizations to better understand the correlations.

# ## Approach and Analysis
# *What is your approach to answering your project question?*
# *How will you use the identified data to answer your project question?*
# 📝 <!-- Start Discussing the project here; you can add as many code cells as you need -->
# I will begin by cleaning and organizing the DHS 2022 data and filtering to focus more on rural households in Nepal. I plan to group participants by their education and compare household wealth, employment status, and access to basic services. I plan to use charts, correlations, and statistics to identify any trends, patterns, or relationships. The DHS will be my main dataset; the World Bank and UNESCO will be used to support the information.

# In[ ]:


# Start your code here


# ## Resources and References
# *What resources and references have you used for this project?*
# 📝 <!-- Answer Below -->
# 1. DHS Program :https://dhsprogram.com/data/dataset_admin/index.cfm 
# 2. World Bank: https://data.worldbank.org/country/nepal 
# 3. UNESCO UIS: https://www.uis.unesco.org/en/data/sdg4-country-profiles? 

# In[ ]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')

