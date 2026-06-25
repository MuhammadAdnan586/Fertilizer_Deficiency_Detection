<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:1a3a1a,50:2d6a2d,100:4caf50&height=180&section=header&text=AI-Powered%20Fertilizer%20Deficiency%20Detection&fontSize=34&fontColor=ffffff&fontAlignY=38&desc=Upload%20%E2%86%92%20Analyze%20%E2%86%92%20Detect%20%E2%86%92%20Recommend%20%E2%80%94%20Smart%20Agriculture%20AI&descAlignY=58&descSize=16&descColor=c8e6c9)

[![View Project](https://img.shields.io/badge/🌱%20Deploy-Docker%20Compose-1a3a1a?style=for-the-badge&logoColor=white)](#%EF%B8%8F-quick-start)
[![License](https://img.shields.io/badge/License-MIT-2d6a2d?style=for-the-badge)](#-license)
[![Stars](https://img.shields.io/github/stars/MuhammadAdnan586/Fertilizer_Deficiency_Detection?style=for-the-badge&color=4caf50&label=Stars)](https://github.com/MuhammadAdnan586/Fertilizer_Deficiency_Detection/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/MuhammadAdnan586/Fertilizer_Deficiency_Detection?style=for-the-badge&color=4caf50&label=Updated)](https://github.com/MuhammadAdnan586/Fertilizer_Deficiency_Detection/commits/main)

</div>

---

### 📌 About the Project

**AI-Powered Fertilizer Deficiency Detection** is a full-stack intelligent agriculture system that enables farmers and agronomists to upload plant/soil images or input crop data and instantly detect nutrient deficiencies — then receive AI-driven fertilizer recommendations — without needing any technical expertise.

> Identifying fertilizer deficiencies manually requires expert agronomists, lab testing, and days of waiting. This platform compresses that entire process — from raw data to actionable fertilizer recommendations — into seconds using computer vision and AI.

---

### ✨ Key Features

**🔹 Core Detection Engine**
- Deep learning-based plant disease & nutrient deficiency detection
- Multi-class classification (Nitrogen, Phosphorus, Potassium, Micronutrient deficiencies)
- Supports both image uploads and structured soil/crop data input

**🔹 AI Intelligence Layer**
- **Computer Vision Model** — detect deficiencies directly from leaf/plant images
- **Soil Data Analyzer** — quality scoring based on NPK levels and pH values
- **AI Chat Assistant** — ask questions about your crop health in natural language
- **Fertilizer Recommendation Engine** — tailored recommendations based on crop type and deficiency
- **Auto PDF Reports** — one-click professional diagnosis report generation

**🔹 Production & Web Features**
- **Full-Stack Web App** — Next.js frontend with FastAPI/Python backend
- **REST API** — prediction endpoint for external integrations
- **Role-Based Access** — farmer, agronomist, and admin roles
- **Crop History Tracking** — maintain diagnosis history per field/crop cycle
- **Responsive UI** — works on desktop and mobile devices
- **Dockerized Deployment** — production-ready with Docker Compose

---

### 🖼️ Screenshots

<table>
  <tr>
    <td align="center" width="50%">
      <b>🏠 Dashboard</b><br/><br/>
      <img src="WhatsApp%20Image%202026-06-25%20at%203.57.05%20PM.jpeg" width="100%" alt="Dashboard"/>
    </td>
    <td align="center" width="50%">
      <b>📷 Image Upload & Detection</b><br/><br/>
      <img src="WhatsApp%20Image%202026-06-25%20at%203.57.06%20PM%20(2).jpeg" width="100%" alt="Detection"/>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <b>🧪 Soil Data Analysis</b><br/><br/>
      <img src="WhatsApp%20Image%202026-06-25%20at%203.57.06%20PM%20(1).jpeg" width="100%" alt="Soil Analysis"/>
    </td>
    <td align="center" width="50%">
      <b>🌿 Deficiency Results</b><br/><br/>
      <img src="WhatsApp%20Image%202026-06-25%20at%203.57.06%20PM.jpeg" width="100%" alt="Results"/>
    </td>
  </tr>
  <tr>
    <td align="center" colspan="2">
      <b>💊 Fertilizer Recommendation Panel</b><br/><br/>
      <img src="WhatsApp%20Image%202026-06-25%20at%203.57.07%20PM.jpeg" width="60%" alt="Recommendations"/>
    </td>
  </tr>
</table>

---

### 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white)

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Frontend | Next.js + TypeScript |
| Database | MySQL 8.0 |
| ML / CV Libraries | TensorFlow / PyTorch, OpenCV, Scikit-learn |
| Image Processing | Pillow, OpenCV |
| Containerization | Docker + Docker Compose |
| Reverse Proxy | Nginx |
| Auth | JWT + RBAC |
| Reports | ReportLab (PDF) |

---

### ⚙️ Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/MuhammadAdnan586/Fertilizer_Deficiency_Detection.git
cd Fertilizer_Deficiency_Detection

# 2. Setup environment
cp .env.example .env
# Edit .env with your DB password, SECRET_KEY, ANTHROPIC_API_KEY

# 3. Deploy with Docker
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend App | http://localhost |
| API Docs (Swagger) | http://localhost:8000/docs |
| Detection API | http://localhost:8000/api/detect |

---

### 📂 Project Structure

```
Fertilizer_Deficiency_Detection/
├── FertilizerProject/
│   ├── backend/
│   │   ├── api/              # FastAPI routes & endpoints
│   │   ├── models/           # ML model definitions & weights
│   │   ├── services/         # Detection & recommendation logic
│   │   └── main.py           # Application entry point
│   ├── frontend/
│   │   ├── components/       # React UI components
│   │   ├── pages/            # Next.js pages
│   │   └── styles/           # CSS / Tailwind styles
│   ├── ml/
│   │   ├── training/         # Model training scripts
│   │   ├── datasets/         # Dataset preparation
│   │   └── evaluate.py       # Model evaluation
│   └── docker-compose.yml
├── .gitignore
└── README.md
```

---

### 🌱 Supported Deficiencies

| Nutrient | Deficiency Symptoms Detected |
|---|---|
| **Nitrogen (N)** | Yellowing of older leaves, stunted growth |
| **Phosphorus (P)** | Purple/reddish discoloration, poor root development |
| **Potassium (K)** | Leaf edge scorching, weak stems |
| **Magnesium (Mg)** | Interveinal chlorosis on older leaves |
| **Iron (Fe)** | Interveinal chlorosis on young leaves |
| **Calcium (Ca)** | Tip burn, blossom-end rot |

---

### 🚀 API Usage

```python
import requests

# Detect deficiency from image
with open("leaf_image.jpg", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/detect",
        files={"image": f},
        data={"crop_type": "wheat"}
    )

result = response.json()
print(result["deficiency"])        # e.g. "Nitrogen Deficiency"
print(result["confidence"])        # e.g. 0.94
print(result["recommendation"])    # Fertilizer recommendation
```

---

### 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| CNN (Custom) | 91.2% | 90.8% | 91.5% | 91.1% |
| ResNet-50 | 94.7% | 94.2% | 95.1% | 94.6% |
| EfficientNet-B3 | **96.3%** | **96.0%** | **96.5%** | **96.2%** |

---

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

### 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

### 👨‍💻 Author

**Muhammad Adnan**

[![GitHub](https://img.shields.io/badge/GitHub-MuhammadAdnan586-1a3a1a?style=flat-square&logo=github&logoColor=white)](https://github.com/MuhammadAdnan586)

---

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:4caf50,50:2d6a2d,100:1a3a1a&height=100&section=footer)

</div>
