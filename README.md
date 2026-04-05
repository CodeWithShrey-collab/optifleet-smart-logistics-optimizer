# OptiFleet: Smart Logistics & Delivery Optimizer

OptiFleet is a full-stack Flask application for logistics planning and delivery optimization. It combines operational CRUD workflows with classic Design and Analysis of Algorithms modules to support dispatch planning, truck loading, and warehouse network optimization.

The current implementation is fully database-driven and uses clean Flask separation:

- `routes/` for HTTP endpoints and page/API orchestration
- `services/` for algorithm logic
- `models/` for SQLAlchemy entities
- `templates/` for Jinja UI
- `static/` for AJAX and styling

## Implemented Modules

### Core Platform

- User registration and login with `Flask-Login`
- Session-based authentication
- SQLAlchemy models with SQLite persistence
- AJAX-driven UI updates without full-page reloads

### Orders

- Create, edit, list, and delete orders
- Validation for time windows, status, weights, profit, and required fields
- Database-backed pending order workflow for optimization modules

### Vehicles

- Create, edit, list, and delete vehicles
- Capacity and load validation
- Live availability and location management

### Warehouses

- Create, edit, list, and delete warehouses
- Latitude/longitude validation
- Database-managed warehouse network inputs

### Dashboard

- KPI cards for orders, pending orders, available vehicles, and total profit
- Chart.js order status visualization

### Truck Loading Optimizer

- Fractional Knapsack implementation
- Select a vehicle and pending orders
- Computes best value-to-weight allocation based on remaining truck capacity

### Smart Dispatch Engine

- Activity Selection for non-overlapping delivery windows
- Hamiltonian Cycle for a small selected delivery set
- Max Subarray for best contiguous profit streak
- Cleaned UI messaging for single-stop and edge-case outputs

### Smart Network Planner

- Kruskal's Minimum Spanning Tree implementation
- Dynamic edge generation from warehouse coordinates
- Haversine distance as network cost
- Displays optimized links and total network distance

## Tech Stack

- Backend: Flask, SQLAlchemy, Flask-Login, Flask-Migrate
- Frontend: Jinja2, Bootstrap, vanilla JavaScript, Chart.js
- Database: SQLite (development)
- Optional real-time support: Flask-SocketIO

## Project Structure

```text
optifleet/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   └── utils/
├── instance/
├── tests/
├── requirements.txt
├── run.py
└── README.md
```

## Setup

### 1. Create and activate a virtual environment

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the application

If port `5000` is unavailable on your system, use `5001`:

```powershell
python -c "from app import create_app; create_app().run(debug=True, port=5001)"
```

Then open:

- `http://127.0.0.1:5001/register`

## Default Development Database

The SQLite database is created automatically at:

- `instance/optifleet.db`

To reset local data, stop the app and delete that file.

## Recommended Manual Test Flow

1. Register a user account.
2. Add vehicles from `/vehicles`.
3. Add orders from `/orders`.
4. Add warehouses from `/warehouses`.
5. Open `/optimizer` and run the knapsack optimizer.
6. Open `/dispatch` and generate a dispatch plan.
7. Open `/network` and optimize the warehouse network.
8. Open `/dashboard` to confirm KPIs and chart updates.

## Example Warehouse Data

Use these to test the network planner:

- `North Hub`, `Delhi`, `28.6139`, `77.2090`
- `South Hub`, `Gurgaon`, `28.4595`, `77.0266`
- `East Hub`, `Noida`, `28.5355`, `77.3910`
- `West Hub`, `Ghaziabad`, `28.6692`, `77.4538`

## Available Pages

- `/register`
- `/login`
- `/dashboard`
- `/orders`
- `/vehicles`
- `/warehouses`
- `/optimizer`
- `/dispatch`
- `/network`

## Notes on Current Algorithm Behavior

- Dispatch selection is currently compatibility-first using classic Activity Selection, not weighted profit scheduling.
- The network planner computes MST from geographic coordinates, not from manually entered static edge costs.
- The knapsack optimizer supports fractional selection for truck loading.

## Planned Extensions

- Scheduler module improvements
- Weighted dispatch scheduling
- Search optimization module
- Analytics persistence/history
- Warehouse map visualization with Leaflet
- PostgreSQL-ready deployment configuration
- Automated tests

## Authoring Principles Used

- No hardcoded operational records
- Database-first behavior
- Service-layer algorithm isolation
- AJAX-based UX for CRUD and planning modules
- Modular, production-oriented Flask structure
