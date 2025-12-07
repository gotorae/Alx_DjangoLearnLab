"""login"""
"""logout"""



# Blog Post Management (CRUD)

Implements class-based views for the `Post` model:

- `PostListView` → `/posts/` shows all posts (public)
- `PostDetailView` → `/posts/<pk>/` shows one post (public)
- `PostCreateView` → `/posts/new/` creates a post (login required; `author` set to current user)
- `PostUpdateView` → `/posts/<pk>/edit/` edits a post (only the post's author)
- `PostDeleteView` → `/posts/<pk>/delete/` deletes a post (only the post's author)

## Permissions
- Creation requires authentication (`LoginRequiredMixin`).
- Editing/Deletion require the requester to be the post author (`UserPassesTestMixin`).
- List/Detail are accessible to all.

## Forms
- `PostForm` (ModelForm) exposes `title`, `content`. `author` is set server-side in `form_valid()`.

## Templates
- `posts_list.html`, `post_detail.html`, `post_form.html`, `post_confirm_delete.html`.
- Include `{% csrf_token %}` in all forms.

## Testing
Run:
```bash
python manage.py test blog



# Comment System

Adds a `Comment` model and CRUD around blog posts.

## Model
- `post` (FK → Post, `related_name='comments'`)
- `author` (FK → User, `related_name='comments'`)
- `content` (Text)
- `created_at`, `updated_at` (timestamps)

## URLs
- `POST /posts/<post_id>/comments/new/` → create (login required)
- `GET/POST /comments/<id>/edit/` → edit (author only)
- `POST /comments/<id>/delete/` → delete (author only)

## Templates
- Comments list + create form embedded in `post_detail.html`.
- Dedicated templates: `comment_form.html`, `comment_confirm_delete.html`.

## Security
- CSRF token in all forms.
- Only logged-in users can create.
- Only the comment author can edit/delete.

## Testing
```bash
python manage.py test blog
