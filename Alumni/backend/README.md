# Alumni Backend - PostgreSQL Database

A robust FastAPI backend with PostgreSQL database that can be hosted on various platforms without errors.

## Features

- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ User authentication and authorization
- ✅ Profile management with file upload support
- ✅ Events and job postings
- ✅ Alumni feedback system
- ✅ Admin dashboard functionality
- ✅ Cross-platform deployment support

## Database Models

- **User**: Alumni profiles with authentication
- **Event**: College events and notices
- **Job**: Job postings and internships
- **Feedback**: Alumni feedback with ratings

## Supported Platforms

This backend can be deployed on:
- **Railway** (Recommended - easiest PostgreSQL setup)
- **Render** (Free tier available)
- **Heroku** (Requires paid PostgreSQL add-on)
- **Supabase** (Free PostgreSQL hosting)
- **DigitalOcean App Platform**
- **AWS Elastic Beanstalk**

## Local Development

1. Install PostgreSQL locally or use Docker:
   ```bash
   docker run -d --name alumni-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=alumni_db -p 5432:5432 postgres:15
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. Run the application:
   ```bash
   python app.py
   ```

The backend will be available at `http://localhost:8000`

## Deployment Instructions

### Railway (Recommended)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Connect your repository
4. Railway will automatically detect PostgreSQL
5. Set environment variable: `DATABASE_URL=${{RAILWAY_POSTGRESQL_URL}}`
6. Deploy!

### Render

1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Add PostgreSQL database
5. Set environment variable: `DATABASE_URL=${{DATABASE_URL}}`
6. Deploy!

### Supabase

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Get your PostgreSQL connection string
4. Set environment variable: `DATABASE_URL=postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres`
5. Deploy your backend to any platform with this DATABASE_URL

### Heroku

1. Install Heroku CLI
2. Create app: `heroku create alumni-backend`
3. Add PostgreSQL: `heroku addons:create heroku-postgresql`
4. Set environment: `heroku config:set DATABASE_URL=$(heroku config:get DATABASE_URL)`
5. Deploy: `git push heroku main`

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (required)
- `CORS_ORIGINS`: Comma-separated list of allowed origins (default: `*`)
- `JWT_SECRET`: Secret key for JWT tokens (required for production)

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/reset-password` - Password reset

### Profile
- `GET /api/me` - Get current user profile
- `PUT /api/me/profile` - Update user profile

### Public Data
- `GET /api/alumni` - Get alumni directory
- `GET /api/events` - Get events
- `GET /api/jobs` - Get jobs
- `POST /api/feedback` - Submit feedback

### Admin
- `GET /api/admin/pending` - Get pending registrations
- `POST /api/admin/pending/{id}/approve` - Approve alumni
- `POST /api/admin/pending/{id}/reject` - Reject alumni
- `GET /api/admin/alumni` - Get all alumni
- `GET /api/admin/feedback` - Get feedback
- `POST /api/admin/events` - Create event
- `POST /api/admin/jobs` - Create job

## Default Admin User

Email: `admin@college.edu`
Password: `admin123`

## Database Schema

The database automatically initializes with the following tables:
- `users` - User accounts and profiles
- `events` - College events
- `jobs` - Job postings
- `feedback` - Alumni feedback

## Troubleshooting

### Database Connection Issues
- Ensure DATABASE_URL is set correctly
- Check if PostgreSQL is running
- Verify network connectivity

### CORS Errors
- Add your frontend URL to CORS_ORIGINS
- Use `*` for development only

### Migration Issues
- The database auto-initializes on first run
- Tables are created automatically using SQLAlchemy

## Support

For issues or questions, check the database models in `database.py` and the main application in `app.py`.
