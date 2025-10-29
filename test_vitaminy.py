# test_vitaminy.py
import pytest
from playwright.sync_api import Page
import time

# Test 1: Načtení hlavní stránky a kontrola titulku
def test_hlavni_stranka_titulek(page: Page):
    page.goto("https://www.vitaminy-mineraly.cz/")
    assert page.title() == "VitaHarmony – český výrobce doplňků stravy | vitaminy-mineraly.cz"

# Test 2: Otevření nabídky Produkty (kontrola URL)
def test_otevreni_produkty(page: Page):
    page.goto("https://www.vitaminy-mineraly.cz/")
    page.click("text=Produkty")
    assert "/produkty/" in page.url

# Test 3: Vyhledání produktu a zobrazeni detailu
import pytest
from playwright.sync_api import Page, expect
import re

def test_vyhledani_a_detail_produktu(page: Page):
    # Otevření hlavní stránky
    page.goto("https://www.vitaminy-mineraly.cz/")
    page.wait_for_load_state("domcontentloaded")

    # Kliknutí na ikonu lupy (otevře vyhledávací pole)
    search_icon = page.locator("a[data-testid='linkSearchIcon']")
    expect(search_icon).to_be_visible()
    search_icon.click()

    # Zapsání hledaného výrazu a potvrzení Enter
    search_input = page.locator("input[type='search']")
    expect(search_input).to_be_visible()
    search_input.fill("vitamin C")
    page.keyboard.press("Enter")

    # Načítání výsledků
    produkty = page.locator(".product-item a, .product a")
    expect(produkty.first).to_be_visible(timeout=10000)

    # Kliknutí na první produkt ve výsledcích
    prvni_produkt = produkty.first
    prvni_produkt.scroll_into_view_if_needed()
    prvni_produkt.click()

    # Ověření, že URL obsahuje "vitamin"
    expect(page).to_have_url(re.compile(".*vitamin.*", re.IGNORECASE))

    # Ověření, že je vidět název produktu
    nazev_elem = page.locator("h1, .product-title").first
    expect(nazev_elem).to_be_visible()
    nazev_text = nazev_elem.inner_text().strip()
    assert nazev_text, "❌ Název produktu se nenačetl!"

    print(f"✅ Test prošel – vyhledán a otevřen produkt: {nazev_text}")

# Test 4: Vyhledání produktu a vložení do košíku

import re
from playwright.sync_api import Page, expect

def test_vlozeni_produktu_do_kosiku(page: Page):
    # Otevření hlavní stránky
    page.goto("https://www.vitaminy-mineraly.cz/")
    page.wait_for_load_state("domcontentloaded")

    # Kliknutí na ikonu lupy a vyhledání produktu
    search_icon = page.locator("a[data-testid='linkSearchIcon']")
    expect(search_icon).to_be_visible()
    search_icon.click()

    search_input = page.locator("input[type='search']")
    expect(search_input).to_be_visible()
    search_input.fill("vitamin C")
    page.keyboard.press("Enter")

    # Vyčkání na výsledky hledání a kliknutí na první produkt
    produkty = page.locator(".product-item a, .product a")
    expect(produkty.first).to_be_visible(timeout=10000)
    prvni_produkt = produkty.first
    prvni_produkt.scroll_into_view_if_needed()
    prvni_produkt.click()

    # Ověření, že URL obsahuje "vitamin"
    expect(page).to_have_url(re.compile(r"vitamin", re.IGNORECASE))

    # Nalezení tlačítka do košíku 
    pridat_kosik = page.locator(
        'button[data-testid="buttonAddToCart"][aria-label="Do košíku Vitamin C & Zinek Gummies (50 gummies)"]'
    )
    pridat_kosik.scroll_into_view_if_needed()
    pridat_kosik.wait_for(state="visible", timeout=15000)
    expect(pridat_kosik).to_be_enabled(timeout=15000)

    # Kliknutí na tlačítko – produkt je přidán
    pridat_kosik.click()

    print("✅ Test prošel – produkt byl přidán do košíku")
