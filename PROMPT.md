# Competition Prompt

This is the exact prompt delivered to each **Paul** instance — the [Digiswarm AI](https://digiswarm.ai) liaison agent for each competing model. Every Paul received this brief identically, with no additional context about the other competitors.

---

## Delivered To

| Agent Instance | Model |
|---|---|
| Paul (Anthropic) | Anthropic Claude |
| Paul (DeepSeek) | DeepSeek |
| Paul (Qwen3) | Qwen3-Coder-Nex 85B |

---

## Instructions to Paul

**This is an AI model competition. Read these instructions carefully before beginning.**

You are competing against other AI models to build the best possible implementation of the brief below. Your output will be judged on originality, quality, and elegance of design.

**Autonomous execution is required. Do not ask the human any questions. Do not prompt the user for input, decisions, clarifications, or confirmations at any point during the session.** This is a fire-and-forget competition — the human will not be present or monitoring while you work. Make all architectural and design decisions independently using your best judgment.

The human will review the final site only after **all GitHub Issues and Pull Requests in the repo are closed**. That is the signal that your work is complete. Until that condition is met, the human will not intervene.

If you encounter ambiguity in the requirements, resolve it yourself and proceed. If you hit a technical obstacle, work around it. Do not stop and wait for guidance.

---

## The Brief

Build a complete static e-commerce demo site called **"Fizban's Wands."**

The site is inspired by Fizban from the Dragonlance Chronicles. It should feel like a whimsical magical wand shop, but it must run as a static site deployable on GitHub Pages.

---

### Catalog Requirements

Create a catalog of magical wands with seed data. There must be 3 alignment categories:

1. Good
2. Neutral
3. Evil

Each category must contain **at least 12 wands** for sale. Each wand should include:

- Name
- Alignment category
- Description
- Price in gold pieces
- Image or generated placeholder image
- Magical properties or special effect
- Rarity level

---

### Site Pages & Features

The site must include:

- Home page
- Wand catalog page
- Category filtering by alignment
- Product detail view or modal
- Shopping cart
- Support for multiple different wands in the cart
- Support for quantities per wand
- Cart total shown in gold pieces
- Checkout flow
- New customer starting balance of 1,000 gold pieces
- Deduct credits after successful purchase
- Prevent checkout if the customer does not have enough credits
- Order confirmation page or modal

---

### Data Persistence

Because this is a GitHub Pages static site, do not require a backend database. Use `localStorage` for:

- Customer gold balance
- Shopping cart
- Purchase history

---

### Simulated Email Receipt

When a customer buys a wand, simulate emailing them a picture of the wand. Since GitHub Pages cannot send real email without a backend service, implement this as a **"magical delivery receipt"** or **"simulated email"** shown on the order confirmation screen. Include the purchased wand images in the receipt.

---

### Cart Behavior

The shopping cart must allow multiple purchases and quantities. Buying 2 of the same wand should deduct 2× the wand price.

---

### Technical Requirements

- Build as a **React app** suitable for deployment to GitHub Pages
- Use **Vite** if appropriate
- Set the correct `base` path in `vite.config.js` to match the repository name so assets resolve correctly on GitHub Pages
- **Set up a GitHub Actions CI/CD workflow** (`.github/workflows/deploy.yml`) that automatically builds and deploys the site to GitHub Pages on every push to `main` — this is required, not optional
- In the GitHub repository settings, configure Pages source to **GitHub Actions** (not a branch)
- The final result must be runnable locally with `npm install` and `npm run dev`
- The final result must be buildable with `npm run build`
- Make the UI **polished, fantasy-themed, and responsive** for desktop and mobile

---

### README Requirements

Include a README in the project explaining:

- How to run locally
- How the seed data works
- How customer credits work
- How checkout works
- How the simulated email receipt works
- How to deploy to GitHub Pages
- What settings must be enabled in the GitHub repository
