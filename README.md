# 🌟 USB Port Manager
- A simple tool to enhance USB drive security.

The **USB Port Manager** is a Python application designed to control and monitor USB ports on your computer. Whether you want to enable or disable USB ports, track user activity, or enhance security, this tool provides a simple interface to manage USB connectivity.

## Objectives 🚀

1. **USB Port Control**:
   - Enable or disable USB ports to prevent unauthorized data transfers or device connections.
   - Enhance security by restricting access to USB devices.

2. **User Activity Logging**:
   - Keep track of USB port usage by logging user actions (enable/disable) and timestamps.
   - Maintain an audit trail for accountability and troubleshooting.

3. **Two-Factor Authentication (2FA)**:
   - Implement an additional layer of security using time-based one-time passwords (TOTPs).
   - Protect sensitive operations with a secure Base32 secret.

## How It Works 🤖

1. **Login/Sign Up**:
   - Users can create an account or log in with existing credentials.
   - Passwords are securely hashed and stored in the database.

2. **Main Application Window**:
   - Users can enable or disable USB ports with a single click.
   - The activity log displays recent actions and timestamps.

3. **Two-Factor Authentication**:
   - Users receive a one-time password (OTP) via email or phone.
   - OTPs are generated using a Base32 secret and verified during critical operations.

## Prerequisites 🛠️

1. **Python**:
   - Ensure you have Python installed on your system. If not, download and install it from the [official Python website](https://www.python.org/downloads/).

## Getting Started 🚀

1. **Clone this Repository**:
   - Clone this repository to your local machine.
 ```
   git clone https://github.com/Shubham24S/USB-Physical-Security.git
 ```

2. **Install Dependencies**:
   - Install Python and required dependencies (e.g., `pip install bcrypt pyotp`).

3. **How to Run the USB Port Manager Application**:
   - Follow the steps below to set up and run the application.

## How to Run the USB Port Manager Application 🚀

### Steps to Set Up and Run the Application

1. **Generate a Base32 Secret**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing `generate_secret.py`.
   - Run the script: `python generate_secret.py`.
   - Copy the generated Base32 secret (e.g., `JBSWY3DPEHPK3PXP`).

2. **Update `main.py` with the Base32 Secret**:
   - Open `main.py` in a text editor.
   - Locate the `two_factor_auth` function (around line 210).
   - Replace `'your_base32_secret'` with the copied secret.
   - Save the file.

3. **Create an `.env` File**:
   - Create a file named `.env` in the same directory as `main.py`.
   - Add your email and password to the `.env` file:
     ```
     EMAIL=example@gmail.com
     EMAIL_PASSWORD=mypassword123
     ```

4. **Run the Application**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing `main.py`.
   - Run the script: `python main.py`.
   - The application window will appear, allowing you to manage USB ports.

### Additional Notes 📝
- The application will prompt you to log in or sign up.
- If you encounter any issues, ensure that your environment variables (email and password) are correctly set in the `.env` file.

## Contributing Guidelines 🙌

1. Fork this repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit: `git commit -m "Add feature"`.
4. Push to your fork: `git push origin feature-name`.
5. Create a pull request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
