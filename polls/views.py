from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm, UploadFileForm
from .models import UploadedFile
import pefile
import os

# New Home Page View (for '/')
def home(request):
    """
    Renders the main site homepage.
    """
    # This view uses a template from the root 'templates' folder
    return render(request, "home.html")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.file_name = request.FILES['file'].name
            
            # --- CAPSTONE COMPONENT 4: ANALYSIS LOGIC HERE ---
            # run_security_scan(instance.file) 
            # instance.has_aslr = check_aslr(instance.file)
            
            instance.save()
            return redirect('index')
    else:
        form = UploadFileForm()
    return render(request, 'polls/upload.html', {'form': form})

def index(request):
    """
    Renders the polls app index page.
    """
    # This view uses a template from the 'templates/polls' folder
    # We are changing this from HttpResponse to render()
    return render(request, "polls/index.html")

def upload_analysis(request):
    """
    Capstone Option 1: Secure File Upload & Analysis
    1. Accepts a file upload.
    2. Performs static analysis using 'pefile'.
    3. Checks for memory protections (DEP and ASLR).
    4. Saves results to the database.
    """
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Save the file instance but don't commit to DB yet
            instance = form.save(commit=False)
            instance.file_name = request.FILES['file'].name
            
            # Save strictly to disk so we can read it for analysis
            instance.save() 
            
            # 2 & 3. Perform Analysis
            # We wrap this in a try/except in case the file isn't a valid EXE
            try:
                file_path = instance.file.path
                pe = pefile.PE(file_path)
                
                # Check for ASLR (DLL Characteristics flag 0x0040)
                if pe.OPTIONAL_HEADER.DllCharacteristics & 0x0040:
                    instance.has_aslr = True
                
                # Check for DEP (DLL Characteristics flag 0x0100)
                if pe.OPTIONAL_HEADER.DllCharacteristics & 0x0100:
                    instance.has_dep = True
                    
                pe.close()
            except Exception as e:
                # If it fails (e.g., user uploaded a text file), assume no protections
                print(f"Analysis failed: {e}")
            
            # 4. Save the analysis results
            instance.save()
            
            return redirect('index') # Redirect to home or a results page
    else:
        form = UploadFileForm()
    
    return render(request, 'polls/upload_page.html', {'form': form})

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
