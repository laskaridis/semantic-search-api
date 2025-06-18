# Semantic Search API

This project provides a semantic search API that allows you to create collections of text documents, index them, and perform semantic searches
against these collections. This is effectively a playground exploring the implementation of semantic search use cases using transformers
(bi-encoder and cross-encoders).

## Setup Instructions

### Prerequisites

- Python 3.13 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the server with:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

or using uv:
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Loading Sample Data

To load a data sample with a collection of quotes use:
```bash
./bin/load.sh
```
This will load the quote vectors under the "quotes" collection.

### Searching Relevant Quptes

To search for quotes based on semantic relevancy use:
```bash
./bin/search.sh
```

## API Usage

### Collections

#### Create a Collection
```bash
curl -X POST http://localhost:8000/collections/my_collection
```

#### List All Collections
```bash
curl -X GET http://localhost:8000/collections
```

#### Delete a Collection
```bash
curl -X DELETE http://localhost:8000/collections/my_collection
```

### Documents

#### Index a document 
```bash
curl -X POST http://localhost:8000/index/my_collection \
  -H "Content-Type: application/json" \
  -d '{"id": "unique_id", "text": "Your text content here"}'
```

### Search

#### Semantic Search
```bash
curl -X GET "http://localhost:8000/search/my_collection?q=your+search+query&limit=5"
```

## Development

The project structure follows standard FastAPI conventions:
- `app`: Main application code
- `app/routes`: API endpoints
- `app/models.py`: Pydantic models
- `bin`: Utility scripts
- `models`: Downloaded transformer models for the bi and cross encoders
