# Bingie 2.0.4~beta1 — migration Skin Shortcuts 3 pour Kodi 22

**Statut : bêta expérimentale. Pas encore testée sur une tablette Kodi 22.**
Ne pas fusionner cette branche dans `omega` et ne pas l'imposer en mise à jour automatique.

## Versions confirmées (19 octobre 2026)
- Skin Shortcuts : **3.0.5~beta1** (préversion publiée le 18 octobre 2026).
- Dernière stable : **3.0.4**.
- Notre skin : **2.0.4~beta1**, dépendance minimale `script.skinshortcuts >= 3.0.4`.

## Changements réalisés
- `shortcuts/menus.xml` : définitions des menus Bingie (principal, power, recherche, hubs, personnalisés) et sous-menus Films/Séries.
- `shortcuts/widgets.xml` : groupes du nouveau sélecteur.
- `shortcuts/properties.xml` : boutons natifs d'édition des widgets, fonds, styles, limites et tris.
- `shortcuts/backgrounds.xml` : choix d'images statiques et personnalisées.
- `shortcuts/templates.xml` : nouveaux générateurs v3 des 8 zones de widgets Bingie.
- `Home.xml` : commande `type=buildxml` sans paramètres v2.
- `IncludesSkinSettings.xml` : `type=manage&menu=` au lieu de `group=`.
- `script-skinshortcuts.xml` : propriétés `menuname`, suppression des IDs obsolètes 101, 308 et 404, réaffectation des contrôles pour la v3.
- 34 sélecteurs de widgets intégrés : `type=skinstring` remplace `type=widgets`.
- Adaptation des noms d'includes générés pour les sous-menus et le menu power.
- Deux accès de secours directs vers **Paramètres Kodi** dans le menu principal et le menu d'alimentation, indépendants de la construction des raccourcis.

## Validation
- `python tools/check_kodi22.py` : XML et labels obsolètes vérifiés.
- `python tools/check_shortcuts_v3.py` : structure v3, noms, boutons, commandes et accès de secours.
- Génération d'un ZIP bêta distinct via `.github/workflows/check-shortcuts-v3.yml`.
- Exécution passée : https://github.com/ntls2000/skin.bingie/actions/runs/39288517400

## À confirmer sur un appareil Kodi 22
- Ouverture des menus, modification et mémorisation des raccourcis ;
- Widgets de chaque hub et génération des includes à l'exécution ;
- Parcours du picker widgets / images, sous-menus et retour aux paramètres ;
- Réglages utilisateur **v2** : sauvegarder avant test. La v3 utilise un fichier JSON nouveau et ne reprend pas automatiquement les anciens fichiers XML.
- Performances Android, dépendances Bingie et retour en Estuary.

Les anciens fichiers `shortcuts/template.xml` et `shortcuts/overrides.xml` restent présents comme références historiques, mais la v3 utilise les nouveaux fichiers au pluriel.

**Important :** tant que les tests sur Kodi 22 ne sont pas confirmés, garder Estuary actif et `omega` stable.
