#!/usr/bin/env python3
"""Moteur déterministe MODE API pour le prompt Paris v13.

Calcule, à partir des cotes RÉELLES (The Odds API) :
- dévig de l'ancre sharp (Pinnacle) : multiplicatif, power, Shin (1X2 3 issues)
- ECART_METHODES (incertitude, en points de %)
- EV de la cible Betclic vs proba dévig de l'ancre
- test de robustesse ±2 pts

Aucune proba inventée : tout dérive des cotes relevées dans today.json.
"""
from __future__ import annotations
import json, math, sys

# --------------------------------------------------------------------------- #
# Méthodes de dévig
# --------------------------------------------------------------------------- #
def implied(odds):
    return [1.0 / o for o in odds]

def multiplicative(odds):
    r = implied(odds)
    s = sum(r)
    return [x / s for x in r], s - 1.0  # probas, overround

def power(odds, tol=1e-10):
    """p_i = r_i^k, k résolu pour sum=1 (bissection)."""
    r = implied(odds)
    lo, hi = 0.5, 5.0
    for _ in range(200):
        k = (lo + hi) / 2
        s = sum(x ** k for x in r)
        if s > 1:
            lo = k
        else:
            hi = k
        if abs(s - 1) < tol:
            break
    k = (lo + hi) / 2
    return [x ** k for x in r], k

def shin(odds, tol=1e-12):
    """Dévig de Shin : estime la proportion z d'argent informé."""
    r = implied(odds)
    S = sum(r)
    lo, hi = 0.0, 0.4
    def probs(z):
        denom = sum(math.sqrt(z * z + 4 * (1 - z) * (ri * ri) / S) for ri in r)
        return [(math.sqrt(z * z + 4 * (1 - z) * (ri * ri) / S) - z) / (2 * (1 - z))
                for ri in r] if z < 1 else r
    # bissection sur la contrainte sum(p)=1 (toujours vraie par construction) ;
    # on cherche z tel que la formule soit cohérente — ici on borne z par overround
    # méthode simple : z ≈ overround conduit, on résout sum=1 via normalisation interne
    for _ in range(200):
        z = (lo + hi) / 2
        p = probs(z)
        s = sum(p)
        if s > 1:
            lo = z
        else:
            hi = z
        if abs(s - 1) < tol:
            break
    z = (lo + hi) / 2
    p = probs(z)
    s = sum(p)
    return [x / s for x in p], z

# --------------------------------------------------------------------------- #
# EV + robustesse
# --------------------------------------------------------------------------- #
def ev(p, cote):
    return p * cote - 1.0

def ev_pct(p, cote):
    return 100.0 * ev(p, cote)

def robustness(p, cote, delta=0.02):
    return ev_pct(p - delta, cote), ev_pct(p + delta, cote)

def get_market(event, book_key, market_key):
    for b in event.get("bookmakers", []):
        if b["key"] == book_key:
            for m in b.get("markets", []):
                if m["key"] == market_key:
                    return {o["name"]: o for o in m["outcomes"]}, b.get("last_update")
    return None, None

