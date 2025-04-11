#!/usr/bin/env python3
"""
Website Generator Module

This script provides functionality to generate websites for businesses based on templates
and customizable options.
"""

import os
import sys
import json
import shutil
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

class WebsiteGenerator:
    """Class for generating websites for businesses."""
    
    def __init__(self, templates_dir=None, output_dir=None):
        """Initialize the WebsiteGenerator with template and output directories."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.templates_dir = templates_dir or os.path.join(base_dir, 'website_generator', 'templates')
        self.output_dir = output_dir or os.path.join(base_dir, 'website_generator', 'output')
        
        # Create directories if they don't exist
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        
        # Load available templates
        self.templates = self._load_templates()
        
        # Load available features
        self.features = self._load_features()
    
    def _load_templates(self):
        """Load available website templates."""
        templates = {
            'modern': {
                'name': 'Modern',
                'description': 'A sleek, contemporary design with smooth animations and modern aesthetics.',
                'preview_image': 'modern_preview.jpg',
                'files': ['index.html', 'style.css', 'script.js']
            },
            'classic': {
                'name': 'Classic',
                'description': 'A timeless design with elegant typography and traditional layout.',
                'preview_image': 'classic_preview.jpg',
                'files': ['index.html', 'style.css', 'script.js']
            },
            'minimal': {
                'name': 'Minimal',
                'description': 'A clean, minimalist design focusing on content and readability.',
                'preview_image': 'minimal_preview.jpg',
                'files': ['index.html', 'style.css', 'script.js']
            }
        }
        
        # Create template files if they don't exist
        for template_id, template in templates.items():
            template_dir = os.path.join(self.templates_dir, template_id)
            os.makedirs(template_dir, exist_ok=True)
            
            for file in template['files']:
                file_path = os.path.join(template_dir, file)
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        if file == 'index.html':
                            f.write(self._generate_template_html(template_id))
                        elif file == 'style.css':
                            f.write(self._generate_template_css(template_id))
                        elif file == 'script.js':
                            f.write(self._generate_template_js(template_id))
        
        return templates
    
    def _load_features(self):
        """Load available website features."""
        return {
            'booking': {
                'name': 'Booking System',
                'description': 'Allow customers to book appointments or reservations.',
                'files': ['booking.html', 'booking.css', 'booking.js']
            },
            'menu': {
                'name': 'Menu Display',
                'description': 'Display menu items with prices and descriptions.',
                'files': ['menu.html', 'menu.css', 'menu.js']
            },
            'gallery': {
                'name': 'Photo Gallery',
                'description': 'Showcase photos in an interactive gallery.',
                'files': ['gallery.html', 'gallery.css', 'gallery.js']
            },
            'testimonials': {
                'name': 'Testimonials',
                'description': 'Display customer testimonials and reviews.',
                'files': ['testimonials.html', 'testimonials.css', 'testimonials.js']
            },
            'contact_form': {
                'name': 'Contact Form',
                'description': 'Include a contact form for customer inquiries.',
                'files': ['contact.html', 'contact.css', 'contact.js']
            },
            'social_media': {
                'name': 'Social Media Integration',
                'description': 'Integrate social media feeds and sharing buttons.',
                'files': ['social.html', 'social.css', 'social.js']
            },
            'calendly': {
                'name': 'Calendly Integration',
                'description': 'Integrate Calendly for appointment scheduling.',
                'files': ['calendly.html', 'calendly.css', 'calendly.js']
            }
        }
    
    def _generate_template_html(self, template_id):
        """Generate HTML template file based on template ID."""
        if template_id == 'modern':
            return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ business.name }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="modern-template">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="#">{{ business.name }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#about">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#services">Services</a>
                    </li>
                    {% if features.gallery %}
                    <li class="nav-item">
                        <a class="nav-link" href="#gallery">Gallery</a>
                    </li>
                    {% endif %}
                    {% if features.menu %}
                    <li class="nav-item">
                        <a class="nav-link" href="#menu">Menu</a>
                    </li>
                    {% endif %}
                    {% if features.booking %}
                    <li class="nav-item">
                        <a class="nav-link" href="#booking">Book Now</a>
                    </li>
                    {% endif %}
                    <li class="nav-item">
                        <a class="nav-link" href="#contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    
    <section class="hero">
        <div class="container">
            <h1>{{ business.name }}</h1>
            <p class="lead">{{ business.category }}</p>
            <button class="btn btn-light btn-lg mt-3">Learn More</button>
        </div>
    </section>
    
    <section class="py-5" id="about">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto text-center">
                    <h2 class="mb-4">About Us</h2>
                    <p class="lead">{{ business.description }}</p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="py-5 bg-light" id="services">
        <div class="container">
            <h2 class="text-center mb-4">Our Services</h2>
            <div class="row">
                {% for service in business.services %}
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body text-center">
                            <h5 class="card-title">{{ service.name }}</h5>
                            <p class="card-text">{{ service.description }}</p>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    
    {% if features.gallery %}
    {% include 'gallery.html' %}
    {% endif %}
    
    {% if features.menu %}
    {% include 'menu.html' %}
    {% endif %}
    
    {% if features.testimonials %}
    {% include 'testimonials.html' %}
    {% endif %}
    
    {% if features.booking %}
    {% include 'booking.html' %}
    {% endif %}
    
    {% if features.calendly %}
    {% include 'calendly.html' %}
    {% endif %}
    
    <section class="py-5" id="contact">
        <div class="container">
            <h2 class="text-center mb-4">Contact Us</h2>
            <div class="row">
                <div class="col-md-6 mb-4">
                    <h5>Get in Touch</h5>
                    <p><i class="bi bi-geo-alt"></i> {{ business.address }}</p>
                    <p><i class="bi bi-telephone"></i> {{ business.phone }}</p>
                    <p><i class="bi bi-envelope"></i> {{ business.email }}</p>
                </div>
                <div class="col-md-6 mb-4">
                    {% if features.contact_form %}
                    {% include 'contact.html' %}
                    {% else %}
                    <h5>Send Us a Message</h5>
                    <form>
                        <div class="mb-3">
                            <input type="text" class="form-control" placeholder="Your Name" required>
                        </div>
                        <div class="mb-3">
                            <input type="email" class="form-control" placeholder="Your Email" required>
                        </div>
                        <div class="mb-3">
                            <textarea class="form-control" rows="3" placeholder="Your Message" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </form>
                    {% endif %}
                </div>
            </div>
        </div>
    </section>
    
    {% if features.social_media %}
    {% include 'social.html' %}
    {% endif %}
    
    <footer class="py-4 bg-dark text-white">
        <div class="container text-center">
            <p>&copy; {{ current_year }} {{ business.name }}. All rights reserved.</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""
        elif template_id == 'classic':
            return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ business.name }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="classic-template">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container">
            <a class="navbar-brand" href="#">{{ business.name }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#about">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#services">Services</a>
                    </li>
                    {% if features.gallery %}
                    <li class="nav-item">
                        <a class="nav-link" href="#gallery">Gallery</a>
                    </li>
                    {% endif %}
                    {% if features.menu %}
                    <li class="nav-item">
                        <a class="nav-link" href="#menu">Menu</a>
                    </li>
                    {% endif %}
                    {% if features.booking %}
                    <li class="nav-item">
                        <a class="nav-link" href="#booking">Book Now</a>
                    </li>
                    {% endif %}
                    <li class="nav-item">
                        <a class="nav-link" href="#contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    
    <header class="py-5 bg-image-full" style="background-image: url('https://via.placeholder.com/1920x500');">
        <div class="text-center my-5">
            <h1 class="text-white fs-3 fw-bolder">{{ business.name }}</h1>
            <p class="text-white-50 mb-0">{{ business.category }}</p>
        </div>
    </header>
    
    <section class="py-5" id="about">
        <div class="container">
            <div class="row">
                <div class="col-lg-8 mx-auto">
                    <h2>About Us</h2>
                    <hr class="divider">
                    <p class="lead">{{ business.description }}</p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="py-5 bg-light" id="services">
        <div class="container">
            <h2 class="text-center">Our Services</h2>
            <hr class="divider">
            <div class="row">
                {% for service in business.services %}
                <div class="col-md-4 mb-4">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">{{ service.name }}</h5>
                            <p class="card-text">{{ service.description }}</p>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    
    {% if features.gallery %}
    {% include 'gallery.html' %}
    {% endif %}
    
    {% if features.menu %}
    {% include 'menu.html' %}
    {% endif %}
    
    {% if features.testimonials %}
    {% include 'testimonials.html' %}
    {% endif %}
    
    {% if features.booking %}
    {% include 'booking.html' %}
    {% endif %}
    
    {% if features.calendly %}
    {% include 'calendly.html' %}
    {% endif %}
    
    <section class="py-5" id="contact">
        <div class="container">
            <h2 class="text-center">Contact Us</h2>
            <hr class="divider">
            <div class="row">
                <div class="col-md-6 mb-4">
                    <h5>Get in Touch</h5>
                    <p><i class="bi bi-geo-alt"></i> {{ business.address }}</p>
                    <p><i class="bi bi-telephone"></i> {{ business.phone }}</p>
                    <p><i class="bi bi-envelope"></i> {{ business.email }}</p>
                </div>
                <div class="col-md-6 mb-4">
                    {% if features.contact_form %}
                    {% include 'contact.html' %}
                    {% else %}
                    <h5>Send Us a Message</h5>
                    <form>
                        <div class="mb-3">
                            <input type="text" class="form-control" placeholder="Your Name" required>
                        </div>
                        <div class="mb-3">
                            <input type="email" class="form-control" placeholder="Your Email" required>
                        </div>
                        <div class="mb-3">
                            <textarea class="form-control" rows="3" placeholder="Your Message" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </form>
                    {% endif %}
                </div>
            </div>
        </div>
    </section>
    
    {% if features.social_media %}
    {% include 'social.html' %}
    {% endif %}
    
    <footer class="py-4 bg-dark text-white">
        <div class="container text-center">
            <p>&copy; {{ current_year }} {{ business.name }}. All rights reserved.</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""
        else:  # minimal
            return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ business.name }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.3/font/bootstrap-icons.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="minimal-template">
    <nav class="navbar navbar-expand-lg navbar-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">{{ business.name }}</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#about">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#services">Services</a>
                    </li>
                    {% if features.gallery %}
                    <li class="nav-item">
                        <a class="nav-link" href="#gallery">Gallery</a>
                    </li>
                    {% endif %}
                    {% if features.menu %}
                    <li class="nav-item">
                        <a class="nav-link" href="#menu">Menu</a>
                    </li>
                    {% endif %}
                    {% if features.booking %}
                    <li class="nav-item">
                        <a class="nav-link" href="#booking">Book Now</a>
                    </li>
                    {% endif %}
                    <li class="nav-item">
                        <a class="nav-link" href="#contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    
    <section class="hero">
        <div class="container">
            <h1>{{ business.name }}</h1>
            <p>{{ business.category }}</p>
        </div>
    </section>
    
    <section class="py-5" id="about">
        <div class="container">
            <h2>About Us</h2>
            <p>{{ business.description }}</p>
        </div>
    </section>
    
    <section class="py-5 bg-light" id="services">
        <div class="container">
            <h2>Our Services</h2>
            <div class="row">
                {% for service in business.services %}
                <div class="col-md-4 mb-4">
                    <h5>{{ service.name }}</h5>
                    <p>{{ service.description }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </section>
    
    {% if features.gallery %}
    {% include 'gallery.html' %}
    {% endif %}
    
    {% if features.menu %}
    {% include 'menu.html' %}
    {% endif %}
    
    {% if features.testimonials %}
    {% include 'testimonials.html' %}
    {% endif %}
    
    {% if features.booking %}
    {% include 'booking.html' %}
    {% endif %}
    
    {% if features.calendly %}
    {% include 'calendly.html' %}
    {% endif %}
    
    <section class="py-5" id="contact">
        <div class="container">
            <h2>Contact Us</h2>
            <div class="row">
                <div class="col-md-6 mb-4">
                    <p><i class="bi bi-geo-alt"></i> {{ business.address }}</p>
                    <p><i class="bi bi-telephone"></i> {{ business.phone }}</p>
                    <p><i class="bi bi-envelope"></i> {{ business.email }}</p>
                </div>
                <div class="col-md-6 mb-4">
                    {% if features.contact_form %}
                    {% include 'contact.html' %}
                    {% else %}
                    <form>
                        <div class="mb-3">
                            <input type="text" class="form-control" placeholder="Your Name" required>
                        </div>
                        <div class="mb-3">
                            <input type="email" class="form-control" placeholder="Your Email" required>
                        </div>
                        <div class="mb-3">
                            <textarea class="form-control" rows="3" placeholder="Your Message" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </form>
                    {% endif %}
                </div>
            </div>
        </div>
    </section>
    
    {% if features.social_media %}
    {% include 'social.html' %}
    {% endif %}
    
    <footer class="py-4">
        <div class="container text-center">
            <p>&copy; {{ current_year }} {{ business.name }}. All rights reserved.</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""
    
    def _generate_template_css(self, template_id):
        """Generate CSS template file based on template ID."""
        if template_id == 'modern':
            return """:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --accent-color: #0dcaf0;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.btn-primary:hover {
    background-color: var(--accent-color);
    border-color: var(--accent-color);
}

