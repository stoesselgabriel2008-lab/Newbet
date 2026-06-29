#!/usr/bin/env python3
"""Récupère les cotes foot (soccer) du jour chez Betclic et Pinnacle.

Source : The Odds API (https://the-odds-api.com/).
La clé API est lue depuis le fichier .env (variable ODDS_API_KEY).

Usage :
    python3 odds_foot.py                 # cotes foot d'aujourd'hui
    python3 odds_foot.py --date 2026-06-30
    python3 odds_foot.py --markets h2h   # marché 1N2 (par défaut)
    python3 odds_foot.py --all-leagues   # toutes les ligues soccer actives
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone, timedelta

import requests

API_BASE = "https://api.the-odds-api.com/v4"
# Clés bookmakers The Odds API : Betclic France = "betclic_fr" (et non "betclic").
BOOKMAKERS = ["betclic_fr", "pinnacle"]
REGIONS = "eu"  # Betclic + Pinnacle sont dans la région "eu"


# --------------------------------------------------------------------------- #
# Chargement de .env (sans dépendance obligatoire à python-dotenv)
# --------------------------------------------------------------------------- #
def load_env(path: str = ".env") -> None:
    """Charge les variables d'un fichier .env dans os.environ."""
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv(path)
        return
    except ImportError:
        pass  # fallback manuel ci-dessous

    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    target = path if os.path.exists(path) else here
    if not os.path.exists(target):
        return
    with open(target, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


# --------------------------------------------------------------------------- #
# Appels API
# --------------------------------------------------------------------------- #
def api_get(path: str, api_key: str, **params) -> tuple[object, dict]:
    """Appelle l'API et renvoie (json, headers de quota)."""
    params["apiKey"] = api_key
    url = f"{API_BASE}{path}"
    resp = requests.get(url, params=params, timeout=30)
    if resp.status_code == 401:
        sys.exit("❌ Clé API invalide ou manquante (401). Vérifie ODDS_API_KEY dans .env.")
    if resp.status_code == 429:
        sys.exit("❌ Quota dépassé (429). Réessaie plus tard.")
    if not resp.ok:
        sys.exit(f"❌ Erreur API {resp.status_code} : {resp.text[:300]}")
    quota = {
        "remaining": resp.headers.get("x-requests-remaining"),
        "used": resp.headers.get("x-requests-used"),
    }
    return resp.json(), quota


def list_soccer_sports(api_key: str) -> list[dict]:
    """Renvoie la liste des compétitions de foot actives."""
    sports, _ = api_get("/sports", api_key)
    return [s for s in sports if s.get("group") == "Soccer" and s.get("active")]


def fetch_odds(api_key: str, sport_key: str, markets: str,
               time_from: str, time_to: str) -> tuple[list, dict]:
    """Récupère les cotes d'une compétition pour Betclic + Pinnacle."""
    data, quota = api_get(
        f"/sports/{sport_key}/odds",
        api_key,
        regions=REGIONS,
        markets=markets,
        bookmakers=",".join(BOOKMAKERS),
        oddsFormat="decimal",
        dateFormat="iso",
        commenceTimeFrom=time_from,
        commenceTimeTo=time_to,
    )
    return data, quota


# --------------------------------------------------------------------------- #
# Affichage
# --------------------------------------------------------------------------- #
def fmt_local(iso_ts: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_ts.replace("Z", "+00:00")).astimezone()
        return dt.strftime("%H:%M")
    except Exception:
        return iso_ts


def bookmaker_odds(event: dict, book_key: str, market_key: str) -> dict[str, float]:
    """Renvoie {nom_issue: cote} pour un bookmaker et un marché donnés."""
    for book in event.get("bookmakers", []):
        if book.get("key") != book_key:
            continue
        for market in book.get("markets", []):
            if market.get("key") != market_key:
                continue
            return {o["name"]: o["price"] for o in market.get("outcomes", [])}
    return {}


def print_event(event: dict, market_key: str) -> None:
    home = event.get("home_team", "?")
    away = event.get("away_team", "?")
    heure = fmt_local(event.get("commence_time", ""))

    bet = bookmaker_odds(event, "betclic_fr", market_key)
    pin = bookmaker_odds(event, "pinnacle", market_key)
    if not bet and not pin:
        return  # aucun des deux books ne couvre ce match

    print(f"  {heure}  {home} vs {away}")
    # ordre d'affichage : domicile, nul, extérieur
    issues = [home, "Draw", away] if market_key == "h2h" else sorted(
        set(bet) | set(pin))
    labels = {home: "1 (dom.)", "Draw": "N (nul)", away: "2 (ext.)"}
    header = f"{'':<10}{'Betclic':>10}{'Pinnacle':>10}"
    print("    " + header)
    for issue in issues:
        b = bet.get(issue)
        p = pin.get(issue)
        if b is None and p is None:
            continue
        label = labels.get(issue, issue)[:10]
        bs = f"{b:.2f}" if b is not None else "—"
        ps = f"{p:.2f}" if p is not None else "—"
        print(f"    {label:<10}{bs:>10}{ps:>10}")
    print()


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description="Cotes foot Betclic & Pinnacle (The Odds API)")
    parser.add_argument("--date", help="Jour ciblé AAAA-MM-JJ (défaut : aujourd'hui)")
    parser.add_argument("--markets", default="h2h", help="Marché(s), défaut h2h (1N2)")
    parser.add_argument("--all-leagues", action="store_true",
                        help="Interroge toutes les ligues soccer actives (consomme plus de quota)")
    args = parser.parse_args()

    load_env()
    api_key = os.environ.get("ODDS_API_KEY")
    if not api_key:
        sys.exit("❌ ODDS_API_KEY introuvable. Crée un fichier .env (voir .env.example).")

    # Fenêtre temporelle de la journée (en UTC, format exigé par l'API)
    if args.date:
        day = datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    else:
        now = datetime.now(timezone.utc)
        day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    time_from = day.strftime("%Y-%m-%dT%H:%M:%SZ")
    time_to = (day + timedelta(days=1) - timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"⚽ Cotes foot du {day.strftime('%Y-%m-%d')} — Betclic vs Pinnacle\n")

    sports = list_soccer_sports(api_key)
    if not args.all_leagues:
        # Par défaut on garde les grandes compétitions pour économiser le quota
        priorities = (
            "soccer_france_ligue_one", "soccer_epl", "soccer_spain_la_liga",
            "soccer_italy_serie_a", "soccer_germany_bundesliga",
            "soccer_uefa_champs_league", "soccer_uefa_europa_league",
            "soccer_uefa_european_championship", "soccer_fifa_world_cup",
            "soccer_conmebol_copa_america",
        )
        keep = [s for s in sports if s["key"] in priorities]
        sports = keep or sports  # si aucune des grandes n'est active, on prend tout

    total_matches = 0
    last_quota: dict = {}
    for sport in sports:
        events, last_quota = fetch_odds(
            api_key, sport["key"], args.markets, time_from, time_to)
        # ne garde que les matchs couverts par Betclic ou Pinnacle
        events = [e for e in events
                  if any(b.get("key") in BOOKMAKERS for b in e.get("bookmakers", []))]
        if not events:
            continue
        print(f"🏆 {sport.get('title', sport['key'])}")
        for ev in sorted(events, key=lambda e: e.get("commence_time", "")):
            print_event(ev, args.markets)
            total_matches += 1

    if total_matches == 0:
        print("Aucun match foot couvert par Betclic/Pinnacle pour cette date.")
    else:
        print(f"➡️  {total_matches} match(s) affiché(s).")

    if last_quota.get("remaining") is not None:
        print(f"\n📊 Quota API — restant : {last_quota['remaining']} | utilisé : {last_quota['used']}")


if __name__ == "__main__":
    main()
