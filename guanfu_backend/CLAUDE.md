# CLAUDE.md

> **Note**: This file is primarily for Claude AI development assistance and contains project context, guidelines, and documentation standards for AI-assisted development work.

## Project Overview

This is the Hualian Typhoon Rescue Site Backend system (花蓮光復救災平台後端), a disaster relief platform for coordinating rescue resources and services in the Guangfu area of Hualien, Taiwan.

## Technology Stack

- **Backend Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Frontend**: Google Sites
- **API Documentation**: Available at the backend repository

## Project Structure

```
Hualian-Typhoon-Rescue-Site-Backend-Team/
├── guanfu_backend/          # Main backend API service
│   ├── src/
│   │   ├── routers/         # API route handlers
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # Database operations
│   │   ├── database.py      # Database connection
│   │   └── config.py        # Configuration settings
│   └── README.md
├── human_resources_etl/     # ETL scripts for HR data
│   └── csv_to_human_resources.py
├── table_spec.md            # Database table specifications
└── README.md                # Project information
```

## API Endpoints

The backend provides the following resource endpoints:

- **Shelters** (`/shelters`) - Emergency shelter locations
- **Medical Stations** (`/medical_stations`) - Medical service points
- **Restrooms** (`/restrooms`) - Public restroom facilities
- **Shower Stations** (`/shower_stations`) - Shower facilities
- **Water Refill Stations** (`/water_refill_stations`) - Water supply points
- **Mental Health Resources** (`/mental_health_resources`) - Mental health support services
- **Human Resources** (`/human_resources`) - Personnel coordination
- **Accommodations** (`/accommodations`) - Temporary housing
- **Supplies** (`/supplies`) - Supply management
- **Supply Items** (`/supply_items`) - Individual supply items
- **Volunteer Organizations** (`/volunteer_organizations`) - NGO coordination
- **Reports** (`/reports`) - Incident reporting

## Key Resources

- **Official Website**: https://sites.google.com/view/guangfu250923/
- **UI Design (Figma)**: https://www.figma.com/design/3HmmJtwok42obsXH93s21b/
- **Backend Repository**: https://github.com/PichuChen/guangfu250923

## Development Notes

- Database specifications are documented in `table_spec.md`
- The project uses a PostgreSQL database for data persistence
- ETL scripts are available for importing CSV data into the system
- Additional documentation can be found in `guanfu_backend/docs/` directory

## Documentation Guidelines

When generating documentation for this project:

- **Language**: Use Traditional Chinese (繁體中文)
- **Terminology**: Follow Taiwan usage conventions, not Simplified Chinese
  - Use 文件 (not 文檔)
  - Use 軟體 (not 软件)
  - Use 網路 (not 网络)
  - Use 資料庫 (not 数据库)
  - Use 程式 (not 程序)
- **Tone**: Professional and clear, suitable for disaster relief coordination
- **Format**: Markdown format for all documentation files
