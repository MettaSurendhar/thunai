# Adding a stack pack

A pack adds skills for one technology stack without touching the stack-agnostic core. Read [packs/README.md](../../packs/README.md) first for how packs are installed.

## Layout

```text
packs/<name>/
  pack.json
  skills/
    <skill>/
      SKILL.md
      references/        optional supporting files
```

## Steps

1. **Pick a name.** Lowercase, hyphenated, `<area>-<stack>` (for example `web-nextjs`, `api-fastapi`, `api-django`).
2. **Write skills.** Each skill folder name must equal the `name` in its frontmatter:

   ```markdown
   ---
   name: django
   description: Django and DRF development. Trigger on models.py, views, serializers, manage.py, migrations, "Django".
   ---
   ```

   The `description` is how agents decide to load the skill, so include the files, tools and phrases that should trigger it.
3. **Keep skills short and specific.** Cover when to use it, what differs from the defaults, a checklist and references. Do not repeat the core rules (git, scope, verification, security).
4. **Write `pack.json`:**

   ```json
   {
     "name": "api-django",
     "description": "One line.",
     "skills": ["django"],
     "detect": ["manage.py", "requirements.txt:django"],
     "stack": "Python, Django, DRF",
     "routing": { "backend": ["django"] }
   }
   ```

   - `skills` must list exactly the folders in `skills/`.
   - Names must not collide with core skills in `skills/`.
   - Every skill in `routing` must be in `skills`.
5. **Record sources.** If any content is copied or adapted from elsewhere, add it to [THIRD_PARTY.md](../../THIRD_PARTY.md) with URL, licence, copyright holder and relationship. Do not add content whose licence forbids redistribution.
6. **Validate:**

   ```powershell
   python .thunai/scripts/validate_template.py
   python .thunai/scripts/smoke_init.py
   ```

   Then try it in a scratch copy: `python init.py --non-interactive --name Scratch --packs api-django`, followed by `python .thunai/sync.py --check`.
7. **Document.** Add a row to the table in `packs/README.md` and a line under `Unreleased` in [CHANGELOG.md](../../CHANGELOG.md).

## Quality bar

- Guidance is accurate for a named, current version of the stack.
- No secrets, personal data, employer-specific names or private URLs.
- A reviewer can understand each skill in a couple of minutes.