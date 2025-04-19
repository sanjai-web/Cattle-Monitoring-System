from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Scheme, UserProfile, PhoneAddress
from .forms import UserProfileForm
from decimal import Decimal
from django.http import JsonResponse
 
    

# Home page view to display all products
def home_view(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# View for the cattle page
def cattle_view(request):
    return render(request, 'cattle.html')

def checkout_view(request):
    # Add your checkout logic here
    return render(request, 'checkout.html')





from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem  # Assuming you have a `CartItem` model for items in the cart
from django.contrib.auth.decorators import login_required
# In views.py
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)  # Get cart items for the logged-in user
    context = {
        'cart_items': cart_items,
        'cart_total': sum(item.total_price for item in cart_items),  # Calculate total for the cart
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, product_id):
    # Get the product being added to the cart
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the cart item for this user and product
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        # If the product is already in the cart, increment the quantity
        cart_item.quantity += 1
    
    # Save the updated cart item
    cart_item.save()

    # Redirect to the cart page after adding
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)  # Ensure the cart item belongs to the logged-in user
        cart_item.delete()
    return redirect('cart')

@login_required
def update_cart_quantity(request, item_id, action):
    # Get the cart item by ID for the current user
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    # Update the quantity based on the action (increase or decrease)
    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    
    # Save the cart item after updating
    cart_item.save()

    # Redirect back to the cart page
    return redirect('cart')





from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
from .models import CartItem  # Import the CartItem model
from datetime import datetime
from django.core.mail import EmailMessage

def generate_invoice_pdf(request):
    # Get the user's cart items
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items:
        return HttpResponse("No items in your cart.", content_type="text/plain")

    # Create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()

    # Create a PDF object, using BytesIO as its "file"
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Set the font and add header information
    p.setFont("Helvetica-Bold", 16)
    p.drawString(40, 750, "CARA Pvt ltd")
    p.setFont("Helvetica", 10)
    p.drawString(40, 735, "ksr kalvi nagar, Tiruchengode")
    p.drawString(40, 720, "Namakkal, 637215")

    # Add customer details
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, 670, f"{request.user.first_name} {request.user.last_name}")
    p.setFont("Helvetica", 10)

   
    p.drawString(40, 655, "Bhavani")  
    p.drawString(40, 640, "Erode, 638504")     

    # Add invoice details
    p.setFont("Helvetica-Bold", 12)
    p.drawString(400, 750, "INVOICE")
    p.setFont("Helvetica", 10)
    p.drawString(400, 730, f"Invoice #: 123456")
    p.drawString(400, 715, f"Invoice Date: {datetime.now().strftime('%m/%d/%Y')}")
    p.drawString(400, 700, "Due Date: " + (datetime.now().strftime('%m/%d/%Y')))

    # Table headers for items
    table_data = [['Item', 'Brand Name', 'Unit Price', 'Quantity', 'Amount']]
    for item in cart_items:
        table_data.append([
            item.product.product_name,
            f"{item.product.brand_name}",  # Replace with actual description if available
            f"₹{item.product.product_price}",
            item.quantity,
            f"₹{item.product.product_price * item.quantity}"
        ])

    # Add total row
    cart_total = sum(item.product.product_price * item.quantity for item in cart_items)
    table_data.append(["", "", "", "Subtotal", f"₹{cart_total}"])
    table_data.append(["", "", "", "Total", f"₹{cart_total}"])
    table_data.append(["", "", "", "Amount Paid", "₹0.00"])
    table_data.append(["", "", "", "Balance Due", f"₹{cart_total}"])

    # Create table
    table = Table(table_data, colWidths=[100, 180, 70, 70, 70])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Calculate table position and draw it
    table.wrapOn(p, width, height)
    table.drawOn(p, 40, 500)

    # Add notes at the bottom
    p.setFont("Helvetica", 10)
    p.drawString(40, 480, "NOTES: Provide a concise, professional description of the services, product, and discount listed above.")

    # Close the PDF object cleanly
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()

    # Send the PDF via email
    email = EmailMessage(
        'Invoice from CARA Pvt ltd',  # Email subject
        'Please find attached your invoice.',  # Email body
        'rajasakar080@gmail.com',  # From email
        ['ksvsanjai20@gmail.com']  # To email login email
    )
    email.attach('invoice.pdf', pdf, 'application/pdf')
    email.send()

    # Create a response object and set the content type to 'application/pdf'
    response = HttpResponse(pdf, content_type='application/pdf')

    # Force download by setting the Content-Disposition header
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response







import requests
import base64
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import io
import numpy as np
import tensorflow as tf

# Replace with your actual Google API Key and Custom Search Engine ID
GOOGLE_API_KEY = 'AIzaSyAdATFGTAL68aTtiRHzYG5xVaGL-vKuTiI'
SEARCH_ENGINE_ID = '8397941029c934170'

# Load the pre-trained model globally (e.g., MobileNetV2)
model = tf.keras.applications.MobileNetV2(weights='imagenet', include_top=True)

@csrf_exempt
def detect_disease(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image')

            # Debug: Print image data to check if it's received correctly
            print(f"Received Image Data: {image_data[:100]}")  # Print first 100 chars

            if not image_data:
                return JsonResponse({'error': 'No image detected'}, status=400)

            # Decode the base64 image
            image = decode_base64_image(image_data)

            if image is None:
                return JsonResponse({'error': 'Invalid image'}, status=400)

            # Preprocess the image
            image_array = preprocess_image(image)

            # Extract features (get predictions from the model)
            predictions = extract_features(image_array)

            # Modify the search query based on the detected labels
            search_query = modify_search_query(predictions)

            # Google Custom Search API request
            search_url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"
            response = requests.get(search_url)

            if response.status_code == 200:
                search_results = response.json()
                results = []
                for item in search_results.get('items', []):
                    results.append({
                        'title': item['title'],
                        'link': item['link'],
                        'snippet': item.get('snippet', '')
                    })
                return JsonResponse({'results': results})
            else:
                return JsonResponse({'error': 'Failed to fetch search results'}, status=500)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Function to decode the base64 image
def decode_base64_image(image_data):
    try:
        # Remove the data URL part if present and decode the image
        image_data = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_data))
        return image
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None

