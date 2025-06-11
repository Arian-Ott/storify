# Contributing to Storify

Thank you for your interest in contributing to **Storify**!
Before making changes, it's important to understand how the project is structured and the guiding principles behind its design.

> [!IMPORTANT]
> If you have a suggestion, feel free to [open an issue on GitHub](https://github.com/Arian-Ott/storify/issues) — contributions and ideas from others are what make open source projects thrive.

---

## 📁 Folder Structure

When you clone the repository, you'll see the following structure:

* `.github/`: GitHub-specific configurations, including CI/CD workflows.
* `api/`: Backend code (e.g., database models, API routes, services).
* `docs/`: Documentation files and assets.
* `frontend/`: Frontend code (Jinja2 templates, static assets, etc.).
* `tests/`: Test suite (based on `pytest`).

Additionally, there are several important files:

* `.dockerignore`: Docker's equivalent to `.gitignore`.
* `.env.example`: Sample environment configuration.
* `.gitignore`: Files and folders to exclude from Git.
* `docker-compose.yml`: Defines the multi-container Docker setup.
* `Dockerfile`: Configuration for building the Docker image.
* `LICENSE`: Apache-2.0 licence file.
* `NOTICE`: Notice file accompanying the licence.
* `pyproject.toml`: Project metadata and dependency definitions.
* `README.md`: Project overview and setup instructions.

> [!NOTE]
> Most development happens inside the `api/`, `frontend/`, and `tests/` directories.

---

## 🧰 Tech Stack

Storify is built using a small but powerful tech stack centred around **FastAPI**.

### Frontend

Currently, the frontend is built with server-side rendering using **Jinja2** templates, styled via **Tailwind CSS**. However, it's designed to be modular — so modern frontend frameworks like **React**, **Next.js**, or **Nuxt** could be integrated later. Just open an issue if you'd like to explore this.

* **Templating**: Jinja2
* **Styling**: Tailwind CSS

### Backend

The backend follows an **MVC-inspired** pattern using:

* **Framework**: FastAPI
* **ORM**: SQLAlchemy
* **Database**: MariaDB

**Backend structure:**

* `api/models`: SQLAlchemy models (one file per logical entity).
* `api/routes`: FastAPI route definitions.
* `api/schemas`: Pydantic schemas (request/response validation).
* `api/services`: Business logic per model/entity.
* `api/utils`: General utilities, unrelated to specific models.
* `api/db.py`: Database engine configuration.
* `api/main.py`: Backend entry point.

---

## 🤝 How to Contribute

### Prerequisites

Make sure the following tools are installed:

* Python 3 (with `python3-venv`)
* Docker Engine
* Git

---

### 🔀 Contribution Workflow

1. **Open an Issue**
   Start by describing your proposed change or idea in a GitHub issue to align with maintainers and avoid duplicate work.

2. **Fork the Repository**
   Use GitHub’s “Fork” button to create your own copy of the project.

3. **Clone Your Fork Locally**

   ```bash
   git clone https://github.com/yourusername/storify.git
   cd storify
   ```

4. **Create a Development Branch**
   Always branch off from `dev`:

   ```bash
   git checkout -b your-feature-name dev
   ```

5. **Set Up Your Environment**
   We recommend using a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install .[dev]
   ```

6. **Make Your Changes**
   Implement your feature or fix while following the existing structure and code style.

7. **Lint and Format Your Code**
   Run Ruff to ensure consistent formatting and linting:

   ```bash
   ruff check .
   ruff format .
   ```

8. **Test Your Changes**
   Run the test suite before submitting:

   ```bash
   pytest
   ```

9. **Submit a Pull Request (PR)**
   Push your branch and open a PR to merge into `dev`. Include:

   * A clear summary of what you've changed
   * A reference to the related issue
   * Any notes for reviewers

10. **Review & Merge**
    The CI pipeline will run checks automatically. After approval, your changes will be merged into `dev`.

---

## 🚀 Release Process

We follow a structured release process to ensure **quality, consistency, and clarity** — with a twist: **stable releases** are named after characters from *The Matrix*, while **unstable development releases** are collectively referred to as **Zion**.

### 🔭 Branch Strategy

* `main`: Always stable and production-ready.
* `dev`: Ongoing development.
* `release/x.y.z`: Optional staging branch for preparing major/minor versions.

### 📎 Versioning

We follow [Semantic Versioning (SemVer)](https://semver.org/):
`MAJOR.MINOR.PATCH` → `v1.2.3`

Each **stable release** is given a **Matrix codename** (e.g., `v1.2.0 - Trinity`).
**Development versions** (alpha, beta, release candidates, etc.) are labelled as **Zion**.

#### Release Candidate Naming

Release candidates follow the pattern:

```txt
vX.Y.Z-rc.N (Zion)
```

Where `N` is the iteration count of the release candidate before the stable release.

### ◳ Release Workflow

1. **Prepare the Release**
   Once enough changes accumulate in `dev`, a release is staged (either in a `release/` branch or merged directly to `main`).

2. **Tag the Release**

   ```bash
   git tag -a v1.2.3 -m "v1.2.3 - Trinity"
   git push origin v1.2.3
   ```

3. **Update the Changelog**
   Summarise changes in `CHANGELOG.md`, using PR titles, commit messages, or tools like [`git-cliff`](https://github.com/orhun/git-cliff).

4. **Run the CI/CD Pipeline**
   On tagging or merging to `main`, the GitHub Actions pipeline will:

   * Run tests and linters
   * Build and push Docker images
   * (Optionally) deploy docs or artefacts

5. **Publish the GitHub Release**
   Include:

   * Version tag (e.g., `v1.2.3`)
   * Codename (e.g., `Trinity`)
   * Changelog
   * Links to artefacts (e.g., Docker Hub, documentation)

---

### 🎭 Naming Convention

| Type                  | Example               | Description                                     |
| --------------------- | --------------------- | ----------------------------------------------- |
| **Stable**            | `v1.2.0 - Trinity`    | Named after a *Matrix* character                |
| **Release Candidate** | `v1.2.0-rc.1 (Zion)`  | Pre-stable testing release, under Zion          |
| **Unstable/dev**      | `v1.3.0-dev.1 (Zion)` | All dev/pre-releases are grouped under **Zion** |

> [!NOTE]
> Stable releases are heroes of the *Matrix*. Development releases are experimental — forged in **Zion**, the heart of resistance.