.hero {
    background-color: var(--primary-color);
    color: white;
    padding: 100px 0;
    text-align: center;
    border-radius: 0 0 50% 50% / 20%;
}

.modern-template h2 {
    position: relative;
    display: inline-block;
    margin-bottom: 30px;
}

.modern-template h2:after {
    content: '';
    position: absolute;
    width: 50%;
    height: 3px;
    background-color: var(--primary-color);
    bottom: -10px;
    left: 25%;
}

.card {
    transition: transform 0.3s;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.card:hover {
    transform: translateY(-10px);
}"""
        elif template_id == 'classic':
            return """:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --accent-color: #0dcaf0;
}

body {
    font-family: 'Georgia', serif;
}

.btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.btn-primary:hover {
    background-color: var(--accent-color);
    border-color: var(--accent-color);
}

.bg-image-full {
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    height: 400px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.classic-template h1, .classic-template h2, .classic-template h3, .classic-template h4, .classic-template h5 {
    font-family: 'Times New Roman', Times, serif;
}

.divider {
    max-width: 3.25rem;
    border-width: 0.2rem;
    border-color: var(--primary-color);
    margin: 1.5rem auto;
}

.card {
    border: none;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}"""
        else:  # minimal
            return """:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --accent-color: #0dcaf0;
}

