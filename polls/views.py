from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm  # <--- ADD THIS IMPORT

# New Home Page View (for '/')
def home(request):
    """
    Renders the main site homepage.
    """
    # This view uses a template from the root 'templates' folder
    return render(request, "home.html")


def index(request):
    """
    Renders the polls app index page.
    """
    # This view uses a template from the 'templates/polls' folder
    # We are changing this from HttpResponse to render()
    return render(request, "polls/index.html")


# New Form Page View (for '/polls/form/')
def form_page(request):
    """
    Renders a page with a form.
    - Handles GET requests by showing a blank form.
    - Handles POST requests by validating the form and showing
      the sanitized submitted data.
    """
    submitted_name = None
    
    if request.method == "POST":
        # Create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        
        # form.is_valid() runs all validation and sanitization
        if form.is_valid():
            # Process the data in form.cleaned_data
            # This data is sanitized and safe to use.
            submitted_name = form.cleaned_data['name']
            
            # For this example, we'll just re-render the page
            # with a success message. We pass in a new, blank form.
            return render(request, "polls/form_page.html", {
                "form": ContactForm(),
                "submitted_name": submitted_name
            })
    
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactForm()

    return render(request, "polls/form_page.html", {
        "form": form
    })


# New Vulnerable Page View (for '/polls/vulnerable/')
def vulnerable_page(request):
    """
    Renders a page with an intentional security vulnerability.
    """
    # Get a 'name' parameter from the URL (e.g., ?name=User)
    # This input is NOT sanitized by the view.
    raw_name = request.GET.get('name', 'Guest')
    
    # We pass this raw, un-sanitized data directly to the template.
    # The vulnerability will be in the template itself.
    return render(request, "polls/vulnerable_page.html", {
        "name": raw_name
    })
