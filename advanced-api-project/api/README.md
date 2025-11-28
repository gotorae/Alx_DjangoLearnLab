
# Advanced API Project — Books API (DRF Generic Views)

## Endpoints
- `GET /books/` — List all books (search, ordering, optional year filters)
- `GET /books/<int:pk>/` — Retrieve a single book
- `POST /books/create/` — Create a new book (authenticated)
- `PUT/PATCH /books/<int:pk>/update/` — Update an existing book (authenticated)
- `DELETE /books/<int:pk>/delete/` — Delete a book (authenticated)

## Permissions
- Read-only (List/Detail): allowed for unauthenticated users
- Write (Create/Update/Delete): requires authentication
- Global DRF defaults set in `settings.py` with Session & Basic authentication

## Validation
- `BookSerializer.validate_publication_year` ensures the year is not in the future.
- `AuthorSerializer` nests books as `books = BookSerializer(many=True, read_only=True)`.

## Filters & Ordering
- `?search=` on `title` and `author__name`
- `?ordering=publication_year` or `-publication_year`
- `?min_year=YYYY&max_year=YYYY` to constrain year range

## Notes
- Extend `perform_create`/`perform_update` for domain-specific logic (e.g., audit fields).
- Consider Token or JWT auth for non-browser clients in production.
