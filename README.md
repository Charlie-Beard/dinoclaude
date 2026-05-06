# DinoClaude

A browser-based endless runner game inspired by the Chrome dino game, themed around Claude Code. Jump over **CONTEXT LIMIT** walls and duck under **OUT OF TOKENS** clouds.

Play it live at [dinoclaude.com](https://dinoclaude.com).

## How to play

| Action | Control |
|--------|---------|
| Jump | Space / Up arrow / Tap |
| Duck | Down arrow |
| Pause | P |

The game speeds up over time. Your high score is saved in the session.

## Stack

- Vanilla JS canvas game ([assets/js/game.js](assets/js/game.js)) — no dependencies, no build step
- [Jekyll](https://jekyllrb.com/) for templating and SEO tags
- Deployed to GitHub Pages via [GitHub Actions](.github/workflows/deploy.yml)
- Custom domain: `dinoclaude.com` (configured via [CNAME](CNAME))

## Local development

```bash
bundle install
bundle exec jekyll serve
```

Then open `http://localhost:4000`.

## Deployment

Pushing to `main` triggers the GitHub Actions workflow, which builds the Jekyll site and deploys it to GitHub Pages automatically.
