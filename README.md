# dqa-helper-tool
Python-based DQA Helper Tool for data quality assurance tasks across DCM projects. Automates capitalization corrections, job title standardization, email normalization, link cleanup, and phone number formatting. Includes quick-entry buttons, clear/reset functions, and customizable features for efficient data validation.

DQA Helper Tool 2.0
📌 Overview
The DQA Helper Tool 2.0 is a Python-based application inspired by the Akin Gump DQA Helper. It is designed to streamline Data Quality Assurance (DQA) tasks across DCM projects, automating repetitive data cleaning and formatting tasks while providing quick-entry shortcuts for efficiency.

📂 Repository Structure
Code
├── dqa_helper_tool/
│   ├── main.py                  # Core Python script
│   ├── utils/                   # Helper functions for formatting
│   ├── gui.py                   # Interface logic
│
├── datasets/
│   ├── sample_inputs.csv        # Example input data
│
├── outputs/
│   ├── cleaned_data.csv         # Corrected and validated outputs
│
└── README.md
⚙️ Features
Company Name Correction  
Fixes capitalization errors.

Job Title Standardization  
Corrects capitalization and expands acronyms.

Email Normalization  
Converts email addresses to lowercase.

Link Cleanup  
Ensures proper formatting of URLs.

Phone Number Formatting  
Adjusts numbers to country-specific and client-specific formats.

Quick Entry Buttons  
Predefined buttons for LinkedIn, Website, and Bio entries.

Clear All Function  
Resets all fields for a fresh start.

Check & Copy Functions

Check: Validates and corrects entered data.

Copy: Copies corrected data automatically.

Enter Key Shortcut: Updates and copies entries instantly.

📊 Advantages
Efficiency: Reduces manual data cleaning.

Consistency: Ensures standardized formats across projects.

Flexibility: Upgradeable and customizable for specific project needs.

Ease of Use: Simple interface with automation shortcuts.

🚀 Usage
Clone the repository:

bash
git clone https://github.com/yourusername/dqa-helper-tool.git
Install dependencies:

bash
pip install -r requirements.txt
Run the tool:

bash
python main.py

_______________________________________
Developed by Jewel Jade Bartolome (2024).