# --------------------------------------------------------------------------- #
def analyse(event):
    home, away = event["home_team"], event["away_team"]
    print("=" * 72)
    print(f"{home} vs {away}  @ {event['commence_time']}  [{event.get('_league','')}]")
    print("=" * 72)

    pin_h2h, pin_h2h_upd = get_market(event, "pinnacle", "h2h")
    bet_h2h, bet_h2h_upd = get_market(event, "betclic_fr", "h2h")
    pin_t, _ = get_market(event, "pinnacle", "totals")
    bet_t, _ = get_market(event, "betclic_fr", "totals")

    if pin_h2h:
        order = [home, "Draw", away]
        odds = [pin_h2h[k]["price"] for k in order]
        pm, ov = multiplicative(odds)
        pp, k = power(odds)
        ps, z = shin(odds)
        print(f"\n  ANCRE SHARP Pinnacle 1X2 (overround {ov*100:.2f}%) — maj {pin_h2h_upd}")
        print(f"  {'issue':<10}{'cote':>7}{'mult.':>9}{'power':>9}{'Shin':>9}")
        for i, k_ in enumerate(order):
            print(f"  {k_:<10}{odds[i]:>7.2f}{pm[i]*100:>8.1f}%{pp[i]*100:>8.1f}%{ps[i]*100:>8.1f}%")
        # ECART_METHODES sur le favori (max proba)
        fav = max(range(3), key=lambda i: pm[i])
        ecart = abs(pm[fav] - pp[fav]) * 100
        print(f"  ECART_METHODES (sur {order[fav]}, mult vs power) = {ecart:.2f} pts")

        if bet_h2h:
            print(f"\n  CIBLE Betclic 1X2 — maj {bet_h2h_upd}")
            for i, k_ in enumerate(order):
                if k_ == "Draw":
                    continue  # le nul ne figure jamais dans la boîte (règle 3)
                cote_b = bet_h2h[k_]["price"]
                # base de proba = dévig power si favori lourd, sinon mult ; on montre les deux
                p_anchor = pp[i]
                e = ev_pct(p_anchor, cote_b)
                lo, hi = robustness(p_anchor, cote_b)
                seuil = max(ecart * cote_b, 2.0)  # marge liquidité plancher ~2%
                fair = 1.0 / p_anchor
                verdict = "🟢 candidate" if (e > seuil and lo > seuil and hi > seuil) else "🎲 (pas value)"
                print(f"   {k_:<9} Betclic={cote_b:.2f}  fair(ancre)={fair:.2f}  "
                      f"p_devig={p_anchor*100:.1f}%  EV={e:+.1f}%  seuil={seuil:.1f}%  "
                      f"±2pts=[{lo:+.1f}%,{hi:+.1f}%]  -> {verdict}")
        else:
            print("\n  CIBLE Betclic 1X2 : NON RENVOYÉE par l'API -> ⚠️/❌")

    if pin_t:
        print(f"\n  ANCRE SHARP Pinnacle TOTALS — maj (Pinnacle)")
        names = list(pin_t.keys())
        odds = [pin_t[n]["price"] for n in names]
        pts = pin_t[names[0]].get("point")
        pm, ov = multiplicative(odds)
        for i, n in enumerate(names):
            print(f"   {n} {pin_t[n].get('point')}: cote={odds[i]:.2f}  p_devig={pm[i]*100:.1f}%  (overround {ov*100:.2f}%)")
        if not bet_t:
            print("   CIBLE Betclic TOTALS : NON RENVOYÉE par l'API -> ⚠️ (ancre seule)")

def combine_two_winners(ev_a, ev_b, label):
    print("\n" + "=" * 72)
    print(f"COMBINÉ 2 VAINQUEURS INDÉPENDANTS — {label}")
    print("=" * 72)
    cote = ev_a["cote_betclic"] * ev_b["cote_betclic"]
    p = ev_a["p_devig"] * ev_b["p_devig"]
    print(f"  Cote combinée Betclic = {ev_a['cote_betclic']:.2f} × {ev_b['cote_betclic']:.2f} = {cote:.2f}")
    print(f"  Proba de toucher (p1×p2, base dévig unique) = "
          f"{ev_a['p_devig']*100:.1f}% × {ev_b['p_devig']*100:.1f}% = {p*100:.1f}%")
    print(f"  -> cote excitante {'OUI' if 2.0<=cote<=4.0 else 'NON'} (cible 2,0-4,0)  | EV = — (combiné plaisir assumé)")

if __name__ == "__main__":
    data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "today.json"))
    favs = {}
    for e in data:
        analyse(e)
        pin_h2h, _ = get_market(e, "pinnacle", "h2h")
        bet_h2h, _ = get_market(e, "betclic_fr", "h2h")
        if pin_h2h and bet_h2h:
            order = [e["home_team"], "Draw", e["away_team"]]
            odds = [pin_h2h[k]["price"] for k in order]
            pp, _ = power(odds)
            favs[e["home_team"]] = {"cote_betclic": bet_h2h[e["home_team"]]["price"],
                                    "p_devig": pp[0]}
    # combiné des deux favoris à domicile (indépendants)
    keys = list(favs)
    if len(keys) >= 2:
        combine_two_winners(favs[keys[0]], favs[keys[1]], f"{keys[0]} + {keys[1]} vainqueurs")
