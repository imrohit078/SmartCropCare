from django.shortcuts import render, redirect
from .forms import LeafImageForm, CommentForm, ContactForm
from .models import LeafImage, Blog, Comment, Reaction
from django.conf import settings
import tensorflow as tf
from tf_keras.models import load_model
from tf_keras.preprocessing import image
import numpy as np
import os
import json
from django.http import JsonResponse
import requests
from decouple import config



# Load precautions.json
precaution_path = os.path.join(settings.BASE_DIR, 'D:/6 month/Ai Projects/crop_disease_project/crop_app/model/precautions.json')
with open(precaution_path, encoding='utf-8') as f:
    precautions = json.load(f)

# Normalize keys
precautions = {k.strip().lower(): v for k, v in precautions.items()}

# Load trained MobileNetV2 model
model_path = os.path.join(settings.BASE_DIR, 'D:/6 month/Ai Projects/crop_disease_project/crop_app/model/mobilenet_model.h5')
model = load_model(model_path)

# Load class labels
labels_path = os.path.join(settings.BASE_DIR, 'D:/6 month/Ai Projects/crop_disease_project/crop_app/model/labels.txt')
with open(labels_path, 'r', encoding='utf-8') as f:
    labels = [line.strip() for line in f]

# Format label for readable output
def format_label(label):
    return label.replace('___', ' - ').replace('_', ' ').title()

# Detection view
def detect_disease(request):
    predicted_label = ""
    formatted_label = ""
    disease_info = []
    uploaded_image_url = ""
    confidence = 0.0

    if request.method == 'POST':
        form = LeafImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            image_path = os.path.join(settings.MEDIA_ROOT, instance.image.name)

            try:
                # Image preprocessing
                img = image.load_img(image_path, target_size=(224, 224))
                img_array = image.img_to_array(img) / 255.0
                img_array = np.expand_dims(img_array, axis=0)

                # Predict
                prediction = model.predict(img_array)
                pred_index = np.argmax(prediction)
                predicted_label = labels[pred_index].strip()
                confidence = float(np.max(prediction)) * 100

                # Save to DB
                instance.predicted_disease = predicted_label
                instance.save()

                formatted_label = format_label(predicted_label)
                predicted_label_key = predicted_label.lower().strip()
                disease_info = precautions.get(predicted_label_key, ["⚠️ No precaution info found."])
                uploaded_image_url = instance.image.url

                print(f"✅ Prediction: {formatted_label} ({confidence:.2f}%)")

            except Exception as e:
                print("❌ Prediction Error:", e)
                disease_info = ["⚠️ Error during prediction. Try another image."]

    else:
        form = LeafImageForm()

    return render(request, 'detect.html', {
        'form': form,
        'predicted_label': formatted_label,
        'disease_info': disease_info,
        'uploaded_image_url': uploaded_image_url,
        'confidence': f"{confidence:.2f}%" if confidence else None
    })



def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blogs.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = Comment.objects.filter(blog=blog)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.blog = blog
        comment.save()
        return redirect('blog_detail', blog_id=blog.id)

    return render(request, 'blog_details.html', {'blog': blog, 'comments': comments, 'form': form})


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


SUGGESTIONS_MAP = {
    'Tomato': {
        'rain': '🌧️ Rain expected — Risk of Early Blight. Avoid overhead watering and consider fungicide sprays.',
        'fog': '🌫️ Fog expected — Increased chance of Late Blight. Monitor leaf conditions daily.',
    },
    'Grape': {
        'rain': '🌧️ Rain + Grape = Downy Mildew risk. Ensure good air circulation.',
        'fog': '🌫️ Foggy weather may cause Powdery Mildew. Prune excess foliage.',
    },
    'Apple': {
        'rain': '🌧️ Rain may trigger Apple Scab. Remove infected leaves and consider fungicides.',
    },
}


def get_weather(request):
    city = request.GET.get('city')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    api_key = '64ff1409c2be21788546f21713bb9043' 

    if not city and not (lat and lon):
        city = 'Delhi'

    if lat and lon:
        current_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric'
    else:
        current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'

    try:
        current_data = requests.get(current_url).json()
        forecast_data = requests.get(forecast_url).json()

        if 'main' not in current_data or 'list' not in forecast_data:
            return render(request, 'weather/weather.html', {'error': 'Unable to retrieve weather data.'})

        current_weather = {
            'city': current_data['name'],
            'temp': current_data['main']['temp'],
            'weather': current_data['weather'][0]['description'].title(),
            'humidity': current_data['main']['humidity'],
            'wind': current_data['wind']['speed'],
            'icon': current_data['weather'][0]['icon'],
        }

        forecast = []
        alerts = []
        for entry in forecast_data['list']:
            if "12:00:00" in entry['dt_txt']:
                desc = entry['weather'][0]['description'].lower()
                alert = None
                if 'rain' in desc:
                    alert = '🌧️ Rain predicted — Monitor for fungal diseases.'
                elif 'fog' in desc:
                    alert = '🌫️ Fog expected — Risk of mildew or rust.'

                rain_chance = entry.get('pop', 0) * 100

                forecast.append({
                    'date': entry['dt_txt'].split(" ")[0],
                    'temp': entry['main']['temp'],
                    'description': desc.title(),
                    'icon': entry['weather'][0]['icon'],
                    'alert': alert,
                     'rain_chance': round(rain_chance)
                })

                if alert:
                    alerts.append(alert)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(current_weather)

        return render(request, 'weather.html', {
            'weather': current_weather,
            'forecast': forecast,
            'alerts': alerts
        })

    except Exception as e:
        return render(request, 'weather.html', {'error': 'Error retrieving weather.'})


def faq_page(request):
    return render(request, 'faq.html')


def contact(request):
    form = ContactForm(request.POST or None)
    submitted = False
    if request.method == 'POST' and form.is_valid():
        form.save()
        submitted = True
        form = ContactForm()  

    return render(request, 'contact.html', {'form': form, 'submitted': submitted})