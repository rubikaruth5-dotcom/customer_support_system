# AI-Powered Customer Support Ticket Management System

## Project Overview

This project is a backend application developed using Django and Django REST Framework to manage customer support tickets.

It allows customers to create and view their own tickets. Support agents and administrators can manage tickets, update their status, and view ticket information. The system also includes rule-based prediction of ticket categories and priorities.

## Technologies Used

- Python
- Django
- Django REST Framework
- SQLite
- django-filter
- Rule-based AI prediction

## Features

- User authentication
- Role-based access for customers, agents, and administrators
- Create, view, update, and delete tickets according to permissions
- Automatic ticket category prediction
- Automatic ticket priority prediction
- Search tickets by title or description
- Filter tickets by status, priority, and category
- Pagination for ticket lists
- Dashboard summary with ticket statistics
- Restricted access to customer tickets

## Ticket Categories

- Technical
- Payment
- Account
- Other

## Ticket Priorities

- Low
- Medium
- High
- Urgent

## Ticket Statuses

- Open
- In Progress
- Resolved
- Closed

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/tickets/` | List accessible tickets |
| POST | `/api/tickets/` | Create a ticket |
| GET | `/api/tickets/<id>/` | Retrieve a ticket |
| PUT/PATCH | `/api/tickets/<id>/` | Update a ticket |
| DELETE | `/api/tickets/<id>/` | Delete a ticket, subject to permissions |
| GET | `/api/dashboard/summary/` | View dashboard statistics |
| POST | `/api/predict/` | Predict ticket category and priority |

## Search and Filtering

Search tickets by title or description:

`/api/tickets/?search=login`

Filter by status:

`/api/tickets/?status=open`

Filter by priority:

`/api/tickets/?priority=high`

Filter by category:

`/api/tickets/?category=payment`

Pagination example:

`/api/tickets/?page=2`

## AI Prediction

The project uses a rule-based prediction function to estimate a ticket's category and priority from its description.

Example request:

```json
{
  "description": "I cannot access my account because login is not working"
}
```

Example response:

```json
{
  "description": "I cannot access my account because login is not working",
  "predicted_category": "account",
  "predicted_priority": "high"
}
```

This is a rule-based approach, not a trained machine learning model.

## Installation and Setup

1. Clone or download the project.
2. Open a terminal in the folder containing `manage.py`.
3. Install the required packages:

   ```bash
   pip install django djangorestframework django-filter
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Create an administrator account if needed:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Open the API in your browser:

   `http://127.0.0.1:8000/api/tickets/`

## Admin Panel

`http://127.0.0.1:8000/admin/`

Sign in using an administrator account.

## Authentication and Permissions

- Authentication is required for protected API endpoints.
- Customers can access their own tickets.
- Support agents and administrators can access tickets across users.
- Customers cannot change ticket category, priority, or status through restricted update operations.

## Dashboard

The dashboard summary endpoint provides ticket counts, including total tickets, open tickets, in-progress tickets, resolved tickets, closed tickets, and high-priority tickets.

## Notes

This project is intended for learning and demonstration. The built-in Django development server is suitable for local development, not production deployment.
