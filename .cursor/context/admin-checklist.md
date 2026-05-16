# Shopify Admin Setup Checklist

This document tracks all manual configurations required in the Shopify Admin dashboard to make the custom theme function correctly.

## 1. Store Settings
- [ ] **Currency:** Set store default currency to ZAR (South African Rand) in `Settings > Store details`.

## 2. Navigation
- [ ] **Main Menu:** Go to `Online Store > Navigation > Main menu` and ensure it has: Home, Catalog, About Us, Contact.

## 3. Pages & Templates
- [ ] **About Page:** Create an "About Us" page in `Online Store > Pages`.
- [ ] **Assign Template:** On the "About Us" page, change the Theme Template dropdown from `Default page` to `about`.

## 4. Custom Metafields
Go to `Settings > Custom Data > Products` and create these exactly as named:
- [ ] **Latin Name:** Single line text (`custom.latin_name`)
- [ ] **Difficulty:** Number/Integer 1-5 (`custom.difficulty`)
- [ ] **Temperature Group:** Single line text (`custom.temperature_group`)
- [ ] **Trap Type:** Single line text (`custom.trap_type`)
- [ ] **Dormancy Required:** Boolean True/False (`custom.dormancy_required`)

## 5. Collections (Genera)
Go to `Products > Collections` and create:
- [ ] Drosera, Nepenthes, Pinguicula, Heliamphora, Cephalotus, Utricularia, Darlingtonia, Byblis, Drossophyllum, Sarracenia, Dionaea, Other, Growing Supplies.
- [ ] **Care Instructions:** For each collection, type the specific care guide (Light, Water, Soil) into the Collection **Description** text box.
- [ ] **Images:** Upload a high-quality macro photo as the Collection Image for each.
