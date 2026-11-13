# Stack facts for upload fixes

Stack facts to use in fixes. Check each against the project before you rely on it:
- The design system's upload component may default `accept` to `'*'`, have no size limit and no drop zone, and clear the native input only when its model is cleared from outside. Check whether it handles both `change` and `cancel`.
- The design system's image upload component may default to a size limit and accept `image/svg+xml` by default, checked against `file.type` only. Check whether it uses `useDropZone` and resets the input after reading. If it does, use it as the model for a custom image picker.
- The best custom picker in the project checks the MIME type *or* a case-insensitive extension, enforces a size limit, uses `useDropZone`, and resets the input. Use it as the model.
- Check whether the project has a CSV library. Hand-rolled imports often split on `'\r\n'` or `'\n'` and then on `','`, or use a regex split that doesn't support line breaks inside fields and turns `"null"`, `"true"`, and numeric text into values.
