 FitMeals - Fitness Meal Planner

Overview

A Flask-based web application for tracking meals and nutrition data, storing all information in an Excel (XLSX) file format. This application allows users to:

- Add, view, edit, and delete meals with complete nutrition information
- Search and filter meals by name or category
- Create meal plans and calculate total nutrition values
- Export all data to Excel for easy analysis

 Features

- Excel Data Storage: All meal data is stored in an XLSX file (meals.xlsx)
- CRUD Operations: Full Create, Read, Update, Delete functionality for meals
- Nutrition Tracking: Track calories, protein, carbs, and fat for each meal
- Meal Planning: Combine multiple meals and view total nutrition
- Search & Filter: Find meals by name or category
- Responsive Design: Works on both desktop and mobile devices

 Technologies Used

- Backend: Python, Flask
- Frontend: HTML, CSS, Bootstrap
- Data Storage: Excel (XLSX) using openpyxl
- Dependencies: See requirements.txt

 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fitness-meal-planner.git
   cd fitness-meal-planner
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

 Configuration

1. Set your secret key:
   - In `app.py`, change `app.secret_key = 'your_secret_key_here'` to a secure random string

2. Excel file:
   - The application will automatically create `meals.xlsx` when first run
   - You can edit this file directly with Excel if needed

 Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

 Usage Guide

Adding a Meal
1. Click "Add Meal" in the navigation
2. Fill in the meal details:
   - Name (e.g., "Grilled Chicken")
   - Category (e.g., "Dinner")
   - Ingredients (comma-separated)
   - Nutrition information (calories, protein, carbs, fat)
   - Cooking instructions (optional)
3. Click "Save Meal"

Viewing and Editing Meals
- The homepage shows all meals
- Click on a meal to view details
- Click "Edit" to modify a meal
- Click "Delete" to remove a meal

Meal Planning
1. Go to the Meal Planner page
2. Select multiple meals by checking the boxes
3. View the total nutrition values for the selected meals

 Searching and Filtering
- Use the search box to find meals by name
- Use the category dropdown to filter by meal type

File Structure

```
fitness-meal-planner/
├── app.py               # Main Flask application
├── meals.xlsx           # Excel data file (created automatically)
├── requirements.txt     # Python dependencies
├── static/              # Static files (CSS, JS)
│   └── ...              
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── index.html       # Homepage
    ├── add_meal.html    # Add meal form
    ├── view_meal.html   # View single meal
    ├── edit_meal.html   # Edit meal form
    └── meal_plan.html   # Meal planner page
```

 Troubleshooting

-Excel file not created: Ensure the application has write permissions in the directory
-Data not saving: Check if the Excel file is open in another program
-Installation issues: Make sure you're using Python 3.6+ and pip is up to date

 License

This project is licensed under the MIT License. See the LICENSE file for details.

Future Enhancements

-User authentication
-Multiple meal plans
-Nutrition goals tracking
-Recipe suggestions based on available ingredients
-Mobile app integration
