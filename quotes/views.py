from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import SavedQuote
from django.shortcuts import render
from django.http import JsonResponse
from urllib.parse import unquote
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import requests

# def index(request):
#     return render(request, 'quotes/index.html', {})

def index(request):
    if 'daily_quote' not in request.session or 'author' not in request.session:
        api_key = 'CkfY/AL6vj6paYbBOns51g==MRyCQx5eVC52s1Rw'
        category = 'inspirational'
        api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'

        headers = {'X-Api-Key': api_key}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                request.session['daily_quote'] = data[0]['quote']
                request.session['author'] = data[0]['author']
            else:
                request.session['daily_quote'] = "No quote available today"
                request.session['author'] = "Unknown"
        else:
            request.session['daily_quote'] = f"Failed to fetch the quote - Error: {response.status_code}"
            request.session['author'] = "Unknown"

    return render(request, 'quotes/index.html', {'daily_quote': request.session['daily_quote'], 'author': request.session['author']})

def fetch_new_quote(request):
    category = "inspirational"
    api_url = f"https://api.api-ninjas.com/v1/quotes?category={category}"

    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    data = response.json()

    return JsonResponse({'quote': data['data'][0]['quote'], 'author': data['data'][0]['author']})

# the signup view less verbose, use the built-in UserCreationForm
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # or wherever you want to redirect after signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# make this login less verbose, use the built-in login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # or wherever you want to redirect after login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# make a logout view that logs the user out and redirects to the home page
def custom_logout(request):
    logout(request)
    return redirect('index')  # or wherever you want to redirect after logout

@login_required
def save_quote(request, quote_text, quote_author):
    # Decode URL-encoded parameters
    quote_text = unquote(quote_text)
    quote_author = unquote(quote_author)

    # Check if the quote already exists for the current user
    existing_quote = SavedQuote.objects.filter(
        user=request.user,
        quote_text=quote_text,
        quote_author=quote_author
    ).first()



    if existing_quote:
        # Redirect back to the original page with a message
        messages.warning(request, 'Quote already saved')
        return redirect('index')  # Replace 'original_page_name' with the actual name or URL pattern of the page
    # Create a new SavedQuote instance and save it
    saved_quote = SavedQuote(user=request.user, quote_text=quote_text, quote_author=quote_author)
    saved_quote.save()

 # Redirect back to the original page with a success message
    messages.success(request, 'Quote saved successfully')
    return redirect('index')

@login_required
def saved_quotes(request):
    author = request.GET.get('author', '')
    saved_quotes = SavedQuote.objects.filter(user=request.user)

    if author:
        # Filter quotes if an author is specified
        saved_quotes = saved_quotes.filter(quote_author__icontains=author)

    # Create a Paginator object
    paginator = Paginator(saved_quotes, 10)  # Show 10 quotes per page

    # Get the page number from the request
    page_number = request.GET.get('page')

    try:
        # Get the Page object for the requested page number
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page.
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'saved-quotes/saved_quotes.html', {'page_obj': page_obj, 'selected_author': author})


@login_required
def delete_saved_quote(request, saved_quote_id):
    saved_quote = get_object_or_404(SavedQuote, id=saved_quote_id, user=request.user)
    saved_quote.delete()
    return redirect('saved_quotes')

@login_required
def delete_selected_quotes(request):
    if request.method == 'POST':
        quote_ids = request.POST.getlist('quote_ids')
        SavedQuote.objects.filter(id__in=quote_ids, user=request.user).delete()

    return redirect('saved_quotes')
