# Django Template Best Practices

## Template Syntax Guidelines

### ✅ DO:
```html
<!-- Keep template tags on single lines when possible -->
{% if condition %}content{% endif %}

<!-- Use proper indentation for readability -->
{% if user.is_authenticated %}
    <div>User content</div>
{% endif %}

<!-- Break long attributes properly -->
<input type="text" 
       placeholder="Enter text here"
       {% if condition %}disabled{% endif %}
       class="form-control" />
```

### ❌ DON'T:
```html
<!-- Don't split template tags across lines unnecessarily -->
{% if condition
   %}content{% endif %}

<!-- Don't nest complex logic in attribute lines -->
<button onclick="function()" {% if complex_condition and another_condition
    %}disabled{% endif %}>

<!-- Don't mix template syntax with JavaScript improperly -->
<script>
    var data = {% if condition %}true{% endif %}; // Missing else case
</script>
```

## Common Template Errors

### 1. Unclosed Tags
- Always match `{% if %}` with `{% endif %}`
- Always match `{% block %}` with `{% endblock %}`
- Always match `{% for %}` with `{% endfor %}`

### 2. Template Tag Splitting
- Keep template tags on single lines when possible
- Use proper line breaks for readability
- Avoid splitting tags across multiple lines unnecessarily

### 3. JavaScript Integration
- Use `|safe` filter carefully
- Escape user data properly: `{{ data|escapejs }}`
- Use JSON filter for complex data: `{{ data|json_script:"data-id" }}`

## Validation Commands

```bash
# Check template syntax
python manage.py check --tag templates

# Validate specific template
python manage.py validate_templates app_name/template_name.html

# Run custom template checker
python check_templates.py
```

## IDE Setup
- Use Django template syntax highlighting
- Configure proper indentation (2-4 spaces)
- Enable template tag matching
- Use template linting plugins