---
name: changelog-and-commit
description: Aktualizuje changelog, podbija wersję projektu i tworzy release commit w repozytorium InAir, z zachowaniem wersji w pyproject.toml i manifest Home Assistant.
---

# Umiejętność: Wersjonowanie i release dla InAir

Ta umiejętność przygotowuje release dla repozytorium InAir przez workflow Semantic Release na GitHub Actions.

Wywołanie: `/changelog-and-commit` (z myślnikami).

## Gdzie trzymana jest wersja w tym projekcie
W repozytorium wersja występuje w dwóch miejscach:
- `pyproject.toml` — wersja projektu Python / pakietu
- `custom_components/inair/manifest.json` — wersja integracji Home Assistant

Przy nowym wydaniu oba pola muszą mieć ten sam numer.

## Wymagania wstępne
- Git i GitHub CLI (`gh`) są zainstalowane, a `gh auth status` potwierdza dostęp do repozytorium.
- Zmiany są wypchnięte na `master`.
- Workflow `.github/workflows/release.yaml` jest uruchamiany przez `workflow_dispatch`; push sam nie publikuje release.

## Flow release

### 1. Sprawdź proponowaną wersję
Semantic Release analizuje commity od ostatniego tagu. Commity `refactor:` są wydaniem patch; pozostałe typy używają domyślnych reguł Conventional Commits.

Uruchom dry-run, który nie publikuje release i nie zmienia plików:
```bash
gh workflow run release.yaml --repo mitabi/InAir --ref master -f dryRun=true
gh run list --repo mitabi/InAir --workflow release.yaml --limit 1
```
Sprawdź log runu i potwierdź, że wybrana wersja oraz changelog obejmują oczekiwane zmiany.

### 2. Opublikuj release
Po poprawnym dry-run uruchom workflow z `dryRun=false`:
```bash
gh workflow run release.yaml --repo mitabi/InAir --ref master -f dryRun=false
gh run list --repo mitabi/InAir --workflow release.yaml --limit 1
```
Semantic Release aktualizuje `CHANGELOG.md`, `pyproject.toml`, `custom_components/inair/manifest.json` i `uv.lock`, tworzy commit oraz tag i publikuje release. Nie zmieniaj tych plików ani nie twórz ręcznych commitów wersji przed dispatch.

### 3. Sprawdź release
Poczekaj na sukces workflow i potwierdź release:
```bash
gh release view vX.Y.Z --repo mitabi/InAir
```

## Dodatkowa uwaga dla InAir
Nie uruchamiaj `dryRun=false`, jeśli dry-run nie wskazuje oczekiwanej wersji. Workflow musi ustawić identyczną wersję w `pyproject.toml` i `custom_components/inair/manifest.json`.

## Minimalna checklist
- [ ] zmiany wypchnięte na `master`
- [ ] dry-run wskazuje oczekiwaną wersję
- [ ] uruchomiono workflow z `dryRun=false`
- [ ] workflow zakończył się sukcesem
- [ ] release istnieje na GitHub, a wersje pakietu i integracji są zgodne

## Przykład wydania
```bash
gh workflow run release.yaml --repo mitabi/InAir --ref master -f dryRun=true
# Po sprawdzeniu logów i wskazanej wersji:
gh workflow run release.yaml --repo mitabi/InAir --ref master -f dryRun=false
```