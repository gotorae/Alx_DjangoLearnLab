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