# Student Information System

This is a Student Information System implemented in Python using the Tkinter library for the GUI, MySQL for database management, and dotenv for handling environment variables.

## Features

- **Login System:** Authenticate administrators to access the system.
- **Signup Functionality:** Register new administrators with username and password validation.
- **Student Record Management:**

  - Add, update, and delete student records.
  - Search for students based on various criteria.
  - Input validation for data integrity.

- **User-friendly Graphical Interface:**
  - Clear and intuitive GUI design.
  - Responsive forms and buttons for a seamless user experience.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python installed
- MySQL database set up with the required schema (`student_information_db`)
- Necessary Python packages installed (e.g., `mysql-connector`, `customtkinter`)

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/student-information-system.git
   ```

2. Navigate to the project directory:

   ```bash
   cd student-information-system
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the MySQL connection details in your code:

   ```python
   host = "localhost"
   user = "root"
   password = ""
   database = "student_information_db"
   ```

5. Run the application:

   ```bash
   python main.py
   ```

## Usage

- Launch the application by running `main.py`.
- Log in with your administrator credentials.
- Add, update, or delete student records using the provided forms.
- Search for students based on various criteria.
- Log out to exit the application.

## Screenshots

![Login Screen](/screenshots/login.png)
_Caption: The login screen for administrators._

![Main Page](/screenshots/mainpage.png)
_Caption: Manage student records - add, update, and delete._

![Signup Form](/screenshots/signup.png)
_Caption: Signup form to register new administrators._

## Contributing

If you'd like to contribute to this project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your fork and submit a pull request.
