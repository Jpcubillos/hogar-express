# Design System: Hogar Express

This document records the exact color tokens, typography, dimensions, and UI components used in the visual interface of Hogar Express, serving as a guideline for visual regression check.

## 1. Brand Color Palette

We utilize a curated color scheme matching the brand guidelines. No generic colors should be introduced.

| Token Name | Hex Code | Purpose |
|------------|----------|---------|
| `mostaza` | `#E0A52C` | Brand Primary / Active Sidebar State |
| `mostazaOscuro` | `#B8821E` | Warning / Active Recargo text |
| `mostazaClaro` | `#FBF1DD` | Warning background |
| `azul` | `#2C5F8A` | Secondary Accent / Main Buttons |
| `azulOscuro` | `#1F4565` | Sidebar Background |
| `azulClaro` | `#E8F0F7` | Active pill background / Info badges |
| `carbon` | `#363432` | Primary Text |
| `carbonSuave` | `#6B6764` | Muted Text / Labels |
| `verde` | `#5B7F3C` | Success Badge Text / Paid states |
| `verdeClaro` | `#EBF1E3` | Success Badge Background |
| `rojo` | `#B6422E` | Danger Text / Mora / High Priority alert |
| `rojoClaro` | `#F8E8E4` | Danger Background |
| `fondo` | `#FBF9F5` | Main Application Workspace Background |
| `borde` | `#E5E0D6` | Standard Border color |

## 2. Typography

- **Headings & Logo Text:**
  - `font-family: Georgia, serif`
  - Used for Page titles (`h1`), modal titles, logo title, and large KPI numbers.
- **Body & Controls Text:**
  - `font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
  - Used for inputs, tables, buttons, secondary text, and descriptions.

## 3. Dimensions & Layout

- **Sidebar Width:** `232px` (fixed, dark blue background `#1F4565`, brand logo section has white background `#FFFFFF`).
- **Main Workspace Padding:** `28px 32px` (background `#FBF9F5`, dynamic layout offset).
- **Cards Padding:** `20px` (border: `1px solid #E5E0D6`, border-radius: `10px`).
- **Input Borders:** `1px solid #E5E0D6` with border-radius: `7px`.
- **Button Padding:** `9px 16px` for medium, `6px 12px` for small. Border-radius: `8px`.
