import os
import requests
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.shortcuts import render, redirect
from django.http import JsonResponse
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

def home(request):
    auth_url = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=read,activity:read_all"
    return render(request, 'home.html', {'auth_url': auth_url})

def exchange_token(request):
    code = request.GET.get('code')

    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
        }
    )

    if response.status_code != 200:
        return render(request, 'home.html', {'error': 'Failed to authenticate with Strava'})

    data = response.json()
    access_token = data.get("access_token")

    request.session['access_token'] = access_token

    return redirect("/dashboard")

def dashboard(request):
    
    access_token = request.session.get('access_token')

    if not access_token:
        
        return redirect('home')

    activities_url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(activities_url, headers=headers)

    if response.status_code != 200:
        return render(request, 'dashboard.html', {'error': 'Failed to fetch activities from Strava'})

    activities = response.json()

    if not activities:
        return render(request, 'dashboard.html', {'error': 'No activities found!'})

    distances = [activity['distance'] for activity in activities[:5]]
    times = [activity['moving_time'] for activity in activities[:5]]
    calories = [activity.get('kilojoules', 0) for activity in activities[:5]]

    fig, ax = plt.subplots()
    ax.bar(range(len(distances)), distances, color='blue', alpha=0.7)
    ax.set_title('Distances of Recent Activities')
    ax.set_xlabel('Activity #')
    ax.set_ylabel('Distance (m)')
   
    img = BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    img.seek(0)

    chart_url = base64.b64encode(img.getvalue()).decode()

    return render(request, 'dashboard.html', {
        'chart_url': f"data:image/png;base64,{chart_url}",
        'activities': activities[:5],
    })