# Function to preprocess the image (resize, normalize, etc.)
def preprocess_image(image):
    # Resize the image to 224x224 for model input
    image = image.resize((224, 224))
    
    # Convert image to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert the image to a NumPy array
    image_array = np.array(image)
    
    # Expand dimensions to match model's expected input shape
    image_batch = np.expand_dims(image_array, axis=0)
    
    # Preprocess the image for the model (normalize to [-1, 1])
    processed_image = tf.keras.applications.mobilenet_v2.preprocess_input(image_batch)
    
    return processed_image

# Function to extract features using the pre-trained model (e.g., MobileNetV2)
def extract_features(image_array):
    # Get predictions from the model
    predictions = model.predict(image_array)
    
    # Debug: print raw predictions
    print(f"Predictions: {predictions}")
    
    # Decode predictions into human-readable labels
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)
    
    # Debug: print decoded predictions
    print(f"Decoded Predictions: {decoded_predictions}")
    
    return decoded_predictions

# Function to modify the Google search query based on predictions
def modify_search_query(predictions):
    # Extract the most probable label from the model predictions
    top_prediction = predictions[0][0][1]  # Get the label of the most probable class
    
    # Modify the search query to include the detected label
    search_query = f"{top_prediction} information"
    
    return search_query






def veterinary_view(request):
    return render(request, 'veterinary.html')



# View for the admin login page
def adminlogin_view(request):
    return render(request, 'adminlogin.html')


# View to display available schemes
def scheme_view(request):
    schemes = Scheme.objects.all()
    return render(request, 'scheme.html', {'schemes': schemes})

from .forms import ProductForm, SchemeForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Scheme
from .forms import ProductForm, SchemeForm
from django.contrib import messages

def admin_page(request):
    schemes = Scheme.objects.all()
    products = Product.objects.all()

    # Initialize forms before any POST handling
    product_form = ProductForm()
    scheme_form = SchemeForm()

    if request.method == 'POST':
        if 'submit_product' in request.POST:
            product_form = ProductForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                messages.success(request, 'Product added successfully.')
            else:
                messages.error(request, 'Failed to add product.')
        elif 'submit_scheme' in request.POST:
            scheme_form = SchemeForm(request.POST, request.FILES)
            if scheme_form.is_valid():
                scheme_form.save()
                messages.success(request, 'Scheme added successfully.')
            else:
                messages.error(request, 'Failed to add scheme.')

    return render(request, 'admin.html', {
        'schemes': schemes,
        'products': products,
        'product_form': product_form,
        'scheme_form': scheme_form
    })











# User login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')





# User signup view
def signup_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST.get('phone')  # Optional
        address = request.POST.get('address')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'User with this email already exists.')
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
            user.save()

            # Create UserProfile
            UserProfile.objects.create(user=user, phone=phone, address=address)

            login(request, user)
            return redirect('login')

    return render(request, 'signup.html')






# View to edit user profile
@login_required
def edit_profile(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile, initial={'full_name': user.first_name})

    return render(request, 'edit_profile.html', {'form': form})


# User dashboard view
@login_required
def dashboard_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    print(user_profile)
    context = {
        'user': request.user,
        'user_profile': user_profile,
    }

    return render(request, 'dashboard.html', context)





def get_user_profile(request):
    # Fetch the user profile for a user with ID 4 (change this ID as needed)
    user_profile = get_object_or_404(PhoneAddress, user=request.user)
    user = user_profile.user

    # Prepare the context data
    context = {
        'user': user,
        'profile': user_profile,
    }

    # Render the 'dashboard.html' template with the context
    return render(request, 'dashboard.html', context)





   





from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Scheme
from .forms import ProductForm, SchemeForm  # Import the forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Edit product view
@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('admin_page')
        else:
            messages.error(request, 'Failed to update product. Please check the form for errors.')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'edit_product.html', {'form': form, 'product': product})





# Edit scheme view
@login_required
def edit_scheme(request, scheme_id):
    scheme = get_object_or_404(Scheme, id=scheme_id)
    if request.method == 'POST':
        form = SchemeForm(request.POST, request.FILES, instance=scheme)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scheme updated successfully.')
            return redirect('admin_page')
        else:
            messages.error(request, 'Failed to update scheme. Please check the form for errors.')
    else:
        form = SchemeForm(instance=scheme)
    
    return render(request, 'edit_scheme.html', {'form': form, 'scheme': scheme})





# Delete product view
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_page')
    
    return redirect('admin_page')



def delete_scheme(request, scheme_id):
    scheme = Scheme.objects.get(id=scheme_id)
    scheme.delete()
    return redirect('admin_page')












from django.shortcuts import render
from django.http import JsonResponse
from .firebase_config import db

def get_sensor_data(request):
    try:
        # Reference to the path in your Firebase Realtime Database
        ref = db.reference('sensorData')
        data = ref.get()

        # Return the data as JSON
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def cattle_view(request):
    # Render the HTML template with data (you can adjust this if needed)
    return render(request, 'cattle.html')
