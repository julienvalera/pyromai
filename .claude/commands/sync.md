---
description: Synchronise le contexte CLAUDE.md avec l'état actuel du projet
---

Tu es un assistant expert qui doit synchroniser le fichier CLAUDE.md avec l'état actuel du projet.

## Contexte
Le projet est situé dans `/Users/julienvalera/Projets/perso/clean-code-analyzer`

## Ta mission

### Étape 1 : Exploration du projet
1. Liste tous les fichiers du projet (ignore `.venv/`, `__pycache__/`, `.git/`, `*.pyc`, `reports/`)
2. Identifie les nouveaux fichiers créés depuis la dernière entrée dans CLAUDE.md
3. Lis les fichiers de code implémentés (`.py`, `.toml`, etc.)
4. Si Git est initialisé, utilise `git status` et `git log --oneline -10` pour contexte additionnel

### Étape 2 : Analyse des changements
Détecte et analyse :
- **Nouvelles features** : Fichiers créés, fonctionnalités implémentées
- **Architecture** : Changements de structure, nouveaux modules
- **Dépendances** : Nouvelles librairies dans `pyproject.toml`
- **Configuration** : Nouveaux fichiers de config (`.env`, `.gitignore`, etc.)
- **Documentation** : README, docstrings ajoutées
- **Tests** : Nouveaux tests implémentés

### Étape 3 : Mise à jour de CLAUDE.md
Mets à jour les sections suivantes si nécessaire :

#### Section "Architecture du PoC"
- Mets à jour la structure du projet si de nouveaux fichiers/répertoires existent
- Note les changements d'organisation

#### Section "Stack technique"
- Ajoute les nouvelles dépendances installées
- Note les versions si importantes

#### Section "Roadmap"
- Marque ✅ les features implémentées
- Déplace les items terminés de "en cours" à "terminé"

#### Section "Journal des modifications"
Ajoute une nouvelle entrée datée (aujourd'hui = 2024-12-10) :
```markdown
### YYYY-MM-DD - [Titre descriptif] (Julien solo / avec Claude)
- [Liste des changements détectés]
- [Nouvelles features]
- [Modifications d'architecture]
- [Nouvelles dépendances]
```

### Étape 4 : Présentation du résumé
Après avoir mis à jour CLAUDE.md, présente-moi un résumé clair :

```
## 🔄 Synchronisation effectuée

### Changements détectés :
- [Liste des fichiers nouveaux/modifiés]
- [Features implémentées]
- [Dépendances ajoutées]

### Sections mises à jour dans CLAUDE.md :
- [Liste des sections modifiées]

### Prochaines étapes suggérées :
- [Suggestions basées sur l'état du projet]
```

## Notes importantes
- Sois exhaustif dans l'exploration
- Ne devine pas : base-toi sur le code réel
- Si incertain sur une intention, demande confirmation
- Préserve le format et le style existant de CLAUDE.md
