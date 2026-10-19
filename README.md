# Bingie pour Kodi — dépôt ntls2000

Skin Bingie en cours d'adaptation pour **Kodi 22 Piers**, tout en conservant Kodi 21 Omega.

## Installer et mettre à jour sur tablette

Installer une seule fois [notre dépôt Kodi 1.0.1](https://raw.githubusercontent.com/ntls2000/skin.bingie/omega/repo/repository.ntls2000.bingie/repository.ntls2000.bingie-1.0.1.zip) dans **Kodi → Paramètres → Extensions → Installer depuis un fichier ZIP**, puis **Installer depuis un dépôt → Bingie - Dépôt de mises à jour**.

- Si **le dépôt 1.0.1 est déjà installé**, inutile de réinstaller le ZIP : Kodi relit automatiquement les nouvelles versions dans `addons.xml`.
- Le catalogue conserve une seconde source officielle Bingie pour les modules que nous ne gérons pas encore nous-mêmes.
- Les ZIP publiés par notre dépôt se trouvent dans `repo/<id>/<id>-<version>.zip`.

## Extensions maintenues dans nos trois dépôts GitHub

| Extension | Source modifiable sur GitHub | Version corrigée |
| --- | --- | --- |
| Bingie Toolbox | [script.bingie.toolbox](https://github.com/ntls2000/script.bingie.toolbox) | **1.0.1** |
| Bingie Widgets | [script.bingie.widgets](https://github.com/ntls2000/script.bingie.widgets) | **1.0.2** |
| Bingie Common Module | [script.module.bingie](https://github.com/ntls2000/script.module.bingie) | **1.0.2** |

Les versions précédentes originales proviennent du [dépôt Bingie de matke-84](https://github.com/matke-84/repository.bingie). Les crédits et licences sont conservés. Les corrections sont faites **dans chacun de ces trois dépôts indépendants** sur la branche `main`.

À chaque publication du dépôt Kodi, GitHub Actions récupère le code de ces trois dépôts dans `addons-src/` **temporairement dans le job de construction**. Le script `tools/build_kodi_repo.py` crée les trois archives d'extensions, les ZIP du skin et du dépôt, et le catalogue `addons.xml`. Ne pas créer ou modifier d'extensions dans le dépôt principal : modifier les dépôts autonomes.

### Correctifs de nos trois extensions

- **Toolbox 1.0.1** : chemins Unicode et XML écrit comme texte pour Kodi VFS, correction de la récupération des propriétés Skin Shortcuts ; protection contre l'ancien bouton 404 retiré dans Skin Shortcuts v3.
- **Widgets 1.0.2** : arguments des tentatives de connexion corrigés, meilleure gestion des codes HTTP dans la récupération des widgets.
- **Common Module 1.0.2** : évite une seconde exception SQLite sur Android si le cache ne peut pas être initialisé, et retente l'ouverture ultérieurement.
- Contrôle automatique du code Python avec l'analyseur Python 3.14 et vérification des manifestes Kodi.

Ces validations **ne démontrent pas** le fonctionnement complet dans Kodi 22 sur Android.

## Point bloquant : Skin Shortcuts 3

Kodi 22 inclut Skin Shortcuts 3, **non rétrocompatible** avec les anciens templates, overrides et userdata XML de Bingie. La migration du skin est encore en cours dans la branche [kodi22-skinshortcuts-v3](https://github.com/ntls2000/skin.bingie/tree/kodi22-skinshortcuts-v3). **Ne pas considérer Bingie 2.0.3 comme complètement compatible Kodi 22** avant cette migration et des tests sur appareil.

## Contrôles et génération

```sh
python3 tools/check_kodi22.py
python3 tools/build_kodi_repo.py
```

Pour construire le catalogue complet localement, cloner les trois dépôts d'extensions dans les sous-répertoires `addons-src/<id>/` avant d'exécuter le générateur. Le workflow `.github/workflows/publish-kodi-repo.yml` réalise automatiquement ces clonages sur GitHub Actions.
