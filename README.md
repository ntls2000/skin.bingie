# Bingie — Skin Netflix pour Kodi

Fork de Bingie, maintenu pour Kodi **21 Omega** et **22 Piers**.

## Version 2.0.3 — première passe Kodi 22

- Conserve l'API `xbmc.gui 5.17.0` : Kodi 22 (`5.18.0`) accepte cette ABI et Kodi 21 reste pris en charge.
- Corrige les deux références à `Player.Cutlist`, supprimé dans Kodi 22, en utilisant `Player.Cuts`.
- Corrige des déclarations XML invalides, des URL de bande-annonce avec esperluette non échappée et des commentaires de classification mal formés.
- Ajoute `tools/check_kodi22.py` : vérification automatique du XML et des InfoLabels supprimés sous Kodi 22.

**Statut :** compatibilité du code du skin vérifiée statiquement. Les scripts Python externes, l'installation complète et les performances doivent encore être testés directement dans Kodi 22 RC sur appareil.

## Dépôt de mises à jour Kodi

Télécharger le ZIP du dépôt :

https://raw.githubusercontent.com/ntls2000/skin.bingie/omega/repo/repository.ntls2000.bingie/repository.ntls2000.bingie-1.0.0.zip

Dans Kodi : Paramètres → Extensions → Installer depuis un fichier ZIP, puis Installer depuis un dépôt → Bingie - Dépôt de mises à jour → Apparence → Habillages → Bingie.

Le dépôt est construit automatiquement par GitHub Actions sur la branche `omega`. Kodi repère les nouvelles versions grâce au numéro de version de `addon.xml`.

## Attention aux dépendances

Bingie dépend d'extensions tierces : `script.bingie.helper`, `script.bingie.toolbox`, `script.bingie.widgets`, `script.skinshortcuts`, `plugin.video.tmdb.bingie.helper`, `plugin.program.autocompletion` et `resource.images.studios.coloured`. Ce dépôt ne les embarque pas. Elles doivent être installées depuis des sources adaptées et vérifiées pour Kodi 22 / Python 3.14.

Avant les essais sous Kodi 22 : sauvegarder les paramètres et vérifier que le skin Estuary est utilisable comme interface de secours.

## Vérification

```sh
python3 tools/check_kodi22.py
python3 tools/build_kodi_repo.py
```

La réussite de ces contrôles ne remplace pas un test dans Kodi sur Android ou un autre système.
