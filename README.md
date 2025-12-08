OrangeHRM Automation Testing Framework

Automated test framework for OrangeHRM using Python, Selenium, Pytest, and Page Object Model (POM).
This project contains reusable page objects, test cases, configuration files, logs, and HTML test reports.

📌 Project Overview

**This automation framework is designed to:**

Validate OrangeHRM application features
Generate HTML reports automatically
Maintain clean Page Object Model design
Reuse methods through utilities and helper classes
Support data-driven testing
**This framework is suitable for functional testing, regression testing, and smoke testing.**

**📂 Project Structure**
OrangeHRM/
├── .venv/                       # Virtual environment (ignored in git)
├── assets/                      # Any project assets (optional)
├── configuration/               # Config files, env variables, URLs, credentials
├── logs/                        # Automation logs generated during runs
├── pages/                       # Page Object Model classes (POM)
├── Reports/                     # HTML reports, XML reports, junit reports
├── screenshots/                 # Screenshots captured on test failure
├── testCases/                   # All pytest test scripts
├── utilities/                   # Utility functions (Excel, waits, logging, helpers)
├── AIO_TestCases.xlsx           # Test data Excel file
├── pytest.ini                   # Pytest configuration file
├── requirements.txt             # Python dependencies list
└── Screen Recording 2025-11-07 120303.mp4   # Recorded test run (large file)


**🚀 How to Run the Tests**

1. Install Dependencies
pip install -r requirements.txt

2. Run All Tests
pytest -v -s testCases

4. Run Tests With markers
   pytest -v -s "marker_name" testCases/

5. Run test Cases parallel
   pytest -v -s -n3 testCases/
   
7. Run in difreent browser
  pytest -v -s testCases/  --browser "edge"
  
**🧪 Testing Features Covered**

Your framework supports:

Feature	Description
🔹 Login Test	Validate correct login and error messages
🔹 Employee Management	Add, update, delete employee records
🔹 Data Driven Testing	Read data from Excel
🔹 POM Architecture	Reusable page objects
🔹 Screenshots	Capture on failure
🔹 Assertion Handling	Clear pass/fail messages
🔹 Logging	Console + file logs
🔹 Reports	HTML reports under /Reports

**🧱 Technology Stack**
Language: Python version[3.13.7]
Automation Tool: Selenium WebDriver selenium_version [3.39.0]
Test Runner: Pytest version[9.0.2]
Design Pattern: Page Object Model (POM)
Reporting: Pytest HTML Report
Logging: Python logging module
Data Handling: openpyxl (Excel)
paraller running : pytest-xdist  version [3.8.0]

**🔧 Configuration (Before Running Tests)**

Inside configuration/ add or edit:

config.ini
[commonInfo]
baseURL = https://opensource-demo.orangehrmlive.com/
username = <your-username>
password = <your-password>

Environment Files
Keep sample.env in repo
Ignore .env using .gitignore

**📸 Screenshots**

Failed tests will automatically save screenshots in:

/screenshots/

**📌 How to Add New Test Cases**

Create/Page Class under /pages/Add locators + actions
Create new test script under /testCases/call methods from pages
Use utilities for waits, Excel data, logging
Run tests using pytest

**📝 Folder Naming Rules**
Page classes → inside pages/
Test case files → inside testCases/
Reusable utilities → inside utilities/
Environment/config → inside configuration/

Use ABSOLUTE PATHS in code

**🤝 Contributing**

Pull requests are welcome.
Create a separate branch for new tests or enhancements.

**📄 License**
This project is for learning & testing automation practice.

Best of luck for your next commit
