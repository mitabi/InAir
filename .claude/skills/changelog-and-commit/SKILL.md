---
name: changelog-and-commit
description: Aktualizuje changelog, podbija wersję projektu i tworzy release commit w repozytorium InAir, z zachowaniem wersji w pyproject.toml i manifest Home Assistant.
---

# Umiejętność: Wersjonowanie i release dla InAir

Ta umiejętność ma przygotować poprawny release dla repozytorium InAir: aktualizuje wpis w changelog, podnosi wersję w odpowiednich plikach, a następnie robi commity i push do GitHub.

Wywołanie: `/changelog-and-commit` (z myślnikami).

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
- Dodaj nową sekcję na górze w formacie używanym w repo, np.:
  `## [1.7.6](https://github.com/mitabi/InAir/compare/v1.7.5...v1.7.6) (2026-09-26)`
- Wpisz zmiany w kategoriach użytych w repo: `### Features`, `### Bug Fixes`.
- Każda zmiana jako osobna linia `* ...`, spójnie ze stylem istniejących wpisów.

### 2. Podbij wersję w repo
- Zaktualizuj `version` w `pyproject.toml`.
- Zaktualizuj `version` w `custom_components/inair/manifest.json`.
- Upewnij się, że obie wartości są identyczne.

### 3. Zrób dwa commity release (wzorzec historii repo, oba z `[skip ci]`)
```bash
git add CHANGELOG.md
git commit -m "docs(changelog): describe v1.7.6 changes [skip ci]"

git add pyproject.toml custom_components/inair/manifest.json
git commit -m "chore(release): 1.7.6 [skip ci]"
```

### 4. Wypchnij zmiany
```bash
git push origin master
```

### 5. Opublikuj release na GitHub (krok ręczny)
Push **nie tworzy release**. Wersję na GitHub publikuje workflow „Build and release"
(`.github/workflows/release.yaml`, semantic-release, trigger ręczny):
GitHub → Actions → „Build and release" → Run workflow → `dryRun: false`.

## Zasady commitów release
Wzorzec z historii repo — dwa commity, oba z `[skip ci]`:

```bash
docs(changelog): describe vX.Y.Z changes [skip ci]
chore(release): X.Y.Z [skip ci]
```

## Dodatkowa uwaga dla InAir
Nie wolno publikować releasu, który zmienia tylko `pyproject.toml`. W projekcie Home Assistant integracja musi mieć zgodną wersję również w `custom_components/inair/manifest.json`.

## Minimalna checklist
- [ ] `CHANGELOG.md` zaktualizowany w formacie repo (link compare + data)
- [ ] commit `docs(changelog): describe vX.Y.Z changes [skip ci]`
- [ ] `pyproject.toml` ma nową wersję
- [ ] `custom_components/inair/manifest.json` ma tę samą wersję
- [ ] commit `chore(release): X.Y.Z [skip ci]`
- [ ] zmiany wypchnięte do `master`
- [ ] release opublikowany ręcznie: Actions → „Build and release" → `dryRun: false`

## Przykład gotowego wydania
```bash
# 1. Zmiana changelog i wersji
# 2. Commity
git add CHANGELOG.md
git commit -m "docs(changelog): describe v1.7.6 changes [skip ci]"

git add pyproject.toml custom_components/inair/manifest.json
git commit -m "chore(release): 1.7.6 [skip ci]"

# 3. Push
git push origin master

# 4. Release na GitHub (ręcznie): Actions → „Build and release" → dryRun: false
```