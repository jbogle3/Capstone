# Secure File Analysis & Web Security Portal (Capstone Project)

## Project Overview
This project is a secure web application built with **Django** and **Docker**. It demonstrates advanced software security principles including **Static & Dynamic Analysis**, **Memory Protection (ASLR/DEP) detection**, and secure coding practices.

The application serves as a "Security Sandbox" where users can upload binary files to check for security mitigations, while also providing educational demonstrations of secure vs. vulnerable web forms.

## 🚀 Quick Start (Docker)
The entire application is containerized for secure isolation.

1.  **Build the Container:**
    ```bash
    docker build -t capstone-security-app .
    ```

2.  **Run the Application:**
    ```bash
    docker run -p 8000:8000 capstone-security-app
    ```

3.  **Access the Dashboard:**
    Open your browser to [http://127.0.0.1:8000](http://127.0.0.1:8000).

## 🛠️ Components & Functionality

### 1. Secure File Analysis Engine (Option 1)
* **Location:** `/polls/upload/`
* **Function:** Users can upload Windows Executable (`.exe`) files.
* **Security Logic:** The backend uses `pefile` to parse the binary header and inspect `DllCharacteristics`.
    * **ASLR Detection:** Checks for the `IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE` flag.
    * **DEP Detection:** Checks for the `IMAGE_DLLCHARACTERISTICS_NX_COMPAT` flag.
* **Storage:** Results are logged to a SQLite database and displayed on the Dashboard.

### 2. Live Security Dashboard
* **Location:** `/polls/dashboard/`
* **Function:** Displays a real-time table of all analyzed files.
* **Features:**
    * Visual badges (Green/Red) indicating if ASLR/DEP are enabled.
    * Overall "SAFE" or "THREAT" status based on analysis.

### 3. Secure Input Form
* **Location:** `/polls/form/`
* **Function:** Demonstrates secure handling of user input.
* **Defenses Implemented:**
    * **CSRF Protection:** Uses Django's `{% csrf_token %}` to prevent Cross-Site Request Forgery.
    * **Input Sanitization:** Validates `max_length` and strips malicious characters via Django Forms.
    * **Output Encoding:** Auto-escapes special characters to prevent XSS.

### 4. Intentional Vulnerability (Educational)
* **Location:** `/polls/vulnerable/`
* **Vulnerability:** **Reflected Cross-Site Scripting (XSS)**.
* **Mechanism:** The view accepts a raw `name` parameter from the URL and renders it using the `|safe` filter, bypassing Django's auto-escaping.
* **Proof of Concept:** Appending `<script>alert(1)</script>` to the URL executes JavaScript.

## 🔍 Security Analysis Reports

### Static Analysis (Bandit)
We ran `bandit -r .` against the codebase.
* **Finding:** `settings.py` had `DEBUG = True`.
* **Mitigation:** In a real production deployment, this would be set to `False` to prevent stack trace leakage.
* **Finding:** Hardcoded `SECRET_KEY`.
* **Mitigation:** Used environment variables in the Docker container for the final build.

### Dynamic Analysis (Fuzzing)
We tested the upload endpoint (`/polls/upload/`) using a custom Python fuzzer (`fuzzer.py`).
* **Test:** Attempted upload without CSRF token.
    * **Result:** `403 Forbidden` (PASSED - Protection Active).
* **Test:** Buffer Overflow (Massive filename).
    * **Result:** Handled gracefully by Django (No 500 Crash).
* **Test:** SQL Injection in filename.
    * **Result:** Sanitized by Django ORM (No DB injection possible).

## 📂 Project Structure
* **`mysite/`**: Core Django settings and configuration.
* **`polls/`**: Main application logic.
    * `models.py`: Database schema for `UploadedFile`.
    * `views.py`: Logic for Analysis Engine and Dashboard.
    * `forms.py`: Secure form definitions.
* **`templates/`**: Bootstrap 5 HTML templates (Dark Mode enabled).
* **`Dockerfile`**: Configuration for the secure, isolated environment.
* **`fuzzer.py`**: Script used for dynamic security testing.
