# 🤖 Claude Code CLI Setup

Claude Code is our AI pair-programmer for the bootcamp. We do the **deep dive on Day 2**, but
please **install it and sign in now** so we don't lose class time. A **free tier or a small
amount of API credit is enough** for the course.

---

## 1. Install

Claude Code installs as a global npm package (Node 18+ required — you already have Node 20):

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:

```bash
claude --version
```

> macOS/Linux alternative (no npm): `curl -fsSL https://claude.ai/install.sh | bash`
> Windows alternative: `irm https://claude.ai/install.ps1 | iex`
> See the official docs for the latest options: <https://docs.claude.com/en/docs/claude-code>

## 2. Sign in

Run `claude` once in any folder and follow the login prompt:

```bash
claude
```

You can authenticate with:
- A **Claude account** (Pro/Max subscription), **or**
- An **Anthropic API key** (Console → API keys), set as `ANTHROPIC_API_KEY` or via the login flow.

Either is fine for the bootcamp. If you're unsure which to use, just log in with your Claude
account when prompted.

## 3. Sanity check

Inside the `claude` session, type a simple prompt:

```
> what is 2 + 2?
```

If it answers, you're connected. Type `/exit` (or Ctrl-C twice) to quit.

---

## ✅ Verify

`scripts/doctor.sh` checks that the `claude` command exists. Full project setup (permissions,
working in a repo, generating page objects) happens **together on Day 2** — no need to learn it
beforehand.

Trouble logging in? Bring it to the cohort channel or we'll sort it at the start of Day 2.
