# School and Van Fees Management System

This software is designed to manage school and van fees efficiently. It allows users to upload Excel sheets, extract student information, and manage fees for educational institutions.

## Features

- **Student Fees Management**: Manage and track school and van fees for students.
- **Excel Upload & Extraction**: Upload Excel sheets and automatically extract student information.

## Installation

To use this software, ensure you have Python installed, then follow these steps:

1. Clone this repository.
2. Navigate to the project directory.
3. Install the required dependencies:

   ```bash
   pip install django pandas
   ```

4. Create the necessary migrations for the `usersAuth` app:

   ```bash
   python manage.py makemigrations usersAuth
   ```

5. Apply the migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

## Usage

Once the server is running, you can access the application through your web browser. Follow the on-screen instructions to manage school fees and upload Excel sheets.

## License

This software is proprietary, and usage requires permission from the author. If you wish to use or modify this software, please contact [Instagram](https://www.instagram.com/shalomarputhasingh).

## Contact

For inquiries or permission requests, please contact me on [Instagram](https://www.instagram.com/shalomarputhasingh).

```
