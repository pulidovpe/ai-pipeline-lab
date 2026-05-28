# 🤖 AI Pipeline Lab

Laboratorio práctico para integrar Inteligencia Artificial en pipelines de CI/CD usando **Cloudflare Workers AI** y **GitHub Actions**. 100% gratuito, sin tarjeta de crédito.

---

## 🛠 Herramientas utilizadas

| Herramienta | Free Tier | Registro |
|---|---|---|
| Cloudflare Workers AI (LLaMA 3.3 70B) | 10,000 req/día | cloudflare.com |
| GitHub Actions | 2,000 min/mes | github.com |
| GitHub Copilot Free | 2,000 completions/mes | github.com/copilot |
| GitHub Agentic Workflows (gh-aw) | Technical Preview | github.com/github/gh-aw |

---

## 📋 Requisitos previos

- Cuenta GitHub (free)
- Cuenta Cloudflare (free, solo email)
- Git 2.23+ y GitHub CLI (`gh`) instalados y autenticados
- Python 3.11+
- Conocimientos básicos de GitHub Actions y YAML

---

## 🗂 Estructura del repositorio

```
ai-pipeline-lab/
├── .github/
│   └── workflows/
│       ├── ai-dispatcher.yml       # Responde con IA al abrir issues/PRs
│       ├── ai-pr-review.yml        # Review automático de código en PRs
│       ├── ci.yml                  # Pipeline CI con pytest
│       ├── ai-ci-fix.yml           # Auto-fix de fallas de CI con IA
│       ├── ai-issue-triage.yml     # Triage automático de issues
│       ├── ai-chatops.yml          # /ai-review on-demand en PRs
│       ├── daily-repo-status.md    # Reporte diario (Agentic Workflow)
│       └── ci-doctor.md            # SRE agente clasifica fallas CI
├── src/
│   ├── __init__.py                 # OBLIGATORIO para imports de pytest
│   └── calculadora.py
├── tests/
│   ├── __init__.py                 # OBLIGATORIO para imports de pytest
│   └── test_calculadora.py
├── requirements-dev.txt
├── CONTEXT.md                      # Reglas del proyecto para la IA
└── README.md
```

---

## ⚙️ Configuración inicial

### 1. Clonar y crear estructura

```bash
gh repo create ai-pipeline-lab --public --clone
cd ai-pipeline-lab
mkdir -p .github/workflows src tests
touch src/__init__.py tests/__init__.py
```

### 2. Configurar secrets

```bash
REPO=$(gh api user --jq .login)/ai-pipeline-lab

# Cloudflare Workers AI
gh secret set CF_ACCOUNT_ID --body "tu-account-id" --repo $REPO
gh secret set CF_TOKEN      --body "tu-cf-token"   --repo $REPO

# Para Tareas 6-7 (GitHub Agentic Workflows)
gh secret set COPILOT_GITHUB_TOKEN --body "github_pat_..." --repo $REPO
```

