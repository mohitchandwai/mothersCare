import os

# Files structure define karna
files = {
    "core/templates/base.html": """
<!DOCTYPE html>
<html>
<head>
    <title>Motherscare AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .navbar { margin-bottom: 30px; }
        .footer { margin-top: 50px; padding: 20px; background: #eee; text-align: center; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Motherscare</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/">Home</a>
                <a class="nav-link" href="/about/">About</a>
                <a class="nav-link" href="/contact/">Contact</a>
                {% if user.is_authenticated %}
                    <a class="nav-link btn btn-primary text-white ms-2" href="/upload/">Upload Hub</a>
                    <form action="{% url 'logout' %}" method="post" style="display:inline;">
                        {% csrf_token %}<button type="submit" class="nav-link btn btn-link">Logout</button>
                    </form>
                {% else %}
                    <a class="nav-link" href="/login/">Login</a>
                {% endif %}
            </div>
        </div>
    </nav>
    <div class="container">{% block content %}{% endblock %}</div>
    <div class="footer">© 2024 Motherscare AI - All Rights Reserved</div>
</body>
</html>""",

    "core/templates/home.html": """
{% extends 'base.html' %}
{% block content %}
<div class="text-center py-5">
    <h1>Smart Maternal Care with AI</h1>
    <p class="lead">Upload images, videos, or audio to get instant health analysis.</p>
    <a href="/upload/" class="btn btn-lg btn-success">Start Analyzing Now</a>
</div>
{% endblock %}""",

    "core/templates/about.html": """
{% extends 'base.html' %}
{% block content %}
<div class="card p-4">
    <h2>About Our Mission</h2>
    <p>Motherscare AI is dedicated to providing high-quality health monitoring tools using AWS cloud and advanced machine learning models.</p>
</div>
{% endblock %}""",

    "core/templates/contact.html": """
{% extends 'base.html' %}
{% block content %}
<div class="card p-4">
    <h2>Contact Us</h2>
    <p>Email: support@motherscare.ai</p>
    <p>Address: Tech Hub, Mumbai, India</p>
</div>
{% endblock %}""",

    "core/templates/login.html": """
{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-4 card p-4 shadow">
        <h3 class="text-center">Login</h3>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit" class="btn btn-primary w-100">Sign In</button>
        </form>
    </div>
</div>
{% endblock %}""",

    "core/templates/upload.html": """
{% extends 'base.html' %}
{% block content %}
<div class="card p-4 shadow text-center">
    <h3>Multimedia Upload Hub</h3>
    <p>Choose the specific media type to upload to S3</p>
    <div class="row mt-4">
        <div class="col-md-4"><button class="btn btn-outline-primary w-100 py-3" onclick="selectFile('image')">🖼️ Image</button></div>
        <div class="col-md-4"><button class="btn btn-outline-danger w-100 py-3" onclick="selectFile('video')">🎥 Video</button></div>
        <div class="col-md-4"><button class="btn btn-outline-success w-100 py-3" onclick="selectFile('audio')">🎵 Audio</button></div>
    </div>
    <input type="file" id="mediaInput" hidden onchange="doUpload()">
    <div id="status" class="mt-4 fw-bold text-primary"></div>
</div>

<script>
let currentType = '';
function selectFile(type) { 
    currentType = type;
    const input = document.getElementById('mediaInput');
    input.accept = type + "/*";
    input.click(); 
}

async function doUpload() {
    const file = document.getElementById('mediaInput').files[0];
    const status = document.getElementById('status');
    if(!file) return;

    status.innerText = "Uploading " + file.name + "...";
    let fd = new FormData();
    fd.append('file', file);

    try {
        const res = await fetch('/upload/', {
            method: 'POST',
            body: fd,
            headers: {'X-CSRFToken': '{{ csrf_token }}'}
        });
        const data = await res.json();
        if(data.success) {
            status.innerHTML = "✅ Success! Saved in S3: " + data.key;
            status.className = "mt-4 fw-bold text-success";
        } else {
            status.innerText = "❌ Error: " + data.error;
            status.className = "mt-4 fw-bold text-danger";
        }
    } catch(e) { status.innerText = "❌ Upload Failed"; }
}
</script>
{% endblock %}"""
}

# Directories create karna aur files likhna
os.makedirs("core/templates", exist_ok=True)
for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Created: {path}")

print("\\n--- All template files generated successfully! ---")