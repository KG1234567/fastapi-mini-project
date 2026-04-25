# 🏥 FastAPI Patient CRUD API

A lightweight backend project built using **FastAPI** to perform CRUD (Create, Read, Update, Delete) operations on patient data stored in a JSON file. This project demonstrates RESTful API design, data validation, and structured backend development.

---

## 🚀 Features

- Create new patient records  
- Retrieve all patients or a specific patient  
- Update existing patient data  
- Delete patient records  
- Data validation using Pydantic  
- JSON-based storage (no database required)  
- Clean and modular API structure  

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **Uvicorn**
- JSON (for data storage)

---

## 📂 Project Structure
fastapi-patient-crud/
│
├── venv
├── main.py # Main FastAPI application
├── patients.json # JSON file storing patient data
└── README.md


---

## ⚙️ Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/fastapi-patient-crud.git
cd fastapi-patient-crud
```

2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. Install dependencies
```bash
pip install fastapi uvicorn pydantic
```

4. Run the Server
```bash
uvicorn main:app --reload
```

## API Endpoints
| Method | Endpoint         | Description        |
| ------ | ---------------- | ------------------ |
| GET    | `/patients`      | Get all patients   |
| GET    | `/patients/{id}` | Get patient by ID  |
| POST   | `/patients`      | Create new patient |
| PUT    | `/patients/{id}` | Update patient     |
| DELETE | `/patients/{id}` | Delete patient     |


## Example Request
Create Patient (POST /create)
{
  "id": P006
  "name": "Kareen",
  "city": "delhi"
  "age": 30,
  "gender": "male"
  "height": 1.57,
  "weight": 65
  "
}

## Learning Outcomes
- Understanding of RESTful APIs
- Working with FastAPI framework
- Data validation using Pydantic
- Handling JSON as a data store