body {
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
    color: #333;
}

.btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

.btn-primary:hover {
    background-color: var(--accent-color);
    border-color: var(--accent-color);
}

.hero {
    padding: 80px 0;
    text-align: center;
    border-bottom: 3px solid var(--primary-color);
}

.minimal-template h1, .minimal-template h2, .minimal-template h3, .minimal-template h4, .minimal-template h5 {
    font-weight: 300;
}

.minimal-template h2 {
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 10px;
}

.minimal-template section {
    max-width: 800px;
    margin: 0 auto;
}"""
    
    def _generate_template_js(self, template_id):
        """Generate JavaScript template file based on template ID."""
        return """document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Form submission handling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Form submission functionality would be implemented in a production environment.');
        });
    });
});"""
    
    def _create_feature_files(self, features):
        """Create feature template files."""
        for feature_id, feature in self.features.items():
            if feature_id in features and features[feature_id]:
                feature_dir = os.path.join(self.templates_dir, 'features', feature_id)
                os.makedirs(feature_dir, exist_ok=True)
                
                for file in feature['files']:
                    file_path = os.path.join(self.templates_dir, file)
                    if not os.path.exists(file_path):
                        with open(file_path, 'w') as f:
                            if file == 'booking.html':
                                f.write(self._generate_booking_html())
                            elif file == 'menu.html':
                                f.write(self._generate_menu_html())
                            elif file == 'gallery.html':
                                f.write(self._generate_gallery_html())
                            elif file == 'testimonials.html':
                                f.write(self._generate_testimonials_html())
                            elif file == 'contact.html':
                                f.write(self._generate_contact_html())
                            elif file == 'social.html':
                                f.write(self._generate_social_html())
                            elif file == 'calendly.html':
                                f.write(self._generate_calendly_html())
    
    def _generate_booking_html(self):
        """Generate booking feature HTML."""
        return """<section class="py-5 bg-light" id="booking">
    <div class="container">
        <h2 class="text-center mb-4">Book an Appointment</h2>
        <div class="row justify-content-center">
            <div class="col-md-8">
                <form id="bookingForm">
                    <div class="mb-3">
                        <label for="name" class="form-label">Your Name</label>
                        <input type="text" class="form-control" id="name" required>
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email Address</label>
                        <input type="email" class="form-control" id="email" required>
                    </div>
                    <div class="mb-3">
                        <label for="phone" class="form-label">Phone Number</label>
                        <input type="tel" class="form-control" id="phone">
                    </div>
                    <div class="mb-3">
                        <label for="date" class="form-label">Preferred Date</label>
                        <input type="date" class="form-control" id="date" required>
                    </div>
                    <div class="mb-3">
                        <label for="time" class="form-label">Preferred Time</label>
                        <input type="time" class="form-control" id="time" required>
                    </div>
                    <div class="mb-3">
                        <label for="message" class="form-label">Additional Information</label>
                        <textarea class="form-control" id="message" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Book Now</button>
                </form>
            </div>
        </div>
    </div>