**Obtener credenciales:**
- `CF_ACCOUNT_ID` y `CF_TOKEN`: [cloudflare.com](https://cloudflare.com) → Workers & Pages → AI → Use REST API
- `COPILOT_GITHUB_TOKEN`: [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new) → Fine-grained → Account permissions → **Copilot Requests: Read-only**

### 3. Verificar Cloudflare antes de continuar

```bash
curl -s "https://api.cloudflare.com/client/v4/accounts/$CF_ACCOUNT_ID/ai/run/@cf/meta/llama-3.3-70b-instruct-fp8-fast" \
  -H "Authorization: Bearer $CF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"responde solo: ok"}]}' \
  | jq '.result.response'
# Debe responder texto, no null ni error
```

---

## 📚 Tareas del laboratorio

| # | Tarea | Nivel | Tiempo |
|---|---|---|---|
| 1 | Configuración del entorno | Básico | 20 min |
| 2 | Asistente IA en Issues y PRs | Básico | 30 min |
| 3 | Review automático de código | Intermedio | 30 min |
| 4 | Auto-fix de fallas de CI | Intermedio | 40 min |
| 5 | Triage de issues con IA | Intermedio | 30 min |
| 6 | GitHub Agentic Workflows | Avanzado | 45 min |
| 7 | CI Doctor autónomo | Avanzado | 45 min |

---

## ⚠️ Reglas importantes

> **Todos los workflows deben existir en `main`** para aparecer en la pestaña Actions y para que los triggers funcionen. Crea siempre los workflows en `main` primero.

> **Usa `cat > archivo << 'EOF'`** para crear archivos YAML desde terminal. Los editores pueden colapsar líneas multilínea causando errores de sintaxis.

> **`src/__init__.py` y `tests/__init__.py` son obligatorios.** Sin ellos pytest falla con `ModuleNotFoundError`.

> **`exit ${PIPESTATUS[0]}`** es necesario después de `pytest ... | tee` para que el exit code de pytest se propague correctamente. Sin esto, CI siempre reporta success aunque los tests fallen.

---

## 🔧 Solución de errores comunes

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: src` | Falta `src/__init__.py` | `touch src/__init__.py tests/__init__.py` |
| CI pasa aunque tests fallen | `pytest \| tee` devuelve exit 0 | Agregar `exit ${PIPESTATUS[0]}` |
| `workflow_run` se omite | CI no corrió desde `main` o falta `branches:` | Hacer push a `main` y agregar `branches:` al trigger |
| `AI CI Fix` no aparece en Actions | `.yml` solo en feature, no en `main` | Copiar todos los `.yml` a `main` |
| `accepts at most N args` | YAML multilínea colapsado por editor | Usar `cat > file << 'EOF'` |
| `RESPONSE=null` | `CF_ACCOUNT_ID` vacío | Verificar con `gh secret list` |
| `invalid refspec HEAD:refs/heads/branch/` | Barra extra en refspec | Usar variable bash `BRANCH` separada |
| Fix descartado — no es Python válido | IA devuelve markdown | Limpiar con `sed '/^\`\`\`/d'` antes de `ast.parse()` |
| Conflictos en `calculadora.py` | `main` y feature divergen | `git pull --no-rebase` + `git checkout --ours` |
| `gh aw` — `not authenticated` | Token en keyring no reconocido | Usar `gh aw add` en lugar de `add-wizard` |
| `activation artifact` HTTP 400 | Bug de gh-aw en cuentas free | Usar plan Team/Enterprise o Copilot Pro |

---

## 🤖 Cómo funciona cada workflow

### `ai-dispatcher.yml`
Se dispara al abrir un issue o PR. Lee el body con `gh issue view` / `gh pr view` y responde con un comentario generado por LLaMA 3.3 70B en Cloudflare.

### `ai-pr-review.yml`
Se dispara en PRs que modifiquen `src/**/*.py`. Obtiene el diff con `gh pr diff` y pide a la IA que detecte bugs, vulnerabilidades y malas prácticas.

### `ci.yml`
Pipeline estándar de pytest. Usa `PYTHONPATH=$(pwd)` y `exit ${PIPESTATUS[0]}` para reportar el exit code correctamente.

### `ai-ci-fix.yml`
Se dispara cuando `CI Tests` falla. Lee los logs con `gh run view --log-failed`, llama a Cloudflare Workers AI para generar un fix, lo valida con `ast.parse()`, corre los tests localmente y si pasan hace commit con `[skip ci]`.

### `ai-issue-triage.yml`
Se dispara al abrir un issue. Pide a la IA que clasifique en JSON (`tipo`, `prioridad`, `necesita_info`) y aplica los labels correspondientes.

### `ai-chatops.yml`
Responde al comando `/ai-review` en comentarios de PRs (solo OWNER/MEMBER). Ejecuta un security review del diff.

### `daily-repo-status.md` (Agentic Workflow)
Corre cada día laboral a las 9 AM UTC. El agente (Copilot) analiza el repo y crea un issue `[Daily Report]` con el estado del día.

### `ci-doctor.md` (Agentic Workflow)
Se dispara cuando `CI Tests` falla. El agente clasifica la falla (código, transitoria, flaky, config) y toma la acción correspondiente.

---

## 📖 Referencias

- [Cloudflare Workers AI REST API](https://developers.cloudflare.com/workers-ai/get-started/rest-api)
- [GitHub Agentic Workflows CLI](https://github.com/github/gh-aw)
- [Sample workflows — githubnext/agentics](https://github.com/githubnext/agentics)
- [Blog post oficial GitHub Agentic Workflows (feb 2026)](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows)
- [GitHub Actions workflow_run docs](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#workflow_run)
- [Quick Start gh-aw](https://github.github.com/gh-aw/setup/quick-start)

---

## 📄 Licencia

MIT — libre para usar, modificar y distribuir.
