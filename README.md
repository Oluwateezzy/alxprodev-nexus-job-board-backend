# Job Board Platform - Backend API

A robust Django REST Framework backend for a job board platform featuring role-based access control, advanced search capabilities, and comprehensive API documentation.

## 🚀 Features

### Core Functionality
- **Job Posting Management**: Complete CRUD operations for job postings
- **Role-Based Authentication**: Support for Job Seekers, Employers, and Administrators
- **Company Profiles**: Comprehensive company information management
- **Application Tracking**: Job application submission and status management
- **Bookmarking System**: Save jobs for later viewing
- **Advanced Search**: Optimized job filtering by location, type, and criteria

### Authentication & Authorization
- JWT-based authentication
- Custom user model with email as username
- Role-based permissions (Seeker, Employer, Admin)
- Secure API endpoints

### Performance Optimization
- Database indexing for efficient queries
- Optimized search functionality
- PostgreSQL integration for scalability

### API Documentation
- Interactive Swagger/OpenAPI documentation
- Comprehensive endpoint documentation at `/api/docs/`

## 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| **Django REST Framework** | API development framework |
| **PostgreSQL** | Primary database |
| **JWT** | Authentication tokens |
| **Swagger/OpenAPI** | API documentation |
| **Python 3.8+** | Programming language |

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Oluwateezzy/alxprodev-nexus-job-board-backend.git
cd alxprodev-nexus-job-board-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Configuration

Create a PostgreSQL database and update your settings:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jobboard_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Environment Variables

Create a `.env` file in the project root:

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser
```bash
python manage.py createsuperuser
```

### 8. Start Development Server
```bash
python manage.py runserver
```

The API will be available at `https://alxprodev-nexus-job-board-backend.onrender.com/api/`
## 📖 API Documentation

### Interactive Documentation
Visit `https://alxprodev-nexus-job-board-backend.onrender.com/api/docs` for interactive Swagger documentation.

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "role": "SEEKER"  # or "EMPLOYER", "ADMIN"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### Get Profile
```http
GET /api/auth/profile/
Authorization: Bearer <your-jwt-token>
```

### Core API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/companies/` | GET, POST | List/Create companies | Yes (POST) |
| `/api/companies/{id}/` | GET, PUT, DELETE | Company details | Yes (PUT/DELETE) |
| `/api/jobs/` | GET, POST | List/Create job postings | Yes (POST) |
| `/api/jobs/{id}/` | GET, PUT, DELETE | Job posting details | Yes (PUT/DELETE) |
| `/api/applications/` | GET, POST | List/Create applications | Yes |
| `/api/applications/{id}/` | GET, PUT, DELETE | Application details | Yes |
| `/api/bookmarks/` | GET, POST | List/Create bookmarks | Yes |

### Job Search & Filtering

The job listings endpoint supports various query parameters for filtering:

```http
GET /api/jobs/?employment_type=FULL_TIME&location_type=REMOTE&city=Lagos&country=Nigeria
```

**Available Filters:**
- `employment_type`: FULL_TIME, PART_TIME, CONTRACT, TEMPORARY, INTERNSHIP, VOLUNTEER
- `location_type`: REMOTE, HYBRID, ON_SITE
- `city`: Filter by city name
- `country`: Filter by country
- `salary_range_min`: Minimum salary
- `salary_range_max`: Maximum salary
- `company`: Filter by company ID

## 🏗 Database Schema

### Key Models

#### User Model
- Custom user model using email as username
- Role-based user types (Seeker, Employer, Admin)
- Email verification support

#### Company Model
- Comprehensive company information
- Verification status
- Industry and size categorization

#### JobPosting Model
- Detailed job information
- Employment and location types
- Salary ranges and application deadlines
- View tracking

#### Application Model
- Job application management
- Status tracking (Applied, Reviewed, Interviewed, Rejected, Offered)
- Resume and cover letter links

## 🔒 Role-Based Access Control

### User Roles

1. **Job Seeker (SEEKER)**
   - Apply to job postings
   - Manage applications
   - Bookmark jobs
   - Update profile

2. **Employer (EMPLOYER)**
   - Create and manage companies
   - Post job listings
   - Review applications
   - Manage job status

3. **Administrator (ADMIN)**
   - Full system access
   - Manage all users and companies
   - System configuration
   - Data management

### Permission Examples

```python
# Only employers can create job postings
# Only job seekers can apply to jobs
# Only application owners can view their applications
```

### Manual Deployment

1. Set up production database
2. Configure environment variables
3. Collect static files: `python manage.py collectstatic`
4. Use a WSGI server like Gunicorn
5. Set up reverse proxy (Nginx recommended)

## 📊 Performance Optimization

### Database Indexes
The project includes optimized database indexes for:
- Job title and description search
- Location-based filtering
- Employment type filtering
- Salary range queries
- Job status filtering

### Query Optimization
- Select related for foreign key relationships
- Prefetch related for many-to-many relationships
- Efficient pagination
- Cached query results where appropriate

## 📝 API Response Examples

### Job Listing Response
```json
{
  "id": 1,
  "title": "Senior Django Developer",
  "company": {
    "id": 1,
    "name": "TechCorp",
    "logo_url": "https://example.com/logo.png"
  },
  "description": "We are looking for...",
  "employment_type": "FULL_TIME",
  "location_type": "REMOTE",
  "salary_range_min": 120000,
  "salary_range_max": 180000,
  "currency": "USD",
  "date_posted": "2025-08-10T10:30:00Z",
  "application_deadline": "2025-09-10T23:59:59Z",
  "status": "ACTIVE"
}
```

### Application Response
```json
{
  "id": 1,
  "job": {
    "id": 1,
    "title": "Senior Django Developer",
    "company": "TechCorp"
  },
  "status": "APPLIED",
  "submitted_at": "2025-08-10T10:30:00Z",
  "resume_url": "https://example.com/resume.pdf",
  "cover_letter_url": "https://example.com/cover.pdf"
}
```

## 📞 Support

For support, create an issue in the repository.

## 🙏 Acknowledgments

- Django REST Framework team
- PostgreSQL community
- Swagger/OpenAPI contributors
- All contributors to this project

---

**Built with ❤️ using Django REST Framework**
