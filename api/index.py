// Simple HTML page for the Business Finder landing page
export default function handler(req, res) {
  res.setHeader('Content-Type', 'text/html');
  
  const html = `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Finder | Page & Brand</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        line-height: 1.6;
        color: #333;
        background-color: #f8f9fa;
      }
      header {
        background-color: #2c3e50;
        color: white;
        padding: 2rem 0;
        text-align: center;
      }
      .container {
        width: 90%;
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 0;
      }
      .hero {
        text-align: center;
        margin-bottom: 3rem;
      }
      .hero h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: white;
      }
      .hero p {
        font-size: 1.2rem;
        color: #ecf0f1;
        max-width: 800px;
        margin: 0 auto;
      }
      .cta-button {
        display: inline-block;
        background-color: #3498db;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 1.5rem;
        transition: background-color 0.3s;
      }
      .cta-button:hover {
        background-color: #2980b9;
      }
      .features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-bottom: 3rem;
      }
      .feature-card {
        background-color: white;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
      }
      .feature-card:hover {
        transform: translateY(-5px);
      }
      .feature-card h3 {
        font-size: 1.5rem;
        margin-bottom: 1rem;
        color: #2c3e50;
      }
      footer {
        background-color: #2c3e50;
        color: white;
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
      }
      .footer-links {
        margin-top: 1rem;
      }
      .footer-links a {
        color: #ecf0f1;
        margin: 0 1rem;
        text-decoration: none;
      }
      .footer-links a:hover {
        text-decoration: underline;
      }
      @media (max-width: 768px) {
        .hero h1 {
          font-size: 2rem;
        }
        .hero p {
          font-size: 1rem;
        }
      }
    </style>
  </head>
  <body>
    <header>
      <div class="container">
        <div class="hero">
          <h1>Business Finder & Website Generator</h1>
          <p>Find local businesses without websites and help them establish their online presence</p>
          <a href="https://pageandbrand.vercel.app" class="cta-button">Visit Page & Brand</a>
        </div>
      </div>
    </header>
    
    <div class="container">
      <div class="features">
        <div class="feature-card">
          <h3>Business Finder Tool</h3>
          <p>Our advanced tool helps you identify local businesses in London and England that don't have websites, creating perfect opportunities for your services.</p>
        </div>
        
        <div class="feature-card">
          <h3>Personalized Outreach</h3>
          <p>Create customized outreach campaigns with templates designed to convert businesses into clients with compelling value propositions.</p>
        </div>
        
        <div class="feature-card">
          <h3>Website Generator</h3>
          <p>Generate professional websites with optional features like booking systems, menus, and more to meet each client's specific needs.</p>
        </div>
        
        <div class="feature-card">
          <h3>Lead Management</h3>
          <p>Track all your potential clients, monitor outreach status, and manage your entire sales pipeline in one convenient dashboard.</p>
        </div>
        
        <div class="feature-card">
          <h3>Calendly Integration</h3>
          <p>Allow clients to book appointments directly through their websites with seamless Calendly integration.</p>
        </div>
        
        <div class="feature-card">
          <h3>Analytics & Insights</h3>
          <p>Measure the effectiveness of your outreach messages and optimize your approach based on real data.</p>
        </div>
      </div>
      
      <div style="text-align: center; margin-top: 2rem;">
        <a href="https://pageandbrand.vercel.app" class="cta-button">Learn More About Our Services</a>
      </div>
    </div>
    
    <footer>
      <div class="container">
        <p>&copy; 2025 Page & Brand. All rights reserved.</p>
        <div class="footer-links">
          <a href="https://pageandbrand.vercel.app">Home</a>
          <a href="https://pageandbrand.vercel.app#services">Services</a>
          <a href="https://pageandbrand.vercel.app#contact">Contact</a>
        </div>
      </div>
    </footer>
  </body>
  </html>
  `;
  
  return res.send(html);
}
