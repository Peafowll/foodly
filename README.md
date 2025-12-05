# 🍽️ Foodly

An MVP for an AI-powered food recognition and recipe suggestion application that helps you discover recipes based on ingredients you have at home.

## 🏆 Achievements

### EduTech Hackathon #4 (Nov 18-20, 2024)
- **Team:** EcoBites
- **Coding Team Members:** Paun Tudor & Vatajita Teodor
- **Result:** 🥉 3rd Place out of 18 teams
- **Features:** Food scanning via laptop camera using Google Vision API and CV2

### InnovationLabs Bucharest Hackathon (March 8-9, 2025)
- **Team:** Foodly
- **Coding Team Members:** Paun Tudor & Vatajita Teodor
- **Development Time:** ~15 hours (9:30 AM March 8th → 12:43 AM March 9th)

## ✨ Features

- **🔍 Real-time Food Detection** - Uses YOLOv8 AI model to identify food items through your webcam
- **📖 Recipe Suggestions** - Matches detected ingredients against a recipe database
- **🏪 Nearby Store Locator** - Finds partner hypermarkets near you using OpenStreetMap's Overpass API
- **📊 Smart Sorting** - Recipes sorted by missing ingredients count
- **🗺️ Google Maps Integration** - Direct links to navigate to nearby stores

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **YOLOv8** | Real-time object detection for food recognition |
| **OpenCV (cv2)** | Webcam capture and image processing |
| **Tkinter** | Desktop GUI application |
| **Overpass API** | Query nearby supermarkets from OpenStreetMap |
| **Geocoder** | IP-based location detection |

## 📁 Project Structure

```
foodly/
├── main.py              # Main GUI application with recipe and store display
├── yolo_cam.py          # YOLO-based webcam food detection
├── scan_get_recipes.py  # Recipe matching logic
├── store_loc.py         # Nearby store locator using Overpass API
├── location.py          # Location utilities
├── recipes.json         # Recipe database with ingredients
├── partners. list        # List of partner store names
└── yolov8n.pt           # Pre-trained YOLOv8 nano model
```

## 🚀 How It Works

1. **Scan** - Point your webcam at food items; press 'Q' when done scanning
2. **Match** - The app matches detected ingredients against the recipe database
3.  **Browse** - View suggested recipes sorted by fewest missing ingredients
4. **Shop** - Double-click a recipe to see nearby partner stores where you can buy missing ingredients

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Peafowll/foodly.git
cd foodly

# Install dependencies
pip install ultralytics opencv-python tkinter requests geocoder

# Run the application
python main.py
```

## 🎯 Detectable Food Items

The application uses COCO dataset food classes (IDs 46-51):
- Banana, Apple, Sandwich, Orange, Broccoli, Carrot

## 📝 License

This project was created for educational and hackathon purposes. 
