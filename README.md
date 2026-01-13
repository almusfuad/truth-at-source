# Truth at Source - Compliance Evidence Management System

A Django REST API for managing compliance evidence and fulfilling document requests between factories and buyers.

## Prerequisites

- Python 3.12+
- pip (Python package manager)
- Virtual environment (recommended)

## Project Setup

### 1. Clone the Repository
```bash
cd truth-at-source
```

### 2. Create Virtual Environment
```bash
python3 -m venv env
```

### 3. Activate Virtual Environment

**Linux/macOS:**
```bash
source env/bin/activate
```

**Windows:**
```bash
env\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install manually:
```bash
pip install django djangorestframework PyJWT
pip freeze > requirements.txt
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Start Development Server
```bash
python manage.py runserver
```

Server will run at: `http://localhost:8000`

---

## API Endpoints

### Authentication

#### Login
```
POST /api/auth/login/
```
**Body:**
```json
{
  "userId": "U1",
  "role": "factory",
  "factoryId": "F001"
}
```
**Response:**
```json
{
  "token": "jwt_token_here"
}
```

---

### Evidence Management (Factory)

#### Create Evidence
```
POST /api/evidence/
```
**Permissions:** `IsAuthenticated`, `IsFactory`

**Body:**
```json
{
  "name": "ISO_9001_Certificate",
  "docType": "ISO",
  "expiry": "2027-01-13",
  "notes": "Factory A certification"
}
```
**Response:**
```json
{
  "evidenceId": 1,
  "versionId": "v1"
}
```

#### Create Evidence Version
```
POST /api/evidence/{evidence_id}/versions/
```
**Permissions:** `IsAuthenticated`, `IsFactory`

**Body:**
```json
{
  "notes": "Updated with latest standards",
  "expiry": "2027-06-15"
}
```
**Response:**
```json
{
  "versionId": "v2"
}
```

---

### Request Management

#### Create Request (Buyer)
```
POST /api/requests/
```
**Permissions:** `IsAuthenticated`, `IsBuyer`

**Body:**
```json
{
  "factoryId": "F001",
  "title": "Compliance Documentation Request",
  "items": [
    {
      "docType": "ISO"
    },
    {
      "docType": "OSHA_Certificate"
    }
  ]
}
```
**Response:**
```json
{
  "requestId": 1
}
```

#### List Factory Requests
```
GET /api/requests/factory/
```
**Permissions:** `IsAuthenticated`, `IsFactory`

**Response:**
```json
[
  {
    "id": 1,
    "factoryId": "F001",
    "title": "Compliance Documentation Request",
    "items": [
      {
        "id": 1,
        "docType": "ISO",
        "fulfilled": false,
        "fulfilledEvidence": null,
        "fulfilledVersion": null
      }
    ]
  }
]
```

#### Fulfill Request Item
```
POST /api/requests/{request_id}/items/{item_id}/fulfill/
```
**Permissions:** `IsAuthenticated`, `IsFactory`

**Body:**
```json
{
  "evidenceId": 1,
  "versionId": 2
}
```
**Response:**
```json
{
  "status": "Fulfilled"
}
```

---

### Audit Logs

#### List Audit Logs
```
GET /api/audit/logs/
```
**Response:**
```json
[
  {
    "id": 1,
    "actor": "FAC_1",
    "action": "CREATE_EVIDENCE",
    "object_type": "Evidence",
    "object_id": 1,
    "metadata": {
      "factoryId": "F001",
      "docType": "ISO"
    },
    "timestamp": "2026-01-13T10:30:00Z"
  }
]
```

---

## Authentication

All endpoints (except login) require JWT Bearer token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

