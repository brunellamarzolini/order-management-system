
# Book Order Manager Application

## Description

This project is a full-stack application for managing orders and products. It provides a user-friendly interface to view, filter, and update orders, with a Django REST backend and a Vue 3 + TypeScript frontend.


### Views / Pages

- **Order List:**
  - Paginated table of all orders
  - Search, filter by date, and sort by creation date or total amount

- **Order Detail:**
  - View and edit order details (name, description)
  - Add or remove products from the order
  - See product list and total amount (with live calculation on changes)


### Frontend Features

- Built with **Vue 3** and **TypeScript**
- Uses **Sass/SCSS** for styling, with variables and utility classes for consistent spacing, colors, and design tokens
- Reusable **base components** (inputs, buttons, forms, modals, tables, etc.) for a unified and maintainable UI
- JWT authentication with access/refresh token handling
- Toast notifications, composables for API/auth logic, and navigation guards

### Backend Features

- Built with **Django REST Framework**
- JWT authentication (SimpleJWT)
- API endpoints for orders and products
- **Localization:**
  - `localization` app provides multilingual support for product and order fields
  - Custom `TranslatedField` returns translated fields based on the `Accept-Language` header
- **Caching:**
  - Uses **Redis** for API response caching
  - `CacheDetailResponseMixin` and `CacheListResponseMixin` automatically caches list/detail responses for key endpoints
  - Cache keys are language-aware and include query params for granular control
  - Cache invalidation handled by Django signals for data consistency


**Backend API is available at [http://localhost:8000/api/schema/swagger-ui](http://localhost:8000/api/schema/swagger-ui)**  
**Frontend is available at [http://localhost:3000](http://localhost:3000)**


## Requirements

- [Docker](https://www.docker.com/) installed
- [Docker Compose](https://docs.docker.com/compose/) installed

## Getting Started

This project uses Docker for both the backend (Django) and frontend (Vue). All commands are run via npm scripts defined in the root `package.json`.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/brunellamarzolini/order-management-system.git
   cd order-management-system

### Setup (Required Steps)

To access and use the project, you must run, from the project root, the following commands in order:

1. **Start the project (detached mode):**
   ```bash
   npm run dev:detach
   ```
   > Starts all services in the background using Docker Compose.

2. **Populate the database with mock data:**
   ```bash
   npm run populate_osm
   ```
   > Populates the database with languages model and mock products and orders so you can browse and test the app.

3. **Create a superuser (for login):**
   ```bash
   npm run createsuperuser
   ```
   > Runs Django's createsuperuser command inside the backend container. This is required to log in to the application.

After completing these steps, you can access the frontend backoffice and backend api swagger as described above.

---

### Additional Commands

- **Run backend tests:**
  ```bash
  npm run test
  ```
  > Runs Django backend API tests.


## Possible Improvements

- **Frontend:**
  - Add a Product List page to view all products.
  - Add a Product Detail page to create or update products.
  - Integrate Vue I18n to localize the backoffice UI for multiple languages, making the frontend interface multilingual as well as the API data.

- **Backend:**
  - Switch from SQLite to PostgreSQL for production deployments to ensure better performance, scalability, and advanced database features.

- **General:**
  - use an `.env` file to store environment variables (such as database credentials, secret keys, and API URLs) for both backend and frontend.


## Notes
- All commands are run from the project root.
- The backend and frontend are both containerized; you do not need to install Python or Node dependencies manually.

---

For more details, see the scripts section in `package.json`.
