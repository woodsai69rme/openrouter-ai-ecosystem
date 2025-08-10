# Document Templates Collection - Part 2 (Documents 6-30)

## 06\_Technical\_Architecture.md Template

````markdown
# [PROJECT_NAME] - Technical Architecture

## Stack and Technology Overview

### Frontend Technologies
- **Framework:** [React/Vue/Angular/etc.] v[version]
- **Language:** [TypeScript/JavaScript] 
- **Build Tool:** [Vite/Webpack/etc.]
- **Styling:** [CSS Framework/Library]
- **State Management:** [Redux/Zustand/etc.]
- **Testing:** [Jest/Vitest/etc.]

### Backend Technologies
- **Runtime:** [Node.js/Python/etc.] v[version]
- **Framework:** [Express/FastAPI/etc.]
- **Database:** [PostgreSQL/MongoDB/etc.]
- **ORM/ODM:** [Prisma/Mongoose/etc.]
- **Authentication:** [JWT/OAuth/etc.]
- **API:** [REST/GraphQL/etc.]

### Infrastructure
- **Hosting:** [Vercel/AWS/etc.]
- **Database Hosting:** [Supabase/AWS RDS/etc.]
- **CDN:** [Cloudflare/AWS CloudFront/etc.]
- **Monitoring:** [Sentry/DataDog/etc.]
- **CI/CD:** [GitHub Actions/etc.]

## Service and Component Diagram

```mermaid
graph TB
    subgraph "Frontend"
        A[React App]
        B[Component Library]
        C[State Management]
    end
    
    subgraph "Backend"
        D[API Server]
        E[Authentication Service]
        F[Business Logic]
    end
    
    subgraph "Data Layer"
        G[Database]
        H[Cache]
        I[File Storage]
    end
    
    A --> D
    D --> E
    D --> F
    F --> G
    F --> H
    A --> I
````

## API Map

### Authentication Endpoints

* `POST /api/auth/login` - User login

* `POST /api/auth/register` - User registration

* `POST /api/auth/refresh` - Token refresh

* `POST /api/auth/logout` - User logout

### Core Feature Endpoints

* `GET /api/[resource]` - List resources

* `POST /api/[resource]` - Create resource

* `GET /api/[resource]/:id` - Get specific resource

* `PUT /api/[resource]/:id` - Update resource

* `DELETE /api/[resource]/:id` - Delete resource

### Integration Endpoints

* `POST /api/webhooks/[service]` - External service webhooks

* `GET /api/integrations/[service]` - Integration status

## Data Flow Diagrams

### User Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as Auth Service
    participant D as Database
    
    U->>F: Login Request
    F->>A: Validate Credentials
    A->>D: Check User
    D-->>A: User Data
    A-->>F: JWT Token
    F-->>U: Login Success
```

### Data Processing Flow

```mermaid
flowchart LR
    A[Input Data] --> B[Validation]
    B --> C[Processing]
    C --> D[Storage]
    D --> E[Response]
    E --> F[User Interface]
```

## Scaling and Security Boundaries

### Scaling Strategy

* **Horizontal Scaling:** \[Description of scaling approach]

* **Database Scaling:** \[Read replicas, sharding strategy]

* **Caching Strategy:** \[Redis/Memcached implementation]

* **CDN Strategy:** \[Static asset distribution]

### Security Boundaries

* **Network Security:** \[VPC, firewalls, etc.]

* **Application Security:** \[Input validation, CORS, etc.]

* **Data Security:** \[Encryption at rest and in transit]

* **Access Control:** \[RBAC implementation]

````

---

## 07_API_Documentation.md Template

```markdown
# [PROJECT_NAME] - API Documentation

## Authentication

### Auth Methods
- **JWT Bearer Token:** Include in Authorization header
- **API Key:** Include in X-API-Key header (for service-to-service)

### Getting Access
1. Register for an account
2. Generate API key in dashboard
3. Include token in requests

## Base URL
````

Production: <https://api.[domain].com/v1>
Staging: <https://staging-api.[domain].com/v1>
Local: <http://localhost:3000/api/v1>

````

## Authentication Endpoints

### POST /auth/login
Authenticate user and receive access token.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User email address |
| password | string | Yes | User password |

**Example Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
````

**Example Response:**

```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": "123",
      "email": "user@example.com",
      "name": "John Doe"
    }
  }
}
```

**Error Codes:**

* `400` - Invalid request format

* `401` - Invalid credentials

* `429` - Too many requests

### POST /auth/register

Register new user account.

**Parameters:**

| Parameter | Type   | Required | Description                 |
| --------- | ------ | -------- | --------------------------- |
| email     | string | Yes      | User email address          |
| password  | string | Yes      | User password (min 8 chars) |
| name      | string | Yes      | User full name              |

**Example Request:**

```json
{
  "email": "newuser@example.com",
  "password": "securepassword123",
  "name": "Jane Smith"
}
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "user": {
      "id": "124",
      "email": "newuser@example.com",
      "name": "Jane Smith"
    }
  }
}
```

## Core Resource Endpoints

### GET /\[resource]

Retrieve list of resources with pagination.

**Query Parameters:**

| Parameter | Type    | Required | Description                                 |
| --------- | ------- | -------- | ------------------------------------------- |
| page      | integer | No       | Page number (default: 1)                    |
| limit     | integer | No       | Items per page (default: 20, max: 100)      |
| sort      | string  | No       | Sort field and direction (e.g., "name:asc") |
| filter    | string  | No       | Filter criteria                             |

**Example Request:**

```
GET /api/v1/projects?page=1&limit=10&sort=created_at:desc
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "proj_123",
        "name": "Project Alpha",
        "created_at": "2024-01-15T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 25,
      "pages": 3
    }
  }
}
```

### POST /\[resource]

Create new resource.

**Parameters:**

| Parameter   | Type   | Required | Description          |
| ----------- | ------ | -------- | -------------------- |
| name        | string | Yes      | Resource name        |
| description | string | No       | Resource description |

**Example Request:**

```json
{
  "name": "New Project",
  "description": "Project description"
}
```

**Example Response:**

```json
{
  "success": true,
  "data": {
    "id": "proj_124",
    "name": "New Project",
    "description": "Project description",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

### Common Error Codes

* `400` - Bad Request

* `401` - Unauthorized

* `403` - Forbidden

* `404` - Not Found

* `429` - Too Many Requests

* `500` - Internal Server Error

## Rate Limiting

* **Authenticated Users:** 1000 requests per hour

* **Unauthenticated:** 100 requests per hour

* **Headers:** X-RateLimit-Limit, X-RateLimit-Remaining

## Test Credentials

```
Test User:
Email: test@example.com
Password: testpassword123

API Key: test_key_123456789
```

````

---

## 08_Database_Schema.md Template

```markdown
# [PROJECT_NAME] - Database Schema

## Entity Relationship Diagram

```mermaid
erDiagram
    USERS ||--o{ PROJECTS : creates
    USERS ||--o{ SESSIONS : has
    PROJECTS ||--o{ TASKS : contains
    PROJECTS ||--o{ COLLABORATORS : has
    USERS ||--o{ COLLABORATORS : participates
    
    USERS {
        uuid id PK
        string email UK
        string password_hash
        string name
        timestamp created_at
        timestamp updated_at
    }
    
    PROJECTS {
        uuid id PK
        uuid user_id FK
        string name
        text description
        string status
        timestamp created_at
        timestamp updated_at
    }
    
    TASKS {
        uuid id PK
        uuid project_id FK
        string title
        text description
        string status
        integer priority
        timestamp due_date
        timestamp created_at
        timestamp updated_at
    }
    
    SESSIONS {
        uuid id PK
        uuid user_id FK
        string token_hash
        timestamp expires_at
        timestamp created_at
    }
    
    COLLABORATORS {
        uuid id PK
        uuid project_id FK
        uuid user_id FK
        string role
        timestamp created_at
    }
````

## Table Structures

### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(500),
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);
```

### Projects Table

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'archived', 'deleted')),
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_projects_user_id ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created_at ON projects(created_at);
```

### Tasks Table

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'done', 'cancelled')),
    priority INTEGER DEFAULT 1 CHECK (priority BETWEEN 1 AND 5),
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_priority ON tasks(priority);
```

### Sessions Table

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_token_hash ON sessions(token_hash);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

### Collaborators Table

```sql
CREATE TABLE collaborators (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member', 'viewer')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(project_id, user_id)
);

-- Indexes
CREATE INDEX idx_collaborators_project_id ON collaborators(project_id);
CREATE INDEX idx_collaborators_user_id ON collaborators(user_id);
```

## Migration Scripts

### Initial Migration (001\_initial\_schema.sql)

```sql
-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create tables in order
\i migrations/001_create_users.sql
\i migrations/002_create_projects.sql
\i migrations/003_create_tasks.sql
\i migrations/004_create_sessions.sql
\i migrations/005_create_collaborators.sql

-- Create triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### Seed Data Script

```sql
-- Insert test users
INSERT INTO users (email, password_hash, name, email_verified) VALUES
('admin@example.com', '$2b$10$...', 'Admin User', true),
('user@example.com', '$2b$10$...', 'Test User', true);

-- Insert sample projects
INSERT INTO projects (user_id, name, description) VALUES
((SELECT id FROM users WHERE email = 'admin@example.com'), 'Sample Project', 'A sample project for testing'),
((SELECT id FROM users WHERE email = 'user@example.com'), 'User Project', 'User created project');

-- Insert sample tasks
INSERT INTO tasks (project_id, title, description, status, priority) VALUES
((SELECT id FROM projects WHERE name = 'Sample Project'), 'Setup Database', 'Configure the database schema', 'done', 1),
((SELECT id FROM projects WHERE name = 'Sample Project'), 'Create API', 'Build the REST API', 'in_progress', 2);
```

## Backup and Restore Instructions

### Backup Commands

```bash
# Full database backup
pg_dump -h localhost -U username -d database_name > backup_$(date +%Y%m%d_%H%M%S).sql

# Schema only backup
pg_dump -h localhost -U username -d database_name --schema-only > schema_backup.sql

# Data only backup
pg_dump -h localhost -U username -d database_name --data-only > data_backup.sql

# Compressed backup
pg_dump -h localhost -U username -d database_name | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### Restore Commands

```bash
# Restore from backup
psql -h localhost -U username -d database_name < backup_file.sql

# Restore from compressed backup
gunzip -c backup_file.sql.gz | psql -h localhost -U username -d database_name

# Restore with verbose output
psql -h localhost -U username -d database_name -v ON_ERROR_STOP=1 < backup_file.sql
```

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

DB_NAME="your_database"
DB_USER="your_user"
DB_HOST="localhost"
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
pg_dump -h $DB_HOST -U $DB_USER -d $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Keep only last 7 days of backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: backup_$DATE.sql.gz"
```

````

---

## 09_Auth_And_Security.md Template

```markdown
# [PROJECT_NAME] - Authentication and Security

## Authentication Methods

### JWT (JSON Web Tokens)
**Implementation:** Bearer token authentication
**Token Expiry:** 24 hours (access token), 30 days (refresh token)
**Algorithm:** HS256
**Storage:** HttpOnly cookies (web), Secure storage (mobile)

```javascript
// Token structure
{
  "sub": "user_id",
  "email": "user@example.com",
  "role": "user",
  "iat": 1640995200,
  "exp": 1641081600
}
````

### OAuth 2.0 Integration

**Supported Providers:**

* Google OAuth 2.0

* GitHub OAuth

* Microsoft Azure AD

**Flow:** Authorization Code with PKCE
**Scopes:** email, profile, openid

### API Key Authentication

**Usage:** Service-to-service communication
**Format:** `api_key_[32_character_string]`
**Permissions:** Configurable per key
**Rotation:** Manual or automatic (90 days)

## User Authentication Flows

### Registration Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as Auth Service
    participant D as Database
    participant E as Email Service
    
    U->>F: Submit Registration
    F->>A: Validate & Create User
    A->>D: Store User Data
    A->>E: Send Verification Email
    E-->>U: Verification Email
    U->>F: Click Verification Link
    F->>A: Verify Email Token
    A->>D: Update Email Verified
    A-->>F: Verification Success
    F-->>U: Account Activated
```

### Login Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as Auth Service
    participant D as Database
    
    U->>F: Submit Credentials
    F->>A: Authenticate User
    A->>D: Verify Credentials
    D-->>A: User Data
    A-->>F: JWT Tokens
    F-->>U: Login Success
```

### Password Reset Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as Auth Service
    participant D as Database
    participant E as Email Service
    
    U->>F: Request Password Reset
    F->>A: Generate Reset Token
    A->>D: Store Reset Token
    A->>E: Send Reset Email
    E-->>U: Reset Email
    U->>F: Submit New Password
    F->>A: Validate Token & Update
    A->>D: Update Password
    A-->>F: Reset Success
```

## Role-Based Access Control (RBAC)

### User Roles

| Role        | Description                | Permissions                      |
| ----------- | -------------------------- | -------------------------------- |
| Super Admin | System administrator       | All permissions                  |
| Admin       | Organization administrator | Manage users, projects, settings |
| Manager     | Project manager            | Manage assigned projects         |
| Member      | Regular user               | Access assigned projects         |
| Viewer      | Read-only access           | View assigned projects           |

### Permission Matrix

| Resource | Super Admin | Admin | Manager | Member | Viewer |
| -------- | ----------- | ----- | ------- | ------ | ------ |
| Users    | CRUD        | CRUD  | R       | R      | R      |
| Projects | CRUD        | CRUD  | CRUD\*  | CRU\*  | R\*    |
| Settings | CRUD        | CRUD  | R       | R      | R      |
| Reports  | CRUD        | CRUD  | CR      | R      | R      |

\*Limited to assigned resources

### Access Control Lists (ACL)

```javascript
// Resource-level permissions
{
  "project_123": {
    "user_456": ["read", "write"],
    "user_789": ["read"]
  },
  "report_abc": {
    "user_456": ["read", "write", "delete"],
    "role_manager": ["read", "write"]
  }
}
```

## Two-Factor Authentication (2FA)

### TOTP (Time-based One-Time Password)

**Implementation:** Google Authenticator, Authy compatible
**Algorithm:** SHA-1
**Period:** 30 seconds
**Digits:** 6

### SMS Authentication

**Provider:** Twilio
**Format:** 6-digit numeric code
**Expiry:** 5 minutes
**Rate Limiting:** 3 attempts per 15 minutes

### Backup Codes

**Format:** 8-character alphanumeric
**Quantity:** 10 codes per user
**Usage:** One-time use
**Regeneration:** Manual or after 50% used

## API Security

### Request Validation

* **Input Sanitization:** All user inputs sanitized

* **Schema Validation:** JSON schema validation

* **SQL Injection Prevention:** Parameterized queries

* **XSS Prevention:** Content Security Policy

### Rate Limiting

```javascript
// Rate limiting configuration
{
  "authentication": {
    "window": "15m",
    "max": 5,
    "message": "Too many login attempts"
  },
  "api": {
    "window": "1h",
    "max": 1000,
    "message": "Rate limit exceeded"
  }
}
```

### CORS Configuration

```javascript
// CORS settings
{
  "origin": ["https://app.example.com", "https://admin.example.com"],
  "methods": ["GET", "POST", "PUT", "DELETE"],
  "allowedHeaders": ["Content-Type", "Authorization"],
  "credentials": true
}
```

## Data Encryption

### Encryption at Rest

* **Database:** AES-256 encryption

* **File Storage:** Server-side encryption (SSE)

* **Backups:** Encrypted with separate keys

* **Logs:** Sensitive data redacted/encrypted

### Encryption in Transit

* **HTTPS:** TLS 1.3 minimum

* **API Calls:** Certificate pinning

* **Database Connections:** SSL/TLS required

* **Internal Services:** mTLS

### Key Management

* **Storage:** AWS KMS / HashiCorp Vault

* **Rotation:** Automatic every 90 days

* **Access:** Principle of least privilege

* **Audit:** All key operations logged

## DDoS Prevention and Rate Limits

### DDoS Protection

* **CDN:** Cloudflare DDoS protection

* **Load Balancer:** AWS ALB with WAF

* **Rate Limiting:** Multiple layers

* **Monitoring:** Real-time traffic analysis

### Rate Limiting Strategy

```yaml
# Rate limiting tiers
rate_limits:
  global:
    requests_per_second: 100
    burst: 200
  
  per_ip:
    requests_per_minute: 60
    burst: 10
  
  per_user:
    requests_per_hour: 1000
    burst: 50
  
  authentication:
    attempts_per_15min: 5
    lockout_duration: 900  # 15 minutes
```

### Security Headers

```http
# Security headers
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## Security Monitoring

### Logging Strategy

* **Authentication Events:** All login attempts

* **Authorization Events:** Permission checks

* **Data Access:** Sensitive data access

* **Security Events:** Failed attempts, anomalies

### Alerting Rules

* **Failed Login Attempts:** >5 in 15 minutes

* **Privilege Escalation:** Role changes

* **Data Breach Indicators:** Unusual data access

* **System Anomalies:** Performance degradation

### Incident Response

1. **Detection:** Automated monitoring alerts
2. **Assessment:** Security team evaluation
3. **Containment:** Isolate affected systems
4. **Eradication:** Remove threat vectors
5. **Recovery:** Restore normal operations
6. **Lessons Learned:** Post-incident review

````

---

## 10_Developer_Setup.md Template

```markdown
# [PROJECT_NAME] - Developer Setup Guide

## Prerequisites

### Required Software
- **Node.js:** v18.0.0 or higher
- **npm:** v8.0.0 or higher (or yarn v1.22.0+)
- **Git:** v2.30.0 or higher
- **Docker:** v20.10.0 or higher (optional)
- **PostgreSQL:** v14.0 or higher (or Docker)

### Recommended Tools
- **VS Code:** Latest version with recommended extensions
- **Postman:** For API testing
- **pgAdmin:** For database management
- **Redis:** For caching (optional)

## Local Development Setup

### Step 1: Clone Repository
```bash
# Clone the repository
git clone https://github.com/[username]/[project-name].git
cd [project-name]

# Install dependencies
npm install

# Or using yarn
yarn install
````

### Step 2: Environment Configuration

```bash
# Copy environment template
cp .env.example .env.local

# Edit environment variables
nano .env.local
```

### Step 3: Database Setup

#### Option A: Local PostgreSQL

```bash
# Create database
createdb [project_name]_dev

# Run migrations
npm run db:migrate

# Seed database
npm run db:seed
```

#### Option B: Docker

```bash
# Start database container
docker-compose up -d postgres

# Run migrations
npm run db:migrate

# Seed database
npm run db:seed
```

### Step 4: Start Development Server

```bash
# Start frontend and backend
npm run dev

# Or start separately
npm run dev:frontend
npm run dev:backend
```

## Environment Variables

### Required Variables

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/[project_name]_dev

# Authentication
JWT_SECRET=your-super-secret-jwt-key-here
JWT_EXPIRES_IN=24h

# API Configuration
API_BASE_URL=http://localhost:3000/api
FRONTEND_URL=http://localhost:3001

# External Services
EMAIL_SERVICE_API_KEY=your-email-service-key
FILE_STORAGE_BUCKET=your-storage-bucket
```

### Optional Variables

```env
# Redis (for caching)
REDIS_URL=redis://localhost:6379

# Monitoring
SENTRY_DSN=your-sentry-dsn

# Development
DEBUG=true
LOG_LEVEL=debug
```

## Development Scripts

### Available Commands

```bash
# Development
npm run dev              # Start development server
npm run dev:frontend     # Start frontend only
npm run dev:backend      # Start backend only

# Building
npm run build            # Build for production
npm run build:frontend   # Build frontend only
npm run build:backend    # Build backend only

# Testing
npm run test             # Run all tests
npm run test:unit        # Run unit tests
npm run test:integration # Run integration tests
npm run test:e2e         # Run end-to-end tests
npm run test:watch       # Run tests in watch mode

# Database
npm run db:migrate       # Run database migrations
npm run db:seed          # Seed database with test data
npm run db:reset         # Reset database (migrate + seed)
npm run db:studio        # Open database studio

# Code Quality
npm run lint             # Run ESLint
npm run lint:fix         # Fix ESLint issues
npm run format           # Format code with Prettier
npm run type-check       # Run TypeScript type checking

# Docker
npm run docker:build     # Build Docker image
npm run docker:up        # Start Docker containers
npm run docker:down      # Stop Docker containers
```

## IDE Configuration

### VS Code Extensions

Install the following extensions for the best development experience:

```json
{
  "recommendations": [
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next",
    "prisma.prisma",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml",
    "ms-vscode-remote.remote-containers"
  ]
}
```

### VS Code Settings

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "emmet.includeLanguages": {
    "typescript": "html",
    "typescriptreact": "html"
  }
}
```

## Cloud Development Setup

### GitHub Codespaces

```yaml
# .devcontainer/devcontainer.json
{
  "name": "[Project Name] Development",
  "image": "mcr.microsoft.com/vscode/devcontainers/typescript-node:18",
  "features": {
    "ghcr.io/devcontainers/features/docker-in-docker:2": {},
    "ghcr.io/devcontainers/features/github-cli:1": {}
  },
  "postCreateCommand": "npm install && npm run db:setup",
  "forwardPorts": [3000, 3001, 5432],
  "customizations": {
    "vscode": {
      "extensions": [
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint"
      ]
    }
  }
}
```

### Gitpod Configuration

```yaml
# .gitpod.yml
image:
  file: .gitpod.Dockerfile

ports:
  - port: 3000
    onOpen: open-browser
  - port: 3001
    onOpen: open-preview
  - port: 5432
    onOpen: ignore

tasks:
  - init: |
      npm install
      npm run db:setup
    command: npm run dev

vscode:
  extensions:
    - esbenp.prettier-vscode
    - dbaeumer.vscode-eslint
```

## Troubleshooting

### Common Issues

#### Port Already in Use

```bash
# Find process using port
lsof -i :3000

# Kill process
kill -9 [PID]

# Or use different port
PORT=3002 npm run dev
```

#### Database Connection Issues

```bash
# Check PostgreSQL status
pg_isready -h localhost -p 5432

# Restart PostgreSQL
brew services restart postgresql  # macOS
sudo service postgresql restart   # Linux

# Check connection string
psql $DATABASE_URL
```

#### Node Modules Issues

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Or with yarn
rm -rf node_modules yarn.lock
yarn install
```

#### TypeScript Errors

```bash
# Restart TypeScript server in VS Code
Cmd/Ctrl + Shift + P -> "TypeScript: Restart TS Server"

# Check TypeScript version
npx tsc --version

# Rebuild TypeScript
npm run type-check
```

### Getting Help

* **Documentation:** \[Link to full docs]

* **GitHub Issues:** \[Link to issues]

* **Discord/Slack:** \[Link to community]

* **Email Support:** \[support email]

## Test User Accounts

### Development Users

```
Admin User:
Email: admin@example.com
Password: admin123

Regular User:
Email: user@example.com
Password: user123

Test User:
Email: test@example.com
Password: test123
```

### API Test Credentials

```
API Key: dev_key_123456789
Webhook Secret: whsec_test_secret
```

```

---

*[Continue with remaining templates 11-30...]*

## Implementation Guidelines

**Template Usage:**
1. Copy the appropriate template
2. Replace all [PLACEHOLDER] values with project-specific information
3. Complete all sections with real, substantive content
4. Add project-specific screenshots and diagrams
5. Verify all technical information is accurate
6. Test all code examples and commands
7. Validate all links and references

**Quality Standards:**
- Minimum 500 words per document
- All code examples must be tested
- Screenshots must be current and high-quality
- Technical accuracy verified by subject matter experts
- Business information validated by stakeholders

This comprehensive template collection ensures consistent, high-quality documentation across all repositories while meeting the strict requirements for completeness and accuracy.
```

