🐄 Smart Cattle Monitoring System Using Digital Technology
A complete solution to automate and enhance cattle management through IoT sensors, real-time monitoring, and digital interfaces for farmers, veterinary doctors, and government schemes.

📌 Table of Contents
Project Overview

Key Features

Tech Stack

Hardware Components

Software Modules

Firebase Structure

Screenshots

Team

License

📖 Project Overview
The Smart Cattle Monitoring System aims to improve cattle health, productivity, and overall farm management using IoT sensors and web/mobile applications. This system automates disease detection, environmental monitoring, and milk production tracking, all while providing easy access to government schemes and veterinary support.

✨ Key Features
🔧 IoT Monitoring
MLX90614: Measures individual cattle body temperature.

AM2315: Monitors stall barn temperature and activates a 12V motor to spray water when needed.

ENS160: Detects air quality and activates a ventilation fan.

UHF RFID Reader: Identifies and tracks cattle via RFID.

A7672S 4G SIM Module: Transmits sensor data to Firebase in real time.

🌐 Web Application
Buy cattle food online.

View and apply for government schemes.

Monitor individual cattle health and environmental data.

Real-time milk supply analytics.

ML-based cattle disease detection using camera.

Veterinary doctor listings and contact.

📱 Mobile App
Farmers can input daily milk production.

Visualize milk production analytics using graphs.

🧑‍💻 Tech Stack
📡 Hardware
Arduino/ESP32

Sensors: MLX90614, AM2315, ENS160, UHF RFID Reader

GSM: A7672S 4G SIM Module

💻 Software
Frontend: HTML, CSS, JavaScript

Backend: Firebase (Authentication, Realtime Database)

Mobile: React Native / Flutter (optional)

🔌 Firebase Structure
markdown
Copy
Edit
/CattleData
  /<RFID_Tag_ID>
    - temperature
    - airQuality
    - stallTemp
    - timestamp

/MilkData
  /<Farmer_ID>
    - date
    - litersProduced

/Users
  /Farmers
  /Veterinarians

/GovtSchemes
🖼️ Screenshots
