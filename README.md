# Tevlo

Tevlo is a teal, Messages-style texting app connected to the existing DreamWall Supabase project.

## Supabase
The app uses the existing Supabase project and keeps Tevlo messaging data separate with `tevlo_*` tables. Authentication uses Supabase Auth.

The production-ready HTML is the downloadable `tevlo.html` build from the ChatGPT conversation. The GitHub connector used here cannot directly upload a local sandbox file into a repository, so the final HTML should be added as `index.html` in this repository before enabling GitHub Pages.

## GitHub Pages
Set Pages to deploy from the `main` branch after `index.html` is added.
