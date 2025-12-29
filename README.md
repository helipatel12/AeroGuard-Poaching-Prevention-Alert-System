# AeroGuard: Poaching Prevention Alert System

AeroGuard is an AI-powered surveillance and alert system designed to help prevent wildlife poaching by detecting suspicious human activity in protected areas and notifying authorities in real time. The system focuses on intelligent monitoring, data analysis, and fast alert generation to support wildlife conservation efforts.

---

## 📌 Project Overview

Poaching remains one of the biggest threats to wildlife, especially endangered species like elephants. Traditional monitoring methods are slow, resource-intensive, and often ineffective over large forest areas.

AeroGuard addresses this challenge by using:
- Computer Vision
- Machine Learning
- Thermal and infrared image analysis
- Real-time alert mechanisms

The system detects humans, animals, and vehicles from surveillance imagery and sends alerts with location and visual evidence to concerned authorities.

---

## 🎯 Objectives

- Detect human intrusion in protected wildlife areas  
- Differentiate between humans, animals, and vehicles  
- Generate real-time alerts for suspicious activity  
- Improve response time for anti-poaching teams  
- Support scalable and technology-driven conservation efforts  

---

## 🧠 Key Features

- **AI-Based Detection**  
  Uses deep learning models (YOLO-based) for object detection and classification.

- **Thermal & Infrared Image Support**  
  Works effectively in low-light and night conditions.

- **Real-Time Alerts**  
  Sends instant notifications with location data and captured images.

- **Scalable Architecture**  
  Can be extended to different wildlife reserves and conservation use cases.

- **Data Logging & Analysis**  
  Stores detection data for monitoring trends and future improvements.

---

## 🏗️ System Architecture (High Level)

1. Image acquisition from surveillance sources  
2. Image preprocessing and noise reduction  
3. AI-based object detection and classification  
4. Threat evaluation logic  
5. Alert generation with metadata (time, location, image)  
6. Centralized data storage and monitoring interface  

---

## 📊 Dataset

- Uses aerial thermal infrared (TIR) and RGB image datasets  
- Includes both **real** and **synthetic** data  
- Annotated with:
  - Bounding boxes
  - Class labels (human, animal, unknown)
  - Species information
- Dataset converted to **COCO format** for model compatibility  

---

## 🧪 Model & Technologies Used

- **Programming Language:** Python  
- **Computer Vision:** OpenCV  
- **Deep Learning Model:** YOLOv5  
- **Frameworks & Tools:**  
  - PyTorch  
  - NumPy  
  - Pandas  
  - Flask (for alert server / API)

---

## 📈 Results (Summary)

- High detection accuracy for humans and animals  
- Effective performance during day and night scenarios  
- Reduced response time through instant alerts  
- Robust performance across varied environmental conditions  

---

## 🔮 Proposed Enhancements

- Mobile application for field officers  
- Integration of sound and environmental sensors  
- Expansion to multi-species monitoring  
- Improved UI dashboard for analytics  
- Model optimization for faster inference  

---

## 👥 Team Members

- **Aarya Mehta** – 21124001 (https://github.com/AaryaMehta2506)  
- **Heli Patel** – 21124015  (https://github.com/helipatel12)
- **Khushi Gajjar** – 21124022  (https://github.com/Khushigajjar)

---

## 🏫 Academic Details

- **Degree:** Bachelor of Technology (B.Tech)  
- **Department:** Computer Science and Engineering  
- **University:** Navrachana University, Vadodara  
- **Academic Year:** 2024–25  
- **Project Guide:** Prof. Yogesh Chaudhari  

---

## 📜 Disclaimer

This project is developed for academic and research purposes. It demonstrates the application of AI and computer vision in wildlife conservation and anti-poaching systems.

---

## 🌱 Conclusion

AeroGuard showcases how modern AI-driven surveillance systems can significantly enhance wildlife protection efforts. By combining intelligent detection with real-time alerts, the system contributes toward safeguarding endangered species and promoting biodiversity conservation.
