
import pandas as pd
import sqlite3

# STEP 1: Load the survey dataset
df = pd.read_csv("survey_results_public.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

# STEP 2: Select important columns
columns = [
    "Country",
    "YearsCodePro",
    "Employment",
    "RemoteWork",
    "ConvertedCompYearly"
]

analysis_df = df[columns].copy()

print("\nSelected columns:")
print(analysis_df.head())

# STEP 3: Check missing values
print("\nMissing values:")
print(analysis_df.isnull().sum())

# STEP 4: Create SQL database
conn = sqlite3.connect("survey_analysis_new.db")

analysis_df.to_sql(
    "survey",
    conn,
    if_exists="replace",
    index=False
)

print("\nSQL database created successfully!")

# STEP 5: Analyze employment types
query = """
SELECT Employment, COUNT(*) AS total_respondents
FROM survey
WHERE Employment IS NOT NULL
GROUP BY Employment
ORDER BY total_respondents DESC;
"""

result = pd.read_sql_query(query, conn)

print("\nEmployment Distribution:")
print(result)

conn.close()

print("nProject completed successfully!")


# STEP 6: SALARY ANALYSIS

print("\n--- SALARY ANALYSIS ---")

salary_df = analysis_df[
    ["YearsCodePro", "ConvertedCompYearly"]
].copy()

salary_df["ConvertedCompYearly"] = pd.to_numeric(
    salary_df["ConvertedCompYearly"], errors="coerce"
)

salary_df = salary_df.dropna(
    subset=["YearsCodePro", "ConvertedCompYearly"]
)

print("\nAverage Annual Salary:")
print(salary_df["ConvertedCompYearly"].mean())

print("\nMedian Annual Salary:")
print(salary_df["ConvertedCompYearly"].median())

print("\nSalary Statistics:")
print(salary_df["ConvertedCompYearly"].describe())


# STEP 7: COUNTRY-WISE ANALYSIS

print("\n--- COUNTRY-WISE ANALYSIS ---")

conn = sqlite3.connect("survey_analysis_new.db")

query = """
SELECT Country, COUNT(*) AS total_respondents
FROM survey
WHERE Country IS NOT NULL
GROUP BY Country
ORDER BY total_respondents DESC
LIMIT 10;
"""

country_result = pd.read_sql_query(query, conn)

print(country_result)

conn.close()


# STEP 8: REMOTE WORK ANALYSIS

print("\n--- REMOTE WORK ANALYSIS ---")

conn = sqlite3.connect("survey_analysis_new.db")

query = """
SELECT RemoteWork, COUNT(*) AS total_respondents
FROM survey
WHERE RemoteWork IS NOT NULL
GROUP BY RemoteWork
ORDER BY total_respondents DESC;
"""

remote_result = pd.read_sql_query(query, conn)

print(remote_result)

conn.close()


# STEP 9: DATA VISUALIZATION

import matplotlib.pyplot as plt

print("\n--- CREATING SALARY GRAPH ---")

salary_data = pd.to_numeric(
    analysis_df["ConvertedCompYearly"],
    errors="coerce"
).dropna()

salary_data = salary_data[salary_data > 0]

# Remove extreme values for a clearer graph
salary_data = salary_data[salary_data <= salary_data.quantile(0.95)]

plt.figure(figsize=(10, 6))
plt.hist(salary_data, bins=30)
plt.title("Distribution of Annual Compensation")
plt.xlabel("Annual Compensation (reported values)")
plt.ylabel("Number of Respondents")
plt.tight_layout()

plt.savefig("salary_distribution.png")
plt.show()

print("Salary graph saved as salary_distribution.png")


# STEP 10: COUNTRY-WISE VISUALIZATION

import matplotlib.pyplot as plt

print("\n--- CREATING COUNTRY GRAPH ---")

conn = sqlite3.connect("survey_analysis_new.db")

query = """
SELECT Country, COUNT(*) AS total_respondents
FROM survey
WHERE Country IS NOT NULL
GROUP BY Country
ORDER BY total_respondents DESC
LIMIT 10;
"""

country_result = pd.read_sql_query(query, conn)

plt.figure(figsize=(12, 6))
plt.bar(country_result["Country"], country_result["total_respondents"])
plt.title("Top 10 Countries by Survey Respondents")
plt.xlabel("Country")
plt.ylabel("Number of Respondents")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("country_respondents.png")
plt.show()

conn.close()

print("Country graph saved as country_respondents.png")



# STEP 11: SAVE ANALYSIS RESULTS

print("\n--- SAVING PROJECT RESULTS ---")

conn = sqlite3.connect("survey_analysis_new.db")

# Country-wise respondents
country_query = """
SELECT Country, COUNT(*) AS total_respondents
FROM survey
WHERE Country IS NOT NULL
GROUP BY Country
ORDER BY total_respondents DESC
LIMIT 10;
"""

country_result = pd.read_sql_query(country_query, conn)

# Remote work distribution
remote_query = """
SELECT RemoteWork, COUNT(*) AS total_respondents
FROM survey
WHERE RemoteWork IS NOT NULL
GROUP BY RemoteWork
ORDER BY total_respondents DESC;
"""

remote_result = pd.read_sql_query(remote_query, conn)

# Employment distribution
employment_query = """
SELECT Employment, COUNT(*) AS total_respondents
FROM survey
WHERE Employment IS NOT NULL
GROUP BY Employment
ORDER BY total_respondents DESC;
"""

employment_result = pd.read_sql_query(employment_query, conn)

# Save results to CSV files
country_result.to_csv("country_analysis.csv", index=False)
remote_result.to_csv("remote_work_analysis.csv", index=False)
employment_result.to_csv("employment_analysis.csv", index=False)

conn.close()

print("Country analysis saved!")
print("Remote work analysis saved!")
print("Employment analysis saved!")
print("All result files created successfully!")
