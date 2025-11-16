# Permissions and Groups Setup

## Custom Permissions:
- can_view: View book details
- can_create: Create new books
- can_edit: Edit existing books
- can_delete: Delete books

## Groups:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: All permissions

## Usage:
- Decorators in views enforce permissions:
  @permission_required('bookshelf.can_edit', raise_exception=True)



  # Django Security Best Practices

## Configured Settings:
- DEBUG = False
- CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE = True
- SECURE_BROWSER_XSS_FILTER, SECURE_CONTENT_TYPE_NOSNIFF, X_FRAME_OPTIONS = 'DENY'
- CSP implemented via django-csp

## Templates:
- All forms include {% csrf_token %}

## Views:
- ORM used for queries to prevent SQL injection
- User input validated via Django forms

## Testing:
- Verified CSRF protection
- Checked XSS by attempting script injection in forms