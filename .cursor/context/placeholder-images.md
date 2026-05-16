# placeholder-images.md

# Placeholder Image Asset Map

Public-domain and Creative-Commons-licensed images sourced from **Wikimedia Commons** for use as placeholders during theme development in Cursor IDE. Each URL is a direct hotlink served by Wikimedia's `Special:FilePath` endpoint and is **safe to use during development**. The client must replace these with commissioned/licensed photography before launch.

> **License note:** All URLs below resolve to Wikimedia Commons files under public domain, CC0, CC BY, or CC BY-SA licenses. When integrating, the developer may keep them in placeholder JSON sections — Shopify will not re-host them automatically. For production, upload final assets to Shopify's CDN.

## Naming convention

`{genus}-{variant}-{type}-{index}.{ext}`

- `genus` — kebab-case genus or category name
- `variant` — optional sub-category (e.g. `highland`, `lowland`, `supplies-soil`)
- `type` — one of `hero`, `banner`, `product`, `macro`, `thumb`
- `index` — zero-padded number when more than one of the same type

## Asset Table

| Plant Genus / Component | Semantic Filename | Live URL |
|---|---|---|
| **Site — Home Hero** | `home-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Sarracenia_Judith_Hindle_(5964475729).jpg?width=2400 |
| **Drosera — Hero** | `drosera-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Drosera_Capensis.jpg?width=2000 |
| **Drosera — Macro** | `drosera-macro-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Drosera_capensis_bend.JPG?width=1600 |
| **Drosera — Product** | `drosera-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Drosera_aliciae2_ies.jpg?width=1200 |
| **Drosera — Product** | `drosera-product-02.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Drosera_binata_T_Voigt.jpg?width=1200 |
| **Nepenthes — Parent Hero** | `nepenthes-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Nepenthes_rajah.png?width=2000 |
| **Nepenthes — Macro** | `nepenthes-macro-peristome-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Large_lower_pitcher_of_wild_Nepenthes_rajah_plant.jpg?width=1600 |
| **Nepenthes Highland — Hero** | `nepenthes-highland-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Nepenthes_villosa.jpg?width=2000 |
| **Nepenthes Highland — Product** | `nepenthes-highland-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Nepenthes_villosa_(14238410874).jpg?width=1200 |
| **Nepenthes Highland — Product** | `nepenthes-highland-product-02.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Nepenthes_villosa_036.jpg?width=1200 |
| **Nepenthes Intermediate — Hero** | `nepenthes-intermediate-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Nepenthes_ventricosa4.jpg?width=2000 |
| **Nepenthes Intermediate — Product** | `nepenthes-intermediate-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Nepenthes_ventricosa0.jpg?width=1200 |
| **Nepenthes Intermediate — Product** | `nepenthes-intermediate-product-02.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Nepenthes_ventricosa1.jpg?width=1200 |
| **Nepenthes Lowland — Hero** | `nepenthes-lowland-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Nepenthes_ampullaria.jpg?width=2000 |
| **Nepenthes Lowland — Product** | `nepenthes-lowland-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Pitcher_Plant_(Nepenthes_ampullaria)_(8411421382).jpg?width=1200 |
| **Nepenthes Lowland — Product** | `nepenthes-lowland-product-02.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Nepenthes_ampullaria_multiple_inflorescences.jpg?width=1200 |
| **Pinguicula — Hero** | `pinguicula-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Pinguicula_moranensis.jpg?width=2000 |
| **Pinguicula — Macro** | `pinguicula-macro-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Pinguicula_moranensis_(and_prey).jpg?width=1600 |
| **Pinguicula — Product** | `pinguicula-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Pinguicula_moranensis_0zz.jpg?width=1200 |
| **Heliamphora — Hero** | `heliamphora-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Heliamphora_nutans_(a_pitcher_plant_from_Venezuela)_at_Kew_Gardens_(5253200783).jpg?width=2000 |
| **Heliamphora — Product** | `heliamphora-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Heliamphora_nutans.jpg?width=1200 |
| **Heliamphora — Product** | `heliamphora-product-02.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Heliamphora_nutans_(18564636764).jpg?width=1200 |
| **Cephalotus — Hero** | `cephalotus-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Cephalotus_follicularis_0001.JPG?width=2000 |
| **Cephalotus — Product** | `cephalotus-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Albany_Pitcher_Plant_Oxford_Botanic_Garden.jpg?width=1200 |
| **Cephalotus — Macro** | `cephalotus-macro-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Cephalotus_follicularis_Hennern_3.jpg?width=1600 |
| **Utricularia — Hero** | `utricularia-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Greater_Bladderwort_Utricularia_vulgaris_(6171429381).jpg?width=2000 |
| **Utricularia — Product** | `utricularia-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Greater_Bladderwort_Utricularia_vulgaris_(6171429243).jpg?width=1200 |
| **Utricularia — Macro** | `utricularia-macro-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Common_Bladderwort_(3630283910).jpg?width=1600 |
| **Darlingtonia — Hero** | `darlingtonia-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Darlingtonias.JPG?width=2000 |
| **Darlingtonia — Product** | `darlingtonia-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Cobra_Lily_(Darlingtonia_californica)_(5108542185).jpg?width=1200 |
| **Darlingtonia — Macro** | `darlingtonia-macro-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Darlingtonia_californica_ne5.JPG?width=1600 |
| **Byblis — Hero** | `byblis-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/ByblisLinifloraHabitus.JPG?width=2000 |
| **Byblis — Product** | `byblis-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/ByblisLinifloraFlora.JPG?width=1200 |
| **Drosophyllum — Hero** | `drossophyllum-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Drosophyllum_lusitanicum_RBGK.JPG?width=2000 |
| **Drosophyllum — Product** | `drossophyllum-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Drosophyllum_lusitanicum_b.jpg?width=1200 |
| **Drosophyllum — Macro** | `drossophyllum-macro-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Drosophyllum_lusitanicum_detail.JPG?width=1600 |
| **Sarracenia — Hero** | `sarracenia-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Sarracenia_Judith_Hindle_(5964475729).jpg?width=2000 |
| **Sarracenia — Product** | `sarracenia-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Sarracenia_((leucophylla_x_flava)_x_(purpurea_montana_x_flava))_x_%27Judith_Hindle%27_(5065614694).jpg?width=1200 |
| **Sarracenia — Product** | `sarracenia-product-02.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Sarracenia_(leucophylla_x_purpurea)_x_purpurea_(5065620220).jpg?width=1200 |
| **Dionaea — Hero** | `dionaea-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Venus_Fly_Trap_(Dionaea_muscipula).jpg?width=2000 |
| **Dionaea — Macro** | `dionaea-macro-trigger-hairs-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Venus_Flytrap_showing_trigger_hairs.jpg?width=1600 |
| **Dionaea — Product** | `dionaea-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Venus_flytrap_-_Dionaea_muscipula_-_panoramio_(3).jpg?width=1200 |
| **Other — Hero (Aldrovanda)** | `other-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Aldrovanda_vesiculosa.jpg?width=2000 |
| **Other — Product (Genlisea)** | `other-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Genlisea_violacea.jpg?width=1200 |
| **Growing Supplies — Hero** | `growing-supplies-hero-banner.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Sphagnum_centrale.jpeg?width=2000 |
| **Growing Supplies — Soil** | `growing-supplies-soil-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Schultz_Sphagnum_Peat_Moss.jpg?width=1200 |
| **Growing Supplies — Perlite** | `growing-supplies-perlite-product-01.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/PerliteUSGOV.jpg?width=1200 |
| **Growing Supplies — Perlite (use)** | `growing-supplies-perlite-product-02.jpg` | https://commons.wikimedia.org/wiki/Special:FilePath/Perlite_as_a_medium_for_rooting_of_cuttings.jpg?width=1200 |

## Usage Notes for the IDE Agent

1. **All URLs append `?width=N`** — Wikimedia's thumbnailer serves resized JPEGs on the fly. Adjust width per template (`2000` for hero, `1200` for product card, `400` for thumb).
2. **Hotlinking is permitted** by Wikimedia for reasonable-volume development use. For production, **download → re-upload to Shopify CDN**.
3. **CORS:** Wikimedia serves with permissive CORS, so these URLs work in `<img>`, CSS `background-image`, and `srcset` without proxying.
4. **WebP/AVIF:** Wikimedia does not serve WebP for these files. When wiring up `<picture>` elements, use these JPEGs in the fallback `<img>` and leave WebP/AVIF `<source>` slots commented for the client's final assets.
5. **Attribution:** During development, no attribution is required in the DOM, but keep a `/credits.txt` file in the theme root listing each file's Wikimedia Commons page URL until real assets land.
6. **Replace before launch:** Add a TODO comment everywhere a placeholder is used:
   ```liquid
   {%- comment -%} TODO: replace placeholder image before launch — see /placeholder-images.md {%- endcomment -%}

