# Before Day 1: prerequisites (do these a week early)

## 1. A Fabric-capable account (the step most likely to block someone)
Microsoft Fabric needs a **work or school Microsoft Entra account**. A personal Gmail or Outlook account will not work.

Your instructor will tell you which route your class uses:
- **Route A (recommended for a class):** the instructor creates a Microsoft tenant, adds each student as a user, and assigns capacity to a shared workspace group. You receive a username and temporary password.
- **Route B:** you start your own Fabric trial with a work or school account. Trial rules change, so check the current Microsoft page before you rely on it.

Test on Day 0: open https://app.fabric.microsoft.com and sign in. If you see the Fabric home page, you are ready.

## 2. Tools on your laptop
| Tool | Why | Check |
|---|---|---|
| Git and a GitHub account | You will commit work as you go | `git --version` |
| Python 3.10 or newer | Data generator and loaders | `python --version` |
| A code editor (VS Code) | Editing scripts and SQL | opens |
| Your finished Chowly app running locally | It is the source system | you can place an order |
| An AI assistant of your choice | Required. You must log how you use it | you have an account |

## 3. Free accounts for your source systems
- **A Postgres database you can reach from the internet.** Options: Neon, Supabase, or Azure Database for PostgreSQL. Pick one and write down the connection string.
- **MongoDB Atlas free cluster (M0).** In Network Access, allow access from anywhere for the lab (`0.0.0.0/0`). Never do this for real data.
- Keep both connection strings in a `.env` file. Never commit `.env`.
- Create the MongoDB cluster **before Day 1**. On Day 2 you will write to it from your Chowly app.
- You must be able to edit and run your own Chowly source code. Day 2 adds features to it.

## 4. Fork this repo
Fork it on GitHub, clone your fork, and work in your fork. Your commit history is part of your grade.
