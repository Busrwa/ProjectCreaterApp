# 🚀 TeamProjectHub Backend

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github&logoColor=white)](https://github.com/Busrwa/ProjectCreaterApp)

---

## 🇹🇷 Türkçe

### 🔹 Proje Açıklaması

TeamProjectHub, ekipler için **proje yönetimini kolaylaştıran bir backend API**'sidir.  
Kullanıcılar projeler oluşturabilir, takımlara atayabilir, belirli kişilere görevler verebilir ve projelerin ilerleme durumlarını takip edebilirler.

### ⚙️ Teknik Detaylar

* **Backend Framework:** Django
* **Veritabanı:** SQLite (varsayılan)
* **Kimlik Doğrulama:** JWT
* **Dokümantasyon:** Swagger
* **Deployment:** Docker / Heroku
* RESTful API ile proje ve takım yönetimi işlemleri

### 💡 Kullanım Senaryoları

* Ekip projelerinin merkezi yönetimi
* Görev ve zaman takibi
* Proje ilerleme raporlaması

### 🛠️ Kurulum ve Kullanım

```bash
git clone https://github.com/Busrwa/ProjectCreaterApp.git
cd ProjectCreaterApp
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Veritabanını ayarlayın
python manage.py migrate

# Sunucuyu başlatın
python manage.py runserver
```

### 📌 Katkıda Bulunma

1. **Fork** yapın 📌
2. Yeni bir **branch** oluşturun (`feature/yeniozellik`)
3. Değişikliklerinizi yapın ve **commit** atın
4. **Pull request** gönderin 🎉

---

## 🇬🇧 English

### 🔹 Project Description

TeamProjectHub is a **backend API designed to simplify project management for teams**.  
Users can create projects, assign them to teams, allocate tasks to specific members, and track project progress.

### ⚙️ Technical Details

* **Backend Framework:** Django
* **Database:** SQLite (default)
* **Authentication:** JWT
* **Documentation:** Swagger
* **Deployment:** Docker / Heroku
* RESTful API for project and team management operations

### 💡 Use Cases

* Centralized management of team projects
* Task and deadline tracking
* Project progress reporting

### 🛠️ Installation & Usage

```bash
git clone https://github.com/Busrwa/ProjectCreaterApp.git
cd ProjectCreaterApp
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup the database
python manage.py migrate

# Start the server
python manage.py runserver
```

### 📌 Contributing

1. **Fork** the repository 📌
2. Create a new **branch** (`feature/new-feature`)
3. Make your changes and **commit** them
4. Submit a **pull request** 🎉

---

💡 **Support the project by giving it a star! ⭐**
