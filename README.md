# 🏢 Organization Management API

A modern, minimal, and scalable RESTful API built using **FastAPI** and **SQLAlchemy** to perform full CRUD operations on organizations.

---

## 🚀 Features

- ✅ Create new organizations
- 📋 Retrieve a list of organizations *(enhancement suggested)*
- ✏️ Update existing organization details *(enhancement suggested)*
- ❌ Delete organizations *(enhancement suggested)*
- 🗂️ Auto-generated API documentation via Swagger UI (`/docs`)
- ⚙️ Flexible database support: PostgreSQL or SQLite

---

## 👨‍💻 Author

- [@fehedcv](https://github.com/fehedcv)

## 🤝 Contributors

- [@ReverseEngineeringDude](https://github.com/ReverseEngineeringDude)
- [@ShahadThayyil](https://github.com/ShahadThayyil)
- [@Noormhmd07](https://github.com/Noormhmd07)

---

## 📦 Installation Guide

### 1. 🌀 Fork the Repository

Start by forking this repository to your own GitHub account:  
👉 [Click here to Fork](https://github.com/fehedcv/internship-1/fork)

### 2. 📥 Clone the Project

Copy the forked project link and run:

```bash
git clone <your_forked_repo_link>
cd internship-1
```

### 3. 🔧 Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

💡 **Tip:** If you encounter issues, consider using a virtual environment:  
[Python venv guide](https://docs.python.org/3/library/venv.html#module-venv)

### 4. ⚙️ Environment Configuration

Rename the sample config file:

```bash
mv config.env .env
```

Then, open `.env` and update the configuration according to your environment (e.g., database URL, secret keys).

---

## 🚀 Run the API

Use Uvicorn to start the development server:

```bash
uvicorn main:app --reload
```

Now visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the Swagger UI!

---

## 📌 Project Structure

```
internship-1/
├── main.py             # FastAPI app and endpoints
├── models.py           # SQLAlchemy models
├── schemas.py          # Pydantic schemas
├── database.py         # Database setup
├── config.env          # Sample configuration file
├── .env                # Actual environment variables (ignored in git)
└── README.md           # Project documentation
```

---

## 🌟 Star This Project

If you found this useful or inspiring, give it a ⭐ on GitHub — it helps others discover it too!

---

## ✨ Built with love using FastAPI