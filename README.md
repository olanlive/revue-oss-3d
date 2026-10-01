# revue-oss-3d

Veille open source liée à la **3D**, au **VFX** et à la **vidéo**.

Site statique (GitHub Pages) : **https://olanlive.github.io/revue-oss-3d/**

Cadence : **tous les jours** à **9h Europe/Paris** — quelques découvertes à chaque passage (add-ons Blender, pipeline USD/Alembic/assets, nouveaux outils).

## Priorités

1. Add-ons & extensions Blender
2. Pipeline USD / Alembic / asset management
3. Nouveaux outils qui naissent dans le domaine

## Ajouter une découverte

1. Éditer [`data/discoveries.json`](./data/discoveries.json) : ajouter un objet en tête (ou n’importe où — le build trie par date décroissante) :

```json
{
  "date": "2026-09-29",
  "name": "Nom de l’outil",
  "summary": "Pourquoi ça compte, version, licence.",
  "url": "https://…",
  "tags": ["blender-addon", "hair"]
}
```

2. Rebuild :

```bash
python3 scripts/build.py
```

3. Commit + push `data/`, `docs/`, et éventuellement ce README.

Le site dans `docs/` est la **source de vérité**. Les anciens fichiers `revues/*.md` et le format groupé « revue » (`data/posts.json` + pages `docs/posts/`) ne sont plus utilisés : chaque découverte a sa propre date dans un fil chronologique plat.

## Tags (vocabulaire)

Utiliser ces tags kebab-case de façon cohérente :

| Tag | Usage |
|-----|--------|
| `blender-addon` | Extension / add-on Blender |
| `hair` | Cheveux / hair curves |
| `skinning` | Weight paint / skinning |
| `cad-retopo` | Retopo / CAD → mesh |
| `video` | Outils vidéo |
| `exr` | OpenEXR |
| `ocio` | OCIO / color management |
| `pipeline` | Pipeline général |
| `usd` | USD |
| `alembic` | Alembic |
| `assets` | Asset management |
| `compositing` | Compositing |
| `tracking` | Tracking |
| `sim` | Simulation |
| `encoding` | Encodage / codecs |
| `emerging` | Outil émergent / early alpha |

## Architecture

- `data/discoveries.json` — fil plat de découvertes (éditable)
- `scripts/build.py` — génère le HTML dans `docs/`
- `docs/` — site publié (Pages depuis `main` / dossier `/docs`)

Pas de npm. Python 3 standard library uniquement.

## Licence

Notes de veille (liens vers les projets upstream, chacun avec sa propre licence).
