# Django Security Demo App

This is a simple Django web application built to demonstrate basic routing, template usage, and web security principles.

## App Structure

- `mysite/`: The main Django project folder.
  - `settings.py`: Project settings. Edited to add the `polls` app and the root `templates` directory.
  - `urls.py`: Main URL router. Routes `/` to the home page, `/admin` to the admin site, and `/polls/` to the `polls` app.
- `polls/`: A Django app that contains the site's main logic.
  - `urls.py`: App-level URL router. Routes `/polls/`, `/polls/form/`, and `/polls/vulnerable/`.
  - `views.py`: Contains the view functions (logic) for each page.
  - `forms.py`: (New file) Contains the `ContactForm` class for secure form handling.
  - `models.py`: (Unused in this demo) For database models.
- `templates/`: Contains all HTML templates for the project.
  - `home.html`: The main site home page (`/`).
  - `polls/`: Templates specific to the `polls` app.
    - `index.html`: The app's index page (`/polls/`).
    - `form_page.html`: The secure user input form page (`/polls/form/`).
    - `vulnerable_page.html`: The page with the intentional vulnerability (`/polls/vulnerable/`).
- `manage.py`: Django's command-line utility.

## Functionality

This application has 4 distinct routes:

1.  **Home Page (`/`)**
    -   Handled by `polls.views.home`.
    -   Renders `templates/home.html`.
    -   Provides simple navigation to the other pages.

2.  **Polls Index Page (`/polls/`)**
    -   Handled by `polls.views.index`.
    -   Renders `templates/polls/index.html`.
    -   The original page from the Django tutorial.

3.  **Secure Form Page (`/polls/form/`)**
    -   Handled by `polls.views.form_page`.
    -   Renders `templates/polls/form_page.html`.
    -   **Functionality:**
        -   Displays a form defined in `polls/forms.py`.
        -   **Good Security (CSRF):** The form uses the `{% csrf_token %}` tag to protect against Cross-Site Request Forgery.
        -   **Good Security (Input Validation):** On submit, the view uses `form.is_valid()` to validate and sanitize the input (e.g., checking `max_length`, `required`, and stripping whitespace).
        -   **Good Security (Output Escaping):** When the submitted name is shown, Django's template engine auto-escapes it (`{{ submitted_name }}`), preventing XSS attacks from the form input.

4.  **Vulnerable Page (`/polls/vulnerable/`)**
    -   Handled by `polls.views.vulnerable_page`.
    -   Renders `templates/polls/vulnerable_page.html`.
    -   **Functionality:** Takes a URL query parameter `name` and displays it on the page.

---

## 🚨 Intentional Vulnerability

This project contains one intentional, subtle security vulnerability.

* **File:** `templates/polls/vulnerable_page.html`
* **Line:** `Welcome, {{ name|safe }}!`
* **Vulnerability:** **Reflected Cross-Site Scripting (XSS)**

### Explanation

By default, Django's template engine **auto-escapes** all variables. This means if a variable `name` contains `<script>`, Django will render it as the literal text `&lt;script&gt;`, which the browser will not execute. This is a critical security feature that prevents XSS.

The vulnerability is introduced by using the `|safe` filter. This filter explicitly tells Django, "Do not auto-escape this variable. Trust it and render it as raw HTML."

This allows any HTML or JavaScript passed in the URL to be rendered and executed by the browser.

### How to Exploit

1.  Navigate to the vulnerable page: `/polls/vulnerable/`
2.  Append a query parameter to the URL containing a JavaScript payload, like this:

    ```
    /polls/vulnerable/?name=<script>alert('You have been hacked!')</script>
    ```

3.  When the page loads, the browser will execute the script, and an alert box will pop up. This demonstrates that an attacker could run any arbitrary JavaScript on this page.