**Example request with authentication:**
```bash
curl -X GET http://localhost:8000/api/requests/factory/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

---

## Project Structure

```
truth-at-source/
├── app/
│   ├── models/
│   │   ├── user.py          # User model
│   │   ├── evidence.py      # Evidence & Version models
│   │   └── request.py       # Request & RequestItem models
│   ├── views/
│   │   ├── auth.py          # Authentication views
│   │   ├── evidence.py      # Evidence management views
│   │   ├── requests.py      # Request management views
│   │   └── audit.py         # Audit log views
│   ├── services/
│   │   ├── authentication.py # JWT authentication
│   │   ├── audit.py         # Audit logging service
│   │   └── evidence.py      # Evidence business logic
│   ├── permissions.py       # Custom permission classes
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL patterns
│   └── migrations/          # Database migrations
├── config/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL config
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── manage.py                # Django management script
├── db.sqlite3               # SQLite database
└── requirements.txt         # Python dependencies
```

---

## Database Models

### User
- `user_id` - Unique user identifier
- `role` - 'buyer' or 'factory'
- `factory_id` - Factory ID (for factory users)
- `is_authenticated` - Property always returns True

### Evidence
- `name` - Evidence name
- `doc_type` - Document type
- `expiry` - Expiration date
- `notes` - Additional notes
- `factory_id` - Factory that owns this evidence
- `created_by` - User who created it
- **Unique constraint:** (name, factory_id)

### Version
- `evidence` - FK to Evidence
- `version_id` - Version identifier (v1, v2, v3...)
- `notes` - Version notes
- `expiry` - Version expiration date

### Request
- `factory_id` - Factory being requested from
- `title` - Request title
- `created_by` - Buyer who created the request

### RequestItem
- `request` - FK to Request
- `doc_type` - Document type requested
- `fulfilled_evidence` - Evidence used to fulfill (if fulfilled)
- `fulfilled_version` - Version used to fulfill (if fulfilled)

---

## Troubleshooting

### Virtual Environment Not Activating
Ensure you're using the correct activation command for your OS (Linux/macOS vs Windows).

### Port 8000 Already in Use
```bash
python manage.py runserver 8001
```

### Database Migration Issues
```bash
python manage.py makemigrations
python manage.py migrate
```

### Authentication Errors
- Verify JWT token is valid and not expired
- Check Authorization header format: `Bearer <token>`
- Ensure user has correct role (factory/buyer)

---

## Development Tips

- Use `python manage.py shell` for interactive debugging
- Check `db.sqlite3` with tools like SQLite Browser
- Enable Django debug toolbar for development: `pip install django-debug-toolbar`
- Use Postman or Insomnia for API testing

---

## API Testing with cURL

```bash
### Login
curl --location 'http://localhost:8000/api/auth/login/' \
--header 'Content-Type: application/json' \
--data '{
    "userId": "U1",
    "role": "factory",
    "factoryId": "F001"
}'

### Create Evidence
curl --location 'http://localhost:8000/api/evidence/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
  "name": "ISO_9001_Certificate",
  "docType": "ISO",
  "expiry": "2027-01-13",
  "notes": "Factory A certification"
}'

### Update the evidence version
curl --location 'http://localhost:8000/api/evidence/3/versions/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
  "notes": "Updated documentation with latest compliance standards",
  "expiry": "2027-01-13"
}'



### Request by buyers for evidence
curl --location 'http://localhost:8000/api/requests/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
  "factoryId": "F001",
  "title": "Compliance Documentation Request",
  "items": [
    {
      "docType": "ISO"
    },
    {
      "docType": "Factory Safety Certificate"
    }
  ]
}'


### Request List
curl --location 'http://localhost:8000/api/requests/factory/' \
--header 'Authorization: Bearer <token>'



### Fulfill request item
curl --location 'http://localhost:8000/api/requests/1/items/1/fulfill/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data '{
  "evidenceId": 1,
  "versionId": 2
}'


### Audit logs
curl --location 'http://localhost:8000/api/audit/logs/' \
--header 'Authorization: Bearer <token>'
```



---

## License

Proprietary - SentryLinkComply