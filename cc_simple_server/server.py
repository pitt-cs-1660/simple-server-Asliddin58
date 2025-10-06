from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from cc_simple_server.models import TaskCreate
from cc_simple_server.models import TaskRead
from cc_simple_server.database import init_db
from cc_simple_server.database import get_db_connection

# init
init_db()

app = FastAPI()

############################################
# Edit the code below this line
############################################


@app.get("/")
async def read_root():
    """
    This is already working!!!! Welcome to the Cloud Computing!
    """
    return {"message": "Welcome to the Cloud Computing!"}


# POST ROUTE data is sent in the body of the request
@app.post("/tasks/", response_model=TaskRead)
async def create_task(task_data: TaskCreate):
    """
    Create a new task

    Args:
        task_data (TaskCreate): The task data to be created

    Returns:
        TaskRead: The created task data
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
        (task_data.title, task_data.description, task_data.completed),
    )
    conn.commit()

    # get the id of the newly created task
    task_id = cursor.lastrowid

    # fetch the created task to return it
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    # convert database row to taskread object
    return TaskRead(**dict(row))


# GET ROUTE to get all tasks
@app.get("/tasks/", response_model=list[TaskRead])
async def get_tasks():
    """
    Get all tasks in the whole wide database

    Args:
        None

    Returns:
        list[TaskRead]: A list of all tasks in the database
    """
    from cc_simple_server.database import get_db_connection 
    from cc_simple_server.models import TaskRead
    ...
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    # convert database rows to taskread objects
    return [TaskRead(**dict(row)) for row in rows]


# UPDATE ROUTE data is sent in the body of the request and the task_id is in the URL
@app.put("/tasks/{task_id}/", response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskCreate):
    """
    Update a task by its ID

    Args:
        task_id (int): The ID of the task to be updated
        task_data (TaskCreate): The task data to be updated

    Returns:
        TaskRead: The updated task data
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # first, check if the task exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing_task = cursor.fetchone()
    if not existing_task:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    # update the task
    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
        (task_data.title, task_data.description, task_data.completed, task_id),
    )
    conn.commit()

    # fetch the updated task
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated_row = cursor.fetchone()
    conn.close()

    # return the updated task
    return TaskRead(**dict(updated_row))


# DELETE ROUTE task_id is in the URL
@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    """
    Delete a task by its ID

    Args:
        task_id (int): The ID of the task to be deleted

    Returns:
        dict: A message indicating that the task was deleted successfully
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # first, check if the task exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    existing_task = cursor.fetchone()
    if not existing_task:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    # delete the task
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    # return success message
    return {"message": f"Task {task_id} deleted successfully"}
