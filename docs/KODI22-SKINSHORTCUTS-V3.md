# Kodi 22 — migration Skin Shortcuts 2 → 3

**Statut : travail en cours, NON INSTALLABLE.** Cette branche est séparée de `omega` pour protéger la version distribuée sur tablette.

Guide officiel de migration :
https://github.com/MikeSiLVO/script.skinshortcuts/blob/main/docs/migration-v2-to-v3.md

## Avancement réel

- [x] Créer la branche expérimentale `kodi22-skinshortcuts-v3`.
- [x] Ajouter `shortcuts/menus.xml` avec les entrées Bingie principales et le power menu à partir des anciens `.DATA.xml`.
- [x] Ajouter un premier `shortcuts/widgets.xml` avec des catégories vidéo, séries et musique.
- [ ] Migrer tous les menus secondaires : searchmenu, tmdbsearchmenu, moviehub, tvshowhub, newhub, musichub, customhub, somethinghub et mylisthub.
- [ ] Réécrire les 768 lignes de `shortcuts/template.xml` selon le format `shortcuts/templates.xml` de Skin Shortcuts 3. Les instructions `<other>`, `<submenuOther>`, `$SKINSHORTCUTS[]`, `$PYTHON[]`, les identifiants de conteneurs et les includes générés ne sont pas directement compatibles.
- [ ] Remplacer les appels `RunScript(script.skinshortcuts,type=widgets...)` par le nouveau sélecteur `type=skinstring`.
- [ ] Migrer `shortcuts/overrides.xml` vers les nouveaux `properties.xml`, `backgrounds.xml`, `menus.xml` et `widgets.xml`.
- [ ] Actualiser les contrôles des fenêtres v2 devenus obsolètes (dont 101-103, 111, 308, 404, 406-410).
- [ ] Adapter les références de l'interface aux nouveaux noms des includes générés par v3.
- [ ] Actualiser la dépendance `script.skinshortcuts` dans `addon.xml`, augmenter le numéro de version de Bingie et adapter les appels `buildxml` de Home.xml.
- [ ] Vérifier le XML, les includes à l'exécution et les journaux Kodi 22 sur Android.
- [ ] Publier sur `omega` uniquement après validation de la navigation, des widgets et des raccourcis.

## Point d'attention

Les personnalisations sauvegardées en XML sous Skin Shortcuts 2 ne sont pas migrées automatiquement vers le format JSON de Skin Shortcuts 3. Prévoir sauvegarde et reconstruction des menus utilisateur.

Les fichiers `overrides.xml` et `template.xml` d'origine sont intentionnellement préservés pendant la conversion, afin de comparer le comportement.
