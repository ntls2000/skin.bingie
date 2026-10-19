# Bingie — Skin Netflix pour Kodi

Fork de Bingie, en adaptation vers Kodi **21 Omega** et **22 Piers**.

## Installation depuis Kodi (Android / tablette)

1. Télécharger et installer le fichier `repository.ntls2000.bingie-1.0.1.zip` depuis :
   https://raw.githubusercontent.com/ntls2000/skin.bingie/omega/repo/repository.ntls2000.bingie/repository.ntls2000.bingie-1.0.1.zip
2. Dans Kodi : **Paramètres → Extensions → Installer depuis un fichier ZIP**.
3. **Installer depuis un dépôt → Bingie - Dépôt de mises à jour → Apparence → Habillages → Bingie**.
4. Kodi doit rechercher les scripts Bingie depuis le **catalogue officiel de l'auteur**, intégré comme seconde source au dépôt depuis la version 1.0.1. Une connexion Internet et le dépôt Kodi officiel actif sont également nécessaires pour les modules généraux.

Ce dépôt publie **notre skin** (`skin.bingie` 2.0.3) tandis que les extensions tierces sont récupérées **directement à la source d'origine**, sans reconditionnement. La source ajoutée est :
https://github.com/matke-84/repository.bingie/tree/main/omega

## Avertissement Kodi 22 : Skin Shortcuts 3

La branche Kodi 22 du dépôt officiel Kodi peut proposer `script.skinshortcuts` v3.0.0. Bingie utilise encore les fichiers `shortcuts/template.xml` et `shortcuts/overrides.xml` de **Skin Shortcuts 2.0.3**. Skin Shortcuts v3 **n'est pas rétrocompatible** : le skin pourrait s'installer mais les menus personnalisés ne fonctionneraient pas.

**Solution provisoire sur Kodi 22** : avant d'activer Bingie, installer Skin Shortcuts **2.0.3** et désactiver les mises à jour automatiques de cette seule extension. Le fichier original v2.0.3 est disponible dans les archives du dépôt Kodi (Omega) :
https://mirrors.kodi.tv/addons/omega/script.skinshortcuts/script.skinshortcuts-2.0.3.zip

Une migration réelle de tous les menus Bingie vers Skin Shortcuts v3 reste à faire. Ne pas présenter cette première version comme totalement compatible Kodi 22.

## Version 2.0.3 — correctifs Kodi 22

- Garde l'ABI `xbmc.gui 5.17.0` pour Kodi 21 / Kodi 22.
- Remplace `Player.Cutlist` (supprimé de Kodi 22) par `Player.Cuts` dans le lecteur.
- Corrige plusieurs fichiers XML mal formés, des caractères non échappés et des commentaires invalides.
- Vérifie le XML et quelques labels supprimés automatiquement grâce à `tools/check_kodi22.py`.
- Repository v1.0.1 : référence le catalogue des scripts du dépôt officiel Bingie pour résolution automatique.

**Statut :** XML vérifié et packaging réussi sur GitHub Actions. Installation complète, scripts Python, interface et performances à vérifier **sur Kodi 22** avant d'annoncer une compatibilité totale.

## Génération

```sh
python3 tools/check_kodi22.py
python3 tools/build_kodi_repo.py
```

La publication de nouvelles versions se fait automatiquement via GitHub Actions sur la branche `omega`, dès que la version de l'extension augmente.
