# Changes:
## Structural Improvement: Abstraction and Decomposition

### File: `dashboard.py`

#### What was changed:
We extracted two components from `app.layout` into their own helper functions:

- `create_city_dropdown(data)`
- `create_pollutant_dropdown()`

These replace the direct `dcc.Dropdown()` components previously embedded in the layout definition.

#### Why was this done:
- **Abstraction**: This hides UI implementation details behind descriptive function names.
- **Decomposition**: The layout is now cleaner and easier to read or modify.
- **Maintainability**: If dropdown logic changes, we only update it in one place.

