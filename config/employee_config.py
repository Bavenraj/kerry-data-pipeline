CONFIG = {
    
    # FILES
    "input_file": "data/Dset.xlsx",
    "output_file": "output/employee_cleaned.csv",

    # DROP COLUMNS
    "drop_columns": [
        "Tenure (Years)"
    ],

    # VALUE MAPPINGS
    "mappings": {
        "Department": {
            # IT
            "IT": "Information Technology",
            "I.T.": "Information Technology",

            # Sales
            "Sales Dept": "Sales",
            "SLS": "Sales",

            # Customer Support
            "Cust. Support": "Customer Support",
            "CS": "Customer Support",

            # Finance
            "Financial Dept": "Finance",
            "Fin.": "Finance",

            # Marketing
            "Market Dept": "Marketing",
            "MKT": "Marketing",

            # HR
            "HR": "Human Resource",
            "H.R.": "Human Resource",
            "Human Resources": "Human Resource",

            # Operations
            "Operational": "Operations",
            "Ops": "Operations"
        }
    },

    # DATA TYPES
    "data_types": {
        "Employee ID": "string",
        "Name": "string",
        "Gender": "string",
        "Department": "string",
        "Job Title": "string",
        "Reason for Leaving": "string",
        "Age": "Int64",
        "Performance Score": "Int64",
        "Job Satisfaction": "Int64",
        "Work-Life Balance": "Int64",
        "Salary": "float64",
        "Date of Hire": "datetime"
    },

    # REMOVE DUPLICATES
    "remove_duplicates": True
}