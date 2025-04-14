## Late Show API
A Flask-based REST API for managing late-night TV show episodes, guests, and their appearances, built for the Phase 4 Code Challenge at Moringa School.

This API provides structured endpoints to retrieve episode and guest data, create appearance records, and enforce data integrity through validations. It showcases database modeling with SQLAlchemy, JSON serialization, and RESTful design.

### Features
Retrieve all episodes or a specific episode with appearance details
List all guests
Create new appearances with validation
Seed database from a CSV file
Postman collection for streamlined testing
Database Schema

### Episodes
- id (Primary Key)
- date (String)
- number (Integer)

### Guests
- id (Primary Key)
- name (String)
- occupation (String)

###  Appearances
- id (Primary Key)
- rating (Integer)
- episode_id (Foreign Key)
- guest_id (Foreign Key)
### Database Relationships
One-to-Many: Episode → Appearances
An episode can have multiple appearances (multiple guests per episode).
Linked via episode_id in the Appearances table.
One-to-Many: Guest → Appearances
A guest can have multiple appearances (appearing on multiple episodes).
Linked via guest_id in the Appearances table.
Many-to-Many: Episodes ↔ Guests
Managed through the Appearances table.
Allows multiple guests per episode and multiple episodes per guest.
Appearances store additional data like ratings.
### API Endpoints
Method	Endpoint	Description
GET	/episodes	Retrieve all episodes
GET	/episodes/:id	Retrieve an episode with appearances
GET	/guests	Retrieve all guests
POST	/appearances	Create a new appearance
### Setup Instructions
### Prerequisites
Python 3.8 or higher
Virtual environment tool (e.g., venv)
Postman for API testing
### Author
Moureen Mutinda


License
MIT license.