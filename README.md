# TeamProjectHub Backend

## 🚀 Proje Açıklaması
TeamProjectHub, ekipler için proje yönetimini kolaylaştıran bir backend API'sidir. Kullanıcılar projeler oluşturabilir, takımlara atayabilir, belirli kişilere görevler verebilir ve projelerin ilerleme durumlarını takip edebilirler.

## 📌 Özellikler
- 🔹 **Proje Yönetimi**: Yeni projeler oluşturma, düzenleme ve silme.
- 🔹 **Takım Yönetimi**: Kullanıcıları takımlara atama.
- 🔹 **Görev Atama**: Proje içindeki görevleri belirli kişilere atama.
- 🔹 **Son Tarih Takibi**: Projelerin teslim tarihlerini belirleme ve takip etme.
- 🔹 **Durum Güncelleme**: Proje ve görev durumlarını güncelleme.
- 🔹 **API Dokümantasyonu**: Swagger veya Postman ile test edilebilir RESTful API.

## 🛠️ Teknolojiler
- **Backend Framework**: FastAPI / Flask / Django (Seçiminize bağlı)
- **Veritabanı**: PostgreSQL / MySQL / SQLite
- **Kimlik Doğrulama**: JWT / OAuth2
- **Dokümantasyon**: Swagger / Postman
- **Deployment**: Docker / AWS / Heroku

## 📂 Kurulum

### 1️⃣ Projeyi Klonlayın
```bash
git clone https://github.com/kullaniciadi/TeamProjectHub-Backend.git
cd TeamProjectHub-Backend
```

### 2️⃣ Sanal Ortam Oluşturun ve Bağımlılıkları Yükleyin
```bash
python -m venv venv
source venv/bin/activate  # Windows için: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Veritabanını Ayarlayın
```bash
python manage.py migrate  # Django için
alembic upgrade head  # FastAPI için
```

### 4️⃣ Sunucuyu Başlatın
```bash
uvicorn main:app --reload  # FastAPI için
python manage.py runserver  # Django için
```

## 🔗 API Endpointleri
| Metod | Endpoint | Açıklama |
|--------|------------|-------------|
| GET | `/projects` | Tüm projeleri getir |
| POST | `/projects` | Yeni proje oluştur |
| GET | `/projects/{id}` | Belirli projeyi getir |
| PUT | `/projects/{id}` | Projeyi güncelle |
| DELETE | `/projects/{id}` | Projeyi sil |
| GET | `/teams` | Tüm takımları getir |
| POST | `/teams` | Yeni takım oluştur |

## 📌 Katkıda Bulunma
1. **Fork** yapın 📌
2. Yeni bir **branch** oluşturun (`feature/yeniozellik`)
3. Değişikliklerinizi yapın ve **commit** atın
4. **Pull request** gönderin 🎉

## 📄 Lisans
Bu proje MIT Lisansı ile lisanslanmıştır.

---
💡 **Destek olmak için projeyi yıldızlayabilirsiniz! ⭐**

