Original prompt: Look at all of our image files. They come from this book. There is a bone rig I made, too. Help us create the Bertie Physics system that operates similar to a Lotte Reiniger engine but more rigid, less smooth.

- 2026-03-15: Added rigid "Bertie Physics" with snapping + joint limits in canvas.html; default physics style set to smooth; refined hinge directions.
- 2026-03-15: Next goal: align cutout images to model using anchor joints.
- 2026-03-15: Added anchor-aware mask transforms (pivot at joint), anchor picking, default anchor fields, torso slot, and default cutout loader button.
- 2026-03-15: Fixed IK/global state issues (ikBodyMode), guarded DOM initialization, and added render_game_to_text/advanceTime hooks for testing.
- 2026-03-15: Added favicon data URI to avoid 404s; Playwright run clean (no errors).
