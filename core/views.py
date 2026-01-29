import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import boto3
import time
import environ
import os
# AWS Settings
env = environ.Env()
# .env file ko read karein
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Ab keys ko variable se uthayein
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
BUCKET_NAME = "motherscare"
REGION = "ap-south-1"

def home(request): return render(request, 'home.html')
def about(request): return render(request, 'about.html')
def contact(request): return render(request, 'contact.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def upload_view(request):
    if request.method == 'POST':
        f = request.FILES.get('file')
        if not f: return JsonResponse({'success': False, 'error': 'No file'})
        
        folder = f.content_type.split('/')[0] + "s"
        key = f"uploads/{int(time.time())}-{f.name}"
        try:
            s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, 
                              aws_secret_access_key=SECRET_KEY, region_name=REGION)
            s3.upload_fileobj(f, BUCKET_NAME, key, ExtraArgs={'ContentType': f.content_type})
            return JsonResponse({'success': True, 'key': key})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'upload.html')
# core/views.py mein ye check karein
@login_required
def check_result(request):
    file_key = request.GET.get('key')
    result_key = file_key.replace('uploads/', 'results/') + "_output.json"
    
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name=REGION)
    
    try:
        response = s3.get_object(Bucket="motherscare", Key=result_key)
        data = json.loads(response['Body'].read().decode('utf-8'))
        return JsonResponse({'status': 'SUCCEEDED', 'output': data})
    except s3.exceptions.NoSuchKey:
        return JsonResponse({'status': 'RUNNING'})
    except Exception as e:
        return JsonResponse({'status': 'FAILED', 'error': str(e)})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
    else: form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})