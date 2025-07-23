# Room Reservation System

A robust backend system for managing room reservations in hotels or accommodations, built with Django and Django REST framework.

## Features

### Core Features
- Complete room management system
- User authentication and authorization
- Reservation management with status tracking
- API documentation with Swagger and Redoc
- JWT-based authentication

### Room Management
- Different room types (Single, Double, Twin, Suit, Deluxe)
- Room status tracking (Available, Reserved, Cleaning, Maintenance)
- Price management per night
- Capacity management
- Room amenities tracking

### Client Management
- Client profile management
- Contact information storage
- Document number tracking
- Address management
- Email and phone validation

### Reservation System
- Date range validation
- Room availability checking with real-time status
- Capacity validation with guest count tracking
- Reservation status tracking (Pending, Confirmed, Cancelled)
- Automatic price calculation based on nights and room rate
- Guest number validation
- Overlap prevention for conflicting reservations
- Room status consideration (maintenance, cleaning)

### Security Features
- Role-based access control
- JWT token authentication
- Token blacklist support
- Secure password hashing
- Email uniqueness validation

## Technical Stack

### Backend
- Django 5.1.5
- Django REST Framework
- Django Simple JWT
- DRF Spectacular for API documentation
- Python 3.12

### Dependencies
- rest_framework
- rest_framework_simplejwt
- drf_spectacular
- phonenumber_field

## API Endpoints

### Authentication
- POST /api/token/ - Obtain JWT token
- POST /api/token/refresh/ - Refresh JWT token

### Rooms
- GET /room/ - List all rooms (authenticated users)
- POST /room/ - Create new room (admin only)
- GET /room/{id}/ - Get room details (authenticated users)
- PUT /room/{id}/ - Update room (admin only)
- DELETE /room/{id}/ - Delete room (admin only)
- GET /room/availability/ - Check room availability for specific dates

### Clients
- GET /client/ - List clients (admin sees all, users see own profile)
- POST /client/ - Create new client profile (authenticated users)
- GET /client/{id}/ - Get client details (own profile or admin)
- PUT /client/{id}/ - Update client (own profile or admin)
- DELETE /client/{id}/ - Delete client (admin only)

### Reservations
- GET /reservation/ - List reservations (admin sees all, users see own)
- POST /reservation/ - Create new reservation (admin only)
- GET /reservation/{id}/ - Get reservation details (own reservations or admin)
- PUT /reservation/{id}/ - Update reservation (admin only)
- DELETE /reservation/{id}/ - Delete reservation (admin only)
- GET /reservation/my_reservations/ - Get current user's reservations

### User Registration
- POST /register/ - Register new user with optional client profile creation

## Setup Instructions

1. Clone the repository
2. Install UV (Python package manager):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Install dependencies:
   ```bash
   uv sync
   ```
4. Activate virtual environment:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
5. Set up environment variables:
   - Create a `.env` file in the project root
   - Add the following variables:
     ```
     SECRET_KEY=your_secret_key
     DEBUG=True
     SIGNING_KEY=your_signing_key
     DATABASE_URL=postgresql://user:password@localhost:5432/room_reservations
     ```
6. Apply migrations:
   ```bash
   python manage.py migrate
   ```
7. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

The API is documented using DRF Spectacular. You can access the documentation at:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Security Notes

- All endpoints require authentication except for user registration
- Admin privileges are required for creating, updating, or deleting rooms and reservations
- Users can only view and manage their own client profiles and reservations
- Strong password requirements enforced (8+ chars, uppercase, lowercase, numbers, special chars)
- Email and username uniqueness validation
- JWT tokens have a 2-hour expiration time
- Refresh tokens are valid for 30 days
- Automatic client profile creation during user registration
- Document number uniqueness validation for clients

## New Features Added

### Enhanced Reservation System
- **Guest Count Tracking**: Reservations now include number of guests with capacity validation
- **Automatic Price Calculation**: Total price is calculated automatically based on nights and room rate
- **Advanced Availability Checking**: Room status (maintenance, cleaning) is considered in availability
- **Real-time Availability API**: New endpoint to check room availability for specific date ranges

### Improved User Management
- **Enhanced Registration**: Users can create client profiles during registration
- **Profile Integration**: Automatic linking between User accounts and Client profiles
- **Secure Access Control**: Users can only access their own data unless they're administrators

### Room Availability System
- **Availability Query**: GET /room/availability/ endpoint with parameters:
  - `date_in`: Check-in date (YYYY-MM-DD)
  - `date_out`: Check-out date (YYYY-MM-DD)
  - `guests`: Number of guests (optional, default: 1)
  - `room_type`: Filter by room type (optional)
- **Real-time Results**: Shows available rooms with pricing information
- **Comprehensive Filtering**: Considers room status, existing reservations, and capacity

### Enhanced Data Validation
- **Document Number Uniqueness**: Prevents duplicate client document numbers
- **Email Validation**: Enhanced email format and uniqueness checking
- **Date Validation**: Prevents past-date reservations and invalid date ranges
- **Capacity Validation**: Ensures guest count doesn't exceed room capacity

### Testing Suite
- **Comprehensive Test Coverage**: Unit tests for models, serializers, and API endpoints
- **Authentication Testing**: Tests for JWT authentication and authorization
- **Validation Testing**: Tests for all data validation rules
- **API Integration Testing**: End-to-end API functionality testing

## Usage Examples

### Check Room Availability
```bash
GET /room/availability/?date_in=2024-12-25&date_out=2024-12-27&guests=2&room_type=double
```

### Register User with Client Profile
```json
POST /register/
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "client_profile": {
    "name": "John",
    "lastname": "Doe",
    "document_number": "12345678",
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "country": "USA",
    "phone": "+1234567890"
  }
}
```

### Create Reservation (Admin only)
```json
POST /reservation/
{
  "date_in": "2024-12-25",
  "date_out": "2024-12-27",
  "number_of_guests": 2,
  "client": 1,
  "room": 101
}
```

## Testing

Run the test suite with:
```bash
python manage.py test
```

Run tests with coverage:
```bash
pytest --cov=reservations --cov-report=html
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your new feature
4. Ensure all tests pass (`python manage.py test`)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
