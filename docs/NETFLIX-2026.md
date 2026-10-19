# Bingie 2.0.5~beta2 — Accueil TV moderne (inspiré de Netflix 2026)

## Concept
Une **première version expérimentale** du nouvel accueil TV introduit par Netflix en 2025
et utilisé en 2026. La référence porte sur l'ergonomie du téléviseur, et non sur le
nouvel affichage des téléphones. Bingie reste une extension autonome de Kodi 22
et n'intègre aucune image ni aucun service Netflix.

## Mise en route
1. Mettre à jour `skin.bingie` depuis le dépôt Bingie habituel.
2. Depuis Bingie, ouvrir **Paramètres du skin → Accueil → Options du menu**.
3. Activer **Interface TV moderne inspirée de Netflix (2026)**.
4. Le skin se recharge automatiquement. Si nécessaire, sortir puis revenir à l'accueil.

## Fonctionnalités de cette première étape
- Barre horizontale permanente avec les raccourcis du menu principal, gérés par
  **Skin Shortcuts 3**. Leur texte, leur ordre et leurs actions personnalisées sont
  repris sans migration ni remise à zéro.
- Pastille blanche au focus et pastille grise sur la section active.
- Recherche, films, séries, Ma liste et raccourcis personnalisés accessibles à partir de
  la même barre. Les entrées existantes du menu restent éditables.
- Profil actif en haut à droite et **accès indépendant aux paramètres Kodi**.
- Grand visuel de mise en avant (fanart de Kodi, sans contenu de Netflix), sur fond sombre.
- Les widgets et leur contenu restent ceux de la médiathèque Kodi existante.
- Aucun changement dans les hubs ou les fenêtres de lecture.

## Mode classique et sécurité
Le mode moderne est **désactivé par défaut** pour préserver le fonctionnement
de la version précédente sur la tablette Android.
Pour revenir à Bingie classique, désactiver la même option dans les paramètres.
Si le skin ne s'affiche plus au premier test, refuser la confirmation du nouveau skin
pour que Kodi revienne à Estuary. Conserver une sauvegarde de Kodi.
Le raccourci de secours **Paramètres Kodi** est affiché même sans génération de raccourcis.

## À vérifier sur tablette
- Premier affichage et mise en avant d'un film/série existant.
- Navigation tactile et télécommande dans la barre et dans les widgets ;
  transition du focus (barre → widgets, widgets → barre).
- Action de « Recherche », « Séries », « Films », « Ma liste » et raccourcis modifiés.
- Ouverture du panneau paramètres du skin ; désactivation du mode et retour classique.
- Absence de chevauchement des boutons, du texte de présentation et des rangées.

## Limites de la beta
Cette version remplace le **menu d'accueil** et le **visuel de mise en avant** ;
ce n'est pas une reproduction pixel-perfect de Netflix. Le carrousel de cartes
vedettes, les transitions de prévisualisation et les cartes d'information
contextuelles seront affinés après retour visuel depuis Kodi 22.

## Corrections d'après la capture tablette (beta2)
- Les libellés du menu ne défilent plus en dehors du bord droit : seulement quatre
  onglets (Accueil, Séries, Films, Ma liste) restent visibles ; Recherche est indépendante.
- Les menus de ce mode sont éditables via Skin Shortcuts 3 dans les paramètres d'accueil.
  L'ancien menu conserve ses raccourcis et ses libellés personnalisés.
- Le gigantesque titre de section héritée (« Accueil ») ne recouvre plus la mise en avant.
- La carte principale dispose d'un titre provenant du contenu Spotlight de Kodi,
  d'un genre, d'une année, d'un résumé et des actions **Lire** et **Plus d'infos**.
- Les rangées de widgets utilisent de plus grandes cartes au format paysage ;
  le mode classique garde le format choisi dans chaque widget.
- Le premier widget est placé sous la carte vedette, sans chevaucher les textes.

### Vérifications prioritaires beta2
Confirmer que le titre du film/série apparaît dans la carte, que les actions Lire et
Plus d'infos sont fonctionnelles et que les cartes en paysage sont correctes. Sur
certains contenus ou extensions, Kodi peut ne pas fournir tous les champs de métadonnées.
