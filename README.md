[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Z3Va95Y9)
# **Assignment: Task Manager API with FastAPI & SQLite**

## **Overview**

Build a **Task Manager API** using **FastAPI** and **SQLite**. This assignment is split into two phases:

- **Phase 1**: Local Python development and API implementation
- **Phase 2**: Docker containerization

---

## **Documentation**
- **Phase 1**: [python-setup.md](python-setup.md) - Local development setup
- **Phase 2**: [docker-setup.md](docker-setup.md) - Docker containerization
- [sqlite.md](sqlite.md) - Database information
- [rubric.md](rubric.md) - Grading criteria

---

## **Learning Objectives**

- Implement RESTful API endpoints using FastAPI
- Work with SQLite databases in Python
- Use modern Python tooling (uv, virtual environments)
- Containerize applications with Docker

---

## **Automated Testing**

Your assignment is automatically graded using **GitHub Actions**. Every push triggers:
- **API Tests**: Unit tests for your FastAPI endpoints (10 points)
- **Docker Validation**: Multi-stage Dockerfile requirements check
- **Container Tests**: Integration tests in running Docker container (5 points)

Check the Actions tab in your repository to view test results and your grade.

---

## **Phase 1: API Implementation**

**Prerequisites**: Complete [python-setup.md](python-setup.md) first.

Implement the following API endpoints in `cc_simple_server/server.py`:

1. **`GET /tasks/`**: Retrieve all tasks from the SQLite database
2. **`POST /tasks/`**: Create a new task in the SQLite database  
3. **`PUT /tasks/{task_id}/`**: Update an existing task in the SQLite database
4. **`DELETE /tasks/{task_id}/`**: Delete a task from the SQLite database

**Note**: The root endpoint `/` is already implemented and returns `{"message": "Welcome to the Cloud Computing!"}`

### **Testing Your Implementation**

```bash
# Activate your virtual environment
source .venv/bin/activate

# Run all tests
pytest tests/unit/test_server.py -v

# Start the server to test manually
uvicorn cc_simple_server.server:app --reload --host 127.0.0.1 --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation.

---

## **Phase 2: Docker Containerization**

**Prerequisites**: Complete Phase 1 first.

See [docker-setup.md](docker-setup.md) for containerization instructions.

## **Provided Code Structure**

### **Models** (`cc_simple_server/models.py`)
- **`TaskCreate`**: Request model with `title`, `description`, `completed` fields
- **`TaskRead`**: Response model that extends `TaskCreate` with `id` field

### **Database** (`cc_simple_server/database.py`)
- **`init_db()`**: Creates the SQLite database and `tasks` table
- **`get_db_connection()`**: Returns a database connection with row factory

### **API Endpoints** (`cc_simple_server/server.py`)
- Stub implementations that return `501 Not Implemented`
- Your job is to replace these with working implementations

---

## **Submission Instructions**

1. Implement all API routes in Phase 1
2. Complete Docker containerization in Phase 2  
3. Ensure all tests pass: `pytest tests/unit/test_server.py -v`
4. Push your code to GitHub and submit the repository URL

---

## **Example API Usage**

**Create a Task (`POST /tasks/`)**:
```json
{
  "title": "Finish assignment",
  "description": "Complete all API routes", 
  "completed": false
}
```

**Response**:
```json
{
  "id": 1,
  "title": "Finish assignment",
  "description": "Complete all API routes",
  "completed": false
}
```