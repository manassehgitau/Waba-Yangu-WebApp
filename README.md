# Waba Yangu WebApp

**Waba Yangu** (meaning "My Stove" in Swahili) is a comprehensive IoT-enabled energy monitoring system designed to help users track, manage, and optimize their energy consumption. The platform combines hardware (ESP8266-based firmware), a Django REST API backend, and a React-based frontend to provide real-time monitoring and control of energy usage, with integrated M-Pesa payment functionality for utility billing.

## 🌟 Features

- **Real-time Energy Monitoring**: Track your energy consumption in real-time through IoT devices
- **User Authentication & Management**: Secure user registration, login, and profile management with JWT authentication
- **Subscription Plans**: Free, Basic, and Premium subscription tiers
- **M-Pesa Integration**: Seamless payment integration using Safaricom's M-Pesa STK Push
- **Cloud Storage**: Profile picture management via Cloudinary
- **RESTful API**: Well-structured Django REST Framework backend
- **Modern Frontend**: React-based single-page application with Vite
- **IoT Firmware**: ESP8266-based firmware for energy monitoring devices

## 🏗️ Project Structure

```
Waba-Yangu-WebApp/
├── waba-backend/          # Django REST API Backend
│   ├── accounts/          # User authentication and management
│   ├── wabaYangu/         # Main Django project configuration
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Docker configuration for backend
├── waba-frontend/         # React Frontend Application
│   ├── src/               # React source files
│   ├── public/            # Static assets
│   └── package.json       # Node.js dependencies
└── Waba-Yangu-Firmware/   # ESP8266 IoT Device Firmware
    ├── src/               # C++ source code
    ├── platformio.ini     # PlatformIO configuration
    └── lib/               # Libraries
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2.1
- **API**: Django REST Framework 3.16.0
- **Authentication**: JWT (djangorestframework-simplejwt 5.5.0)
- **Database**: PostgreSQL (psycopg2 2.9.10)
- **Cloud Storage**: Cloudinary 1.44.0
- **Payment Integration**: Africa's Talking 1.2.9
- **Time Series Data**: InfluxDB 5.3.2
- **API Documentation**: drf-yasg 1.21.10
- **Messaging**: MQTT (paho-mqtt 2.1.0)

### Frontend
- **Framework**: React 19.1.0
- **Build Tool**: Vite 6.3.5
- **Language**: JavaScript (ES6+)
- **Linting**: ESLint 9.25.0

### Firmware
- **Platform**: ESP8266 (ESP-12E module)
- **Framework**: Arduino
- **IDE**: PlatformIO
- **Libraries**: ArduinoJson 7.0.3, MpesaSTK

## 📋 Prerequisites

### Backend Requirements
- Python 3.11+
- PostgreSQL 12+
- pip (Python package manager)

### Frontend Requirements
- Node.js 18+
- npm or yarn

### Firmware Requirements
- PlatformIO IDE or CLI
- ESP8266 development board

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/manassehgitau/Waba-Yangu-WebApp.git
cd Waba-Yangu-WebApp
```

### 2. Backend Setup

```bash
cd waba-backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file with your configuration
cat > .env << EOF
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/wabayangu
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRET=your-cloudinary-api-secret
DEFAULT_FROM_EMAIL=noreply@wabayangu.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
FRONTEND_PASSWORD_RESET_CONFIRM_URL=http://localhost:5173/auth/reset-password-confirm/
API_BASE_URL=http://localhost:8000
EOF

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd waba-frontend

# Install dependencies
npm install

# Create environment configuration
cat > .env << EOF
VITE_API_URL=http://localhost:8000
EOF

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Firmware Setup

```bash
cd Waba-Yangu-Firmware

# Install PlatformIO if you haven't already
# Using pip:
pip install platformio

# Update WiFi credentials and M-Pesa keys in src/main.cpp
# Then build and upload to your ESP8266 device
pio run --target upload

# Monitor serial output
pio device monitor
```

## 🐳 Docker Deployment (Backend)

```bash
cd waba-backend

# Build the Docker image
docker build -t waba-backend .

# Run the container
docker run -p 8000:8000 -e DATABASE_URL=your-db-url waba-backend
```

## 📚 API Documentation

Once the backend is running, you can access the interactive API documentation:

- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

### Key API Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT tokens)
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update user profile
- `DELETE /api/users/me/` - Delete user account
- `POST /api/auth/change-password/` - Change password
- `POST /api/auth/forgot-password/` - Request password reset
- `POST /api/auth/reset-password/` - Reset password with token

## 🔧 Development

### Backend Development

```bash
cd waba-backend

# Run migrations after model changes
python manage.py makemigrations
python manage.py migrate

# Create a new Django app
python manage.py startapp app_name

# Run tests (when available)
python manage.py test

# Collect static files for production
python manage.py collectstatic
```

### Frontend Development

```bash
cd waba-frontend

# Lint code
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

### Firmware Development

```bash
cd Waba-Yangu-Firmware

# Build firmware
pio run

# Upload to device
pio run --target upload

# Clean build files
pio run --target clean
```

## 🔐 Environment Variables

### Backend (.env)
```
SECRET_KEY=your-django-secret-key
DEBUG=True/False
DATABASE_URL=postgresql://user:password@host:port/database
CLOUDINARY_CLOUD_NAME=your-cloudinary-name
CLOUDINARY_API_KEY=your-cloudinary-key
CLOUDINARY_API_SECRET=your-cloudinary-secret
DEFAULT_FROM_EMAIL=your-email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
FRONTEND_PASSWORD_RESET_CONFIRM_URL=frontend-url
API_BASE_URL=backend-url
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## 📱 User Subscription Types

The platform supports three subscription tiers:

1. **Free**: Basic monitoring features
2. **Basic**: Enhanced monitoring and analytics
3. **Premium**: Full feature access with advanced analytics and priority support

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- **Backend**: Follow PEP 8 style guidelines for Python
- **Frontend**: Use ESLint configuration provided in the project
- **Firmware**: Follow Arduino/C++ best practices

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Manasseh Gitau** - [manassehgitau](https://github.com/manassehgitau)

## 🙏 Acknowledgments

- Safaricom M-Pesa API for payment integration
- Cloudinary for media storage
- Django and React communities for excellent documentation
- PlatformIO for IoT development tools

## 📞 Support

For support, email support@wabayangu.com or open an issue in the GitHub repository.

## 🗺️ Roadmap

- [ ] Add real-time energy consumption graphs
- [ ] Implement device management dashboard
- [ ] Add push notifications for alerts
- [ ] Expand payment options beyond M-Pesa
- [ ] Add mobile applications (iOS/Android)
- [ ] Implement advanced analytics and reporting
- [ ] Add multi-language support

---

**Made with ❤️ in Kenya**
