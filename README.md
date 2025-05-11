# Technical Lesson: Flask Pagination

## Introduction

As your applications scale and datasets grow, returning all records at once can
overwhelm both your backend and frontend. That’s where pagination comes in.
Pagination lets you divide results into manageable “pages” and send only a subset of
data in each response—boosting performance and improving the user experience.

In this lesson, you’ll implement server-side pagination in a Flask API. You’ll write
a reusable pattern to handle query parameters like ?page=2&per_page=5 and return
paginated responses from endpoints like /recipes or /posts.

## Tools & Resources

- [GitHub Repo](https://github.com/learn-co-curriculum/flask-pagination-technical-lesson)
- [Flask SQLAlchemy Docs - paginate](https://flask-sqlalchemy.readthedocs.io/en/stable/pagination/)

## Set Up

The starter code includes a Flask app and seed data for a resource (e.g., Recipe).

To get started:

```bash
pipenv install && pipenv shell
cd server
flask db init
flask db migrate -m "initial migration"
flask db upgrade head
python seed.py
python app.py
```

You can view the API in your browser or using Postman. Test pagination by visiting
http://localhost:5555/recipes?page=1&per_page=5.

## Instructions

### Task 1: Define the Problem

Without pagination, your API will return all records in a table—even if the user only
needs the first 10. This increases response size, clutters the UI, and slows down
both the client and server.

We need to:
* Modify our GET routes (like /recipes) to accept pagination parameters.
* Return a subset of records based on page and per_page.
* Include metadata (like total pages) in the response.

### Task 2: Determine the Design

Backend Design Goals:

* Accept `?page=<number>&per_page=<number>` query params.
* Use SQLAlchemy’s .paginate() method to query the desired page.
* Return a JSON response with:
    * The current page of records
    * Metadata (e.g., current page, total pages, total items)

Example Response:
```json
{
  "page": 2,
  "per_page": 5,
  "total": 23,
  "total_pages": 5,
  "items": [
    {"id": 6, "title": "Tiramisu", ...},
    {"id": 7, "title": "Risotto", ...}
  ]
}
```

### Task 3: Develop, Test, and Refine the Code

#### Step 1: Accept Query Parameters

In your RecipeList resource get route:

```python
from flask import request

class Recipes(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
```

#### Step 2: Paginate SQLAlchemy Query

Use .paginate() to fetch just the right records:

```python
pagination = Recipe.query.paginate(page=page, per_page=per_page, error_out=False)
recipes = pagination.items
```

#### Step 3: Return Paginated Response

Include metadata and the records in the JSON response:

```python
return {
    "page": page,
    "per_page": per_page,
    "total": pagination.total,
    "total_pages": pagination.pages,
    "items": [RecipeSchema().dump(recipe) for recipe in recipes]
}, 200
```

#### Step 4: Test in Browser or Postman

Try endpoints like:
* `/recipes?page=1`
* `/recipes?page=2&per_page=3`

Ensure:
* No crash if page exceeds total
* Returns correct number of records
* Metadata reflects database accurately

#### Step 5: Commit and Push Git History

* Commit and push your code:

```bash
git add .
git commit -m "final solution"
git push
```

* If you created a separate feature branch, remember to open a PR on main and merge.

### Task 4: Document and Maintain

Best Practice documentation steps:
* Add comments to the code to explain purpose and logic, clarifying intent and functionality of your code to other developers.
* Update README text to reflect the functionality of the application following https://makeareadme.com. 
  * Add screenshot of completed work included in Markdown in README.
* Delete any stale branches on GitHub
* Remove unnecessary/commented out code
* If needed, update git ignore to remove sensitive data

## Conclusion

Pagination is a critical tool for building scalable APIs. It prevents unnecessary data transfer and gives clients the control to load only what they need. You’ve now implemented pagination using Flask and SQLAlchemy, returning both records and helpful metadata to support frontend UIs and mobile apps alike.

## Considerations

### Default Behavior and Flexibility

If the client does not send page or per_page, your route should fall back to sensible defaults (e.g., page=1, per_page=5).

This prevents 500 errors and makes your API more resilient to inconsistent client-side behavior.

### Per Page Limits

You may want to cap per_page values to prevent abuse (e.g., a user requesting 10,000 records at once).

A common pattern is to enforce a maximum like min(per_page, 100) to ensure consistent load.

### Pagination Metadata Is Critical

Clients (especially frontends using tables or infinite scroll) rely on metadata such as total, page, and total_pages to render UI controls.

If you only return the items, clients can’t know when to stop or what options to display.

### Sorting and Filtering

Pagination is often used with sorting and filtering.

For example, clients may request ?page=1&per_page=10&sort=title&search=pie.

Plan your pagination logic to layer nicely with additional filters or order_by() logic.

### Empty or Invalid Pages

Requests like ?page=999 shouldn’t crash or return a 404.

Returning an empty items array with correct metadata helps clients know they're at the end.

```json
{
  "page": 999,
  "items": [],
  "total": 42,
  "total_pages": 5
}
```

### Usefulness Beyond Frontend UIs

Pagination is also valuable for background services, admin tools, or any API where data size impacts bandwidth or performance.

Even internal tools should use pagination to prevent unexpected performance bottlenecks.