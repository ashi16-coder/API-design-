# REST Endpoint Plan — Task Management API

## Users

| Method | Path            | Request Body  | Success Response       | Error Cases                  |
|--------|-----------------|---------------|------------------------|------------------------------|
| POST   | /users          | UserCreate    | 201 UserResponse       | 422 validation error         |
| GET    | /users/{id}     | —             | 200 UserResponse       | 404 user not found           |


## Tasks

| Method | Path                        | Request Body  | Success Response           | Error Cases                          |
|--------|-----------------------------|---------------|----------------------------|--------------------------------------|
| POST   | /users/{id}/tasks           | TaskCreate    | 201 TaskResponse           | 404 user not found, 422 validation   |
| GET    | /users/{id}/tasks           | —             | 200 PaginatedResponse      | 404 user not found                   |
| GET    | /tasks/{id}                 | —             | 200 TaskResponse           | 404 task not found                   |
| PATCH  | /tasks/{id}                 | TaskUpdate    | 200 TaskResponse           | 404 task not found, 422 validation   |
| DELETE | /tasks/{id}                 | —             | 204 No Content             | 404 task not found                   |


## Comments

| Method | Path                        | Request Body  | Success Response           | Error Cases                          |
|--------|-----------------------------|---------------|----------------------------|--------------------------------------|
| POST   | /tasks/{id}/comments        | CommentCreate | 201 CommentResponse        | 404 task not found, 422 validation   |
| GET    | /tasks/{id}/comments        | —             | 200 list[CommentResponse]  | 404 task not found                   |
| DELETE | /comments/{id}              | —             | 204 No Content             | 404 comment not found, 403 forbidden |


## Tags

| Method | Path       | Request Body | Success Response      | Error Cases          |
|--------|------------|--------------|-----------------------|----------------------|
| POST   | /tags      | TagCreate    | 201 TagResponse       | 409 tag name exists  |
| GET    | /tags      | —            | 200 list[TagResponse] | —                    |
| DELETE | /tags/{id} | —            | 204 No Content        | 404 tag not found    |


## Query Parameters (Tasks list)

| Param     | Type    | Description                        |
|-----------|---------|------------------------------------|
| status    | string  | Filter by status (todo/in_progress/done) |
| priority  | string  | Filter by priority (low/medium/high)     |
| tag_id    | int     | Filter by tag                      |
| page      | int     | Page number (default: 1)           |
| page_size | int     | Items per page (default: 20)       |


## HTTP Status Code Reference

| Code | Meaning              | When used                              |
|------|----------------------|----------------------------------------|
| 200  | OK                   | Successful GET / PATCH                 |
| 201  | Created              | Successful POST                        |
| 204  | No Content           | Successful DELETE                      |
| 403  | Forbidden            | Action not allowed for this user       |
| 404  | Not Found            | Resource does not exist                |
| 409  | Conflict             | Duplicate unique field (e.g. tag name) |
| 422  | Unprocessable Entity | Pydantic validation failure            |
