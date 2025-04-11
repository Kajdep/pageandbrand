mkdir -p /home/ubuntu/business_finder_project/pageandbrand/images
cd /home/ubuntu/business_finder_project/pageandbrand/images
# Create placeholder images for the website
echo "Creating placeholder SVG images for the website..."

# Hero image
cat > hero-image.svg << 'EOF'
<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f0f0f0"/>
  <rect x="100" y="50" width="400" height="300" rx="10" fill="#ffffff" stroke="#4e57d4" stroke-width="2"/>
  <rect x="150" y="100" width="300" height="30" rx="5" fill="#4e57d4"/>
  <rect x="150" y="150" width="300" height="10" rx="5" fill="#e0e0e0"/>
  <rect x="150" y="170" width="300" height="10" rx="5" fill="#e0e0e0"/>
  <rect x="150" y="190" width="200" height="10" rx="5" fill="#e0e0e0"/>
  <rect x="150" y="230" width="120" height="40" rx="20" fill="#ff6b6b"/>
  <rect x="280" y="230" width="120" height="40" rx="20" fill="none" stroke="#ff6b6b" stroke-width="2"/>
  <text x="300" y="30" font-family="Arial" font-size="24" fill="#4e57d4" text-anchor="middle">Page &amp; Brand</text>
</svg>
EOF

# Create portfolio images
for i in {1..6}; do
  cat > portfolio-$i.jpg << EOF
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f0f0f0"/>
  <rect x="50" y="50" width="300" height="200" rx="10" fill="#ffffff" stroke="#4e57d4" stroke-width="2"/>
  <text x="200" y="150" font-family="Arial" font-size="24" fill="#4e57d4" text-anchor="middle">Portfolio $i</text>
</svg>
EOF
done

# Create testimonial images
for i in {1..3}; do
  cat > testimonial-$i.jpg << EOF
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="45" fill="#4e57d4"/>
  <text x="50" y="55" font-family="Arial" font-size="24" fill="#ffffff" text-anchor="middle">T$i</text>
</svg>
EOF
done

echo "Placeholder images created successfully."
