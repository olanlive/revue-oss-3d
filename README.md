# Pépites Open Source Software 3D & VFX

Repo : `revue-oss-3d`

Veille open source liée à la **3D**, au **VFX** et à la **vidéo**.

Site statique (GitHub Pages) : **https://olanlive.github.io/revue-oss-3d/**

Flux RSS 2.0 : **https://olanlive.github.io/revue-oss-3d/feed.xml** (un item par découverte, lien vers l’ancre du bloc)

Cadence : **tous les jours** à **9h Europe/Paris** — quelques découvertes à chaque passage (add-ons Blender, pipeline USD/Alembic/assets, nouveaux outils).

## Priorités

1. Add-ons & extensions Blender
2. Pipeline USD / Alembic / asset management
3. Nouveaux outils qui naissent dans le domaine

## Résumés

**Résumé court et percutant : 1 à 2 phrases, ~280 caractères max** (le build avertit au-delà). Ce que fait l’outil ou ce qui est neuf dans cette version, avec la date de l’actu, pour donner envie de cliquer. Pas de pavé licence/maturité ; une mention très courte (« bêta », « payant ») seulement si essentielle.

## Ajouter une découverte

1. Éditer [`data/discoveries.json`](./data/discoveries.json) : ajouter un objet en tête (ou n’importe où — le build trie par date décroissante) :

```json
{
  "date": "2026-09-29",
  "name": "Nom de l’outil",
  "summary": "Ce que fait l’outil / ce qui est neuf (sortie le 28 sept). 1–2 phrases, ~280 caractères max.",
  "url": "https://…",
  "tags": ["blender-addon", "hair"]
}
```

2. Rebuild (régénère `docs/`, dont `docs/feed.xml`) :

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
- `docs/` — site publié (Pages depuis `main` / dossier `/docs`) : `index.html` (fil unique, plus récent en haut), `tags/*.html`, `feed.xml` (RSS 2.0, 100 dernières découvertes)

Chaque bloc `<article class="discovery">` a une ancre stable `id="AAAA-MM-JJ-nom-version"` (lien direct, utilisé par le flux RSS).

Pas de npm. Python 3 standard library uniquement.

## Licence

Notes de veille (liens vers les projets upstream, chacun avec sa propre licence).

## Source d’une découverte

Champ optionnel `source` dans `data/discoveries.json` : où la pépite a été repérée.

```json
"source": { "label": "Fil X — @compte", "url": "https://x.com/…" }
```

Libellés usuels : « Fil X — @compte », « Signet X », « Issue GitHub — owner/repo#123 », « Web — site ». Affiché sur le site sous le résumé (« Trouvé via : … »).
