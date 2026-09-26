---
name: changelog-and-commit
description: Aktualizuje changelog, podbija wersję projektu i tworzy release commit w repozytorium InAir, z zachowaniem wersji w pyproject.toml i manifest Home Assistant.
---

# Umiejętność: Wersjonowanie i release dla InAir

Ta umiejętność ma przygotować poprawny release dla repozytorium InAir: aktualizuje wpis w changelog, podnosi wersję w odpowiednich plikach, a następnie robi commit i push do GitHub.

## Gdzie trzymana jest wersja w tym projekcie
W repozytorium wersja występuje w dwóch miejscach:
- `pyproject.toml` — wersja projektu Python / pakietu
- `custom_components/inair/manifest.json` — wersja integracji Home Assistant

Przy nowym wydaniu oba pola muszą mieć ten sam numer.

## Wymagania wstępne
- Git jest zainstalowany i repo jest poprawnie skonfigurowane.
- Masz dostęp do zdalnego repozytorium GitHub.
- Plik `CHANGELOG.md` istnieje i ma format Keep a Changelog.

## Flow release

### 1. Zaktualizuj changelog
- Otwórz `CHANGELOG.md`.
- Dodaj nową sekcję wersji, np. `## [1.7.6] - 2026-09-25`.
- Uzupełnij wpis w kategoriach: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
- Zadbaj o spójność z formatem istniejących wpisów.

### 2. Podbij wersję w repo
- Zaktualizuj `version` w `pyproject.toml`.
- Zaktualizuj `version` w `custom_components/inair/manifest.json`.
- Upewnij się, że obie wartości są identyczne.

### 3. Zrób commit release
Użyj:

```bash
git add CHANGELOG.md pyproject.toml custom_components/inair/manifest.json
git commit -m "chore(release): bump version to X.Y.Z and update changelog"
```

### 4. Wypchnij zmiany
```bash
git push origin master
```

## Zasady commit message
Zalecany format:

```bash
chore(release): bump version to X.Y.Z and update changelog
```

To jest zgodne z praktyką Conventional Commits i jest zrozumiałe dla CI/CD.

## Dodatkowa uwaga dla InAir
Nie wolno publikować releasu, który zmienia tylko `pyproject.toml`. W projekcie Home Assistant integracja musi mieć zgodną wersję również w `custom_components/inair/manifest.json`.

## Minimalna checklist
- [ ] `CHANGELOG.md` został zaktualizowany
- [ ] `pyproject.toml` ma nową wersję
- [ ] `custom_components/inair/manifest.json` ma tę samą wersję
- [ ] commit ma sensowny komunikat release
- [ ] zmiany zostały wypchnięte do `master`

## Przykład gotowego wydania
```bash
# 1. Zmiana changelog i wersji
# 2. Commit
git add CHANGELOG.md pyproject.toml custom_components/inair/manifest.json
git commit -m "chore(release): bump version to 1.7.6 and update changelog"

# 3. Push
git push origin master
```