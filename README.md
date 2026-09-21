# revue-oss-3d

Veille open source liée à la **3D**, au **VFX** et à la **vidéo**.

Site statique (GitHub Pages) : **https://olanlive.github.io/revue-oss-3d/**

Cadence : **lundi** et **jeudi** à **9h Europe/Paris** — 4–5 découvertes par revue (add-ons Blender, pipeline USD/Alembic/assets, nouveaux outils).

## Priorités

1. Add-ons & extensions Blender
2. Pipeline USD / Alembic / asset management
3. Nouveaux outils qui naissent dans le domaine

## Ajouter une revue

1. Éditer [`data/posts.json`](./data/posts.json) : ajouter un objet en tête (ou n’importe où — le build trie par date) :

```json
{
  "date": "2026-09-25",
  "title": "Revue OSS 3D — 22–25 septembre 2026",
  "items": [
    {
      "name": "Nom de l’outil",
      "summary": "Pourquoi ça compte, version, licence.",
      "url": "https://…",
      "tags": ["blender-addon", "hair"]
    }
  ]
}
```

2. Rebuild :

```bash
python3 scripts/build.py
```

3. Commit + push `data/`, `docs/`, et éventuellement ce README.

Le site dans `docs/` est la **source de vérité**. Les anciens fichiers `revues/*.md` ne sont plus utilisés.

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

- `data/posts.json` — contenu éditable
- `scripts/build.py` — génère le HTML dans `docs/`
- `docs/` — site publié (Pages depuis `main` / dossier `/docs`)

Pas de npm. Python 3 standard library uniquement.

## Licence

Notes de veille (liens vers les projets upstream, chacun avec sa propre licence).