</section>"""
    
    def _generate_menu_html(self):
        """Generate menu feature HTML."""
        return """<section class="py-5" id="menu">
    <div class="container">
        <h2 class="text-center mb-4">Our Menu</h2>
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">{{ menu_categories[0].name }}</h5>
                        <ul class="list-group list-group-flush">
                            {% for item in menu_categories[0].items %}
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                {{ item.name }}
                                <span>{{ item.price }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">{{ menu_categories[1].name }}</h5>
                        <ul class="list-group list-group-flush">
                            {% for item in menu_categories[1].items %}
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                {{ item.name }}
                                <span>{{ item.price }}</span>
                            </li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>"""
    
    def _generate_gallery_html(self):
        """Generate gallery feature HTML."""
        return """<section class="py-5 bg-light" id="gallery">
    <div class="container">
        <h2 class="text-center mb-4">Photo Gallery</h2>
        <div class="row">
            {% for image in gallery_images %}
            <div class="col-md-4 mb-4">
                <img src="{{ image.url }}" class="img-fluid rounded" alt="{{ image.alt }}">
            </div>
            {% endfor %}
        </div>
    </div>
</section>"""
    
    def _generate_testimonials_html(self):
        """Generate testimonials feature HTML."""
        return """<section class="py-5" id="testimonials">
    <div class="container">
        <h2 class="text-center mb-4">What Our Customers Say</h2>
        <div class="row">
            {% for testimonial in testimonials %}
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-body">
                        <p class="card-text">"{{ testimonial.text }}"</p>
                        <p class="card-text"><small class="text-muted">- {{ testimonial.author }}</small></p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</section>"""
    
    def _generate_contact_html(self):
        """Generate contact form feature HTML."""
        return """<h5>Send Us a Message</h5>
<form id="contactForm">
    <div class="mb-3">
        <label for="contactName" class="form-label">Your Name</label>
        <input type="text" class="form-control" id="contactName" required>
    </div>
    <div class="mb-3">
        <label for="contactEmail" class="form-label">Email Address</label>
        <input type="email" class="form-control" id="contactEmail" required>
    </div>
    <div class="mb-3">
        <label for="contactSubject" class="form-label">Subject</label>
        <input type="text" class="form-control" id="contactSubject">
    </div>
    <div class="mb-3">
        <label for="contactMessage" class="form-label">Message</label>
        <textarea class="form-control" id="contactMessage" rows="3" required></textarea>
    </div>
    <button type="submit" class="btn btn-primary">Send Message</button>
</form>"""
    
    def _generate_social_html(self):
        """Generate social media feature HTML."""
        return """<section class="py-4 bg-light" id="social">
    <div class="container text-center">
        <h5>Connect With Us</h5>
        <div class="social-icons">
            {% if business.social.facebook %}
            <a href="{{ business.social.facebook }}" class="mx-2" target="_blank">
                <i class="bi bi-facebook fs-3"></i>
            </a>
            {% endif %}
            {% if business.social.twitter %}
            <a href="{{ business.social.twitter }}" class="mx-2" target="_blank">
                <i class="bi bi-twitter fs-3"></i>
            </a>
            {% endif %}
            {% if business.social.instagram %}
            <a href="{{ business.social.instagram }}" class="mx-2" target="_blank">
                <i class="bi bi-instagram fs-3"></i>
            </a>
            {% endif %}
            {% if business.social.linkedin %}
            <a href="{{ business.social.linkedin }}" class="mx-2" target="_blank">
                <i class="bi bi-linkedin fs-3"></i>
            </a>
            {% endif %}
        </div>
    </div>
</section>"""
    
    def _generate_calendly_html(self):
        """Generate Calendly integration feature HTML."""
        return """<section class="py-5 bg-light" id="calendly">
    <div class="container">
        <h2 class="text-center mb-4">Schedule an Appointment</h2>
        <div class="row justify-content-center">
            <div class="col-md-10">
                <div class="calendly-inline-widget" data-url="{{ calendly.url }}" style="min-width:320px;height:630px;"></div>
                <script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>
            </div>
        </div>
    </div>
</section>"""
    
    def generate_website(self, business_data, template_id, color_scheme, features, output_dir=None):
        """Generate a website for a business based on template and features."""
        if template_id not in self.templates:
            raise ValueError(f"Template '{template_id}' not found")
        
        # Create output directory
        business_slug = business_data['name'].lower().replace(' ', '_')
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        website_dir = output_dir or os.path.join(self.output_dir, f"{business_slug}_{timestamp}")
        os.makedirs(website_dir, exist_ok=True)
        
        # Create feature files
        self._create_feature_files(features)
        
        # Copy template files
        template_dir = os.path.join(self.templates_dir, template_id)
        for file in self.templates[template_id]['files']:
            src_path = os.path.join(template_dir, file)
            dst_path = os.path.join(website_dir, file)
            
            if file == 'index.html':
                # Render HTML template
                template = self.env.get_template(os.path.join(template_id, file))
                
                # Prepare context data
                context = {
                    'business': business_data,
                    'features': features,
                    'color_scheme': color_scheme,
                    'current_year': datetime.now().year,
                    'menu_categories': [
                        {
                            'name': 'Appetizers',
                            'items': [
                                {'name': 'Garlic Bread', 'price': '$5.99'},
                                {'name': 'Mozzarella Sticks', 'price': '$7.99'},
                                {'name': 'Bruschetta', 'price': '$6.99'}
                            ]
                        },
                        {
                            'name': 'Main Courses',
                            'items': [
                                {'name': 'Spaghetti Bolognese', 'price': '$12.99'},
                                {'name': 'Chicken Parmesan', 'price': '$14.99'},
                                {'name': 'Grilled Salmon', 'price': '$16.99'}
                            ]
                        }
                    ],
                    'gallery_images': [
                        {'url': 'https://via.placeholder.com/300x200?text=Photo+1', 'alt': 'Gallery Image 1'},
                        {'url': 'https://via.placeholder.com/300x200?text=Photo+2', 'alt': 'Gallery Image 2'},
                        {'url': 'https://via.placeholder.com/300x200?text=Photo+3', 'alt': 'Gallery Image 3'},
                        {'url': 'https://via.placeholder.com/300x200?text=Photo+4', 'alt': 'Gallery Image 4'},
                        {'url': 'https://via.placeholder.com/300x200?text=Photo+5', 'alt': 'Gallery Image 5'},
                        {'url': 'https://via.placeholder.com/300x200?text=Photo+6', 'alt': 'Gallery Image 6'}
                    ],
                    'testimonials': [
                        {'text': 'Absolutely fantastic service! I couldn\'t be happier with the results.', 'author': 'John Smith'},
                        {'text': 'Professional, prompt, and reasonably priced. Would definitely recommend!', 'author': 'Jane Doe'},
                        {'text': 'The best in town! I\'ve been a loyal customer for years and have never been disappointed.', 'author': 'Mike Johnson'}
                    ],
                    'calendly': {
                        'url': business_data.get('calendly', {}).get('link', 'https://calendly.com/yourusername/30min')
                    }
                }
                
                # Render template
                rendered_html = template.render(**context)
                
                # Write rendered HTML to file
                with open(dst_path, 'w') as f:
                    f.write(rendered_html)
            elif file == 'style.css':
                # Modify CSS based on color scheme
                with open(src_path, 'r') as f:
                    css_content = f.read()
                
                # Replace color variables
                if color_scheme == 'blue':
                    css_content = css_content.replace('--primary-color: #0d6efd;', '--primary-color: #0d6efd;')
                    css_content = css_content.replace('--accent-color: #0dcaf0;', '--accent-color: #0dcaf0;')
                elif color_scheme == 'green':
                    css_content = css_content.replace('--primary-color: #0d6efd;', '--primary-color: #198754;')
                    css_content = css_content.replace('--accent-color: #0dcaf0;', '--accent-color: #20c997;')
                elif color_scheme == 'red':
                    css_content = css_content.replace('--primary-color: #0d6efd;', '--primary-color: #dc3545;')
                    css_content = css_content.replace('--accent-color: #0dcaf0;', '--accent-color: #fd7e14;')
                elif color_scheme == 'purple':
                    css_content = css_content.replace('--primary-color: #0d6efd;', '--primary-color: #6f42c1;')
                    css_content = css_content.replace('--accent-color: #0dcaf0;', '--accent-color: #d63384;')
                
                # Write modified CSS to file
                with open(dst_path, 'w') as f:
                    f.write(css_content)
            else:
                # Copy file as is
                shutil.copy2(src_path, dst_path)
        
        # Copy feature files if enabled
        for feature_id, enabled in features.items():
            if enabled and feature_id in self.features:
                for file in self.features[feature_id]['files']:
                    src_path = os.path.join(self.templates_dir, file)
                    dst_path = os.path.join(website_dir, file)
                    
                    if os.path.exists(src_path):
                        shutil.copy2(src_path, dst_path)
        
        # Create metadata file
        metadata = {
            'business': business_data,
            'template': template_id,
            'color_scheme': color_scheme,
            'features': features,
            'generated_at': datetime.now().isoformat()
        }
        
        with open(os.path.join(website_dir, 'metadata.json'), 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return website_dir
    
    def get_templates(self):
        """Get available templates."""
        return self.templates
    
    def get_features(self):
        """Get available features."""
        return self.features
    
    def get_generated_websites(self):
        """Get list of generated websites."""
        websites = []
        
        for item in os.listdir(self.output_dir):
            item_path = os.path.join(self.output_dir, item)
            if os.path.isdir(item_path):
                metadata_path = os.path.join(item_path, 'metadata.json')
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                    
                    websites.append({
                        'id': item,
                        'path': item_path,
                        'metadata': metadata
                    })
        
        return websites

def main():
    """Run the website generator as a standalone script."""
    generator = WebsiteGenerator()
    
    # Example business data
    business_data = {
        'name': 'Delicious Corner Cafe',
        'category': 'Restaurant',
        'description': 'A cozy cafe serving delicious breakfast and lunch options with a focus on locally sourced ingredients.',
        'address': '123 Main St, London, UK',
        'phone': '+44 20 1234 5678',
        'email': 'info@deliciouscorner.com',
        'services': [
            {
                'name': 'Breakfast',
                'description': 'Start your day with our delicious breakfast options.'
            },
            {
                'name': 'Lunch',
                'description': 'Enjoy a satisfying lunch with our fresh, locally sourced ingredients.'
            },
            {
                'name': 'Catering',
                'description': 'Let us cater your next event with our delicious food.'
            }
        ],
        'social': {
            'facebook': 'https://facebook.com/deliciouscorner',
            'instagram': 'https://instagram.com/deliciouscorner',
            'twitter': 'https://twitter.com/deliciouscorner'
        },
        'calendly': {
            'link': 'https://calendly.com/deliciouscorner/reservation'
        }
    }
    
    # Generate website
    website_dir = generator.generate_website(
        business_data=business_data,
        template_id='modern',
        color_scheme='blue',
        features={
            'booking': True,
            'menu': True,
            'gallery': True,
            'testimonials': True,
            'contact_form': True,
            'social_media': True,
            'calendly': False
        }
    )
    
    print(f"Website generated at: {website_dir}")

if __name__ == '__main__':
    main()
