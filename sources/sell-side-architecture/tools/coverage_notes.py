import json, re
d = json.load(open('/home/claude/sell-arch/spec.json'))
b = json.load(open('/home/claude/sell-arch/spec.pre-coverage.bak.json'))
old = {c['id'] for L in b['layers'] for g in L['groups'] for c in g['components']}
oldg = {g['id']: g for L in b['layers'] for g in L['groups']}
OFF = {L['id']: L['office'] for L in d['layers']}
# notes: bands table
rows = ["| Band | Layer | Office | Groups | Group count | Components | Traces to |", "|---|---|---|---|---|---|---|"]
bn = {x['id']: x['name'] for x in d['bands']}
for L in d['layers']:
    rows.append(f"| {L['band']} {bn[L['band']]} | {L['id']} {L['name']} | {L['office']} | " +
                ", ".join(f"{g['id']} {g['name']}" for g in L['groups']) +
                f" | {len(L['groups'])} | {sum(len(g['components']) for g in L['groups'])} | {', '.join(L['stages'])} |")
tr = ["| Owner stage | Now delivered by |", "|---|---|"]
for t in d['xref_matrix']['stage_traceability']:
    by = {}
    for x in t['groups']:
        l, rest = x.split('/', 1); by.setdefault(l, []).append(rest.split()[0])
    tr.append(f"| {t['stage']} {t['name']} | " + "; ".join(f"{l}: {', '.join(v)}" for l, v in by.items()) + " |")
n = open('/home/claude/sell-arch/notes.pre-coverage.bak.md').read()
n = re.sub(r"(## Bands and layers\n)(\|.*\n)+", lambda m: m.group(1) + "\n".join(rows) + "\n", n)
n = re.sub(r"(## Stage to layer traceability\n)(\|.*\n)+", lambda m: m.group(1) + "\n".join(tr) + "\n", n)
n = n.replace("- Shape: 5 bands, 8 layers, 33 groups, 100 components, 21 externals and 50 key flows in three threads (trade, margin and collateral, reporting). Components, links, externals and every cross-reference field are unchanged; only their grouping and placement moved.",
 "- Shape: 5 bands, 8 layers, 51 groups, 114 components, 21 externals and 60 key flows in three threads (trade, margin and collateral, reporting). The coverage expansion (v4, below) split groups and added 14 components (C104 to C117); the original 100 components keep every field.")
n = n.replace("- **CALM 1.1:** all 100 components", "- **CALM 1.1:** all 114 components")
SPLIT = [
 ("L1", "G01 Client Lifecycle", "C02 to new G29 KYC and Screening", "financial crime checks are run by a distinct team from onboarding orchestration"),
 ("L1", "G02 Credit and Documentation", "C06, C07 to new G30 Accounts and SSIs", "operational account and SSI set-up is separate from credit and legal terms"),
 ("L2", "G04 Quoting and Pricing", "C103 to new G32 Electronic Client Channels", "the client-facing e-channel is distinct from pricing engines"),
 ("L2", "G05 Structuring and Suitability", "C14, C15 to new G34 Suitability and Product Governance; G05 renamed Structuring and Term Sheets", "product governance is a control, structuring is a front-office build"),
 ("L3", "G06 Order Management", "C17 to new G36 Pre-Trade Risk Controls", "market-access controls are a regulated control in their own right"),
 ("L3", "G07 Execution and Routing", "C21, C24 to new G37 Venue and Liquidity Access", "connectivity and liquidity access are separate from routing and algo logic"),
 ("L3", "G09 Trade Capture and Booking", "C101 to new G38 Fees and Commissions", "fee capture and billing was flagged as hidden inside booking"),
 ("L4", "G11 OTC Confirmation and Lifecycle", "C102 to new G39 Structured Products Lifecycle", "issuance, fixings and autocalls are a distinct servicing line"),
 ("L4", "G15 CCP and Listed Clearing", "C42 to new G40 Client Clearing and FCMs", "client clearing and broker relationships differ from house CCP access"),
 ("L5", "G17 Settlement Processing", "C48 to new G41 Fails, Penalties and Buy-ins", "fails, CSDR penalties and buy-ins are a separate cost and control pool"),
 ("L5", "G21 Asset Servicing", "C59 to new G42 Tax and Withholding", "tax relief and transaction taxes form a distinct service"),
 ("L6", "G23 Prime Services", "C63 to new G43 Synthetic Financing", "synthetic prime and TRS run as a separate desk from cash prime"),
 ("L6", "P3 Collateral, Liquidity and Cash", "C81, C52 to new G44 Liquidity, Funding and Payments; P3 renamed Collateral Management", "collateral and treasury funding are different functions"),
 ("L7", "G12 Daily Risk and P&L", "C34 to new G46 Valuation and Model Control; G12 renamed Risk, P&L and Profitability", "independent valuation and model control are second-line functions"),
 ("L7", "P2 Risk and Limits", "C79 to new G45 Counterparty Credit and XVA", "XVA and counterparty credit capital were flagged as thin"),
 ("L8", "G28 Reconciliation Services", "renamed Reconciliation and Exceptions (gains C117)", "break workflow sits with reconciliation"),
]
WHY = {
 "C104": "client queries and break chasing had no owner on the client side",
 "C105": "trade, position and valuation statements and MiFID ex-post costs reports were missing",
 "C106": "voice and sales-trading support was flagged missing; complements the e-channel",
 "C107": "structured products need term sheets, final terms and KIDs before sale",
 "C108": "pricing, risk and IPV share a governed quant library",
 "C109": "XVA was only calculated after the trade; the desk prices and hedges it pre-deal",
 "C110": "where the bank is not a CCP member it clears through brokers and FCMs (X17)",
 "C111": "stamp duty, FTTs and 871(m) withholding are per-trade obligations",
 "C112": "collateral optimisation needs governed eligibility schedules and haircuts",
 "C113": "desk funding and liquidity charges drive trading profitability",
 "C114": "counterparty credit capital (SA-CCR, CVA capital) was flagged as thin",
 "C115": "model risk governance had no component",
 "C116": "desk and client profitability after costs, funding and capital was missing",
 "C117": "exceptions from reconciliation and operations need routed, aged workflow",
}
CL = {c['id']: (L['id'], g['id'], g['name'], c) for L in d['layers'] for g in L['groups'] for c in g['components']}
new = [i for i in CL if i not in old]
v4 = ["", "## Coverage expansion (v4)",
      "- Owner feedback: the one-page slide looked thin. Each layer row now holds 6 or 7 group boxes (L1 6, L2 6, L3 7, L4 6, L5 6, L6 6, L7 7, L8 7), up from 2 to 5 (L8 was already 7). Backups: spec.pre-coverage.bak.json, notes.pre-coverage.bak.md. Before and after table: coverage.md. Build and check: /home/claude/sell-arch-tools/coverage_build.py and validate_coverage.py (passes).",
      "- Method: split existing groups along functional seams first, then add components only for genuine sell-side gaps. 18 groups were created, 4 renamed, and 14 components added (100 to 114). Ten illustrative links were added (50 to 60); threads unchanged.",
      "", "### What was split", "| Layer | Old group | Change | Why |", "|---|---|---|---|"]
v4 += [f"| {a} | {b_} | {c} | {w} |" for a, b_, c, w in SPLIT]
v4 += ["", "### What was added", "| Id | Name | Layer and group | Why |", "|---|---|---|---|"]
v4 += [f"| {i} | {CL[i][3]['name']} | {CL[i][0]} {CL[i][1]} {CL[i][2]} | {WHY[i]} |" for i in new]
v4 += ["", "### Considered and not added",
       "- Already covered by existing components, so not duplicated: corporate actions (C57), fails and buy-ins (C48), fee billing (C101), client clearing (C42), XVA exposure (C79), collateral optimisation (C80), intraday liquidity (C81), limits and credit exposure (C77), market data entitlements and licences (C72), SSIs (C06), static data (C74, C75), trade reconstruction and records (C97), best execution and TCA (C90), P&L explain (C33).",
       "",
       "### Cross-references for new components",
       "- BIAN labels on new components, each found verbatim among the ServiceDomain labels of the v10 value chain view (fetched 1 November 2026): Customer Case Management (C104), Dealer Desk (C106, closest fit), Quant Model (C108) and Contribution Analysis (C116, closest fit). The other ten are blank.",
       "- No FIX, ISO 20022 or Swift MT fields were set on new components; C112 carries CDM eligible collateral. New regulation tags reuse existing rows (MiFID costs and charges, recording of communications, UMR, SA-CCR and CVA) or three new standards rows, all verified false: EU PRIIPs KID; UK stamp duty and SDRT, EU FTTs and US 871(m); PRA SS1/23 and SR 11-7.",
       "", "### Limitations of the expansion",
       "- The 14 new components, their links and the group splits are analyst design and have not been reviewed by the independent reviewer or a practitioner.",
       "- Eight groups hold one component (G29, G32, G33, G36, G38, G39, G41, G43). Each one's 'does' text supports two example lines, but they are the first candidates to merge if the slide has to shrink.",
       "- Group 'stages' tags on new groups are inferred: G31 Client Service and Reporting is tagged S1 and G33 Voice and Sales-Trading S1 and S2; G44 and G45 inherit PLATFORM from P3 and P2.",
       "- C114 Counterparty Credit Capital and C79 XVA and Counterparty Exposure share SA-CCR and CVA tags: C79 produces exposure, C114 turns it into capital.",
       ]
n = n.rstrip('\n') + "\n" + "\n".join(v4) + "\n"
open('/home/claude/sell-arch/notes.md', 'w').write(n)

# coverage.md
cv = ["# Coverage expansion: before and after", "",
      "Groups per layer row on the one-page slide (7 equal slots per row) and components per layer. Backup of the previous spec: spec.pre-coverage.bak.json.", "",
      "## Summary by layer", "| Layer | Groups before | Groups after | Components before | Components after | New components |", "|---|---|---|---|---|---|"]
for L, Lb in zip(d['layers'], b['layers']):
    cs = [c['id'] for g in L['groups'] for c in g['components']]
    cv.append(f"| {L['id']} {L['name']} | {len(Lb['groups'])} | {len(L['groups'])} | {sum(len(g['components']) for g in Lb['groups'])} | {len(cs)} | {', '.join(i for i in cs if i not in old) or 'none'} |")
cv.append(f"| Total | {sum(len(L['groups']) for L in b['layers'])} | {sum(len(L['groups']) for L in d['layers'])} | {len(old)} | {len(CL)} | {len(new)} |")
cv += ["", "## Groups and components after the expansion", "New = component added in this expansion (C104 to C117). Group status: kept, renamed or split (new group from an existing one), or new.", "",
       "| Layer | Group | Group status | Component | Name | New |", "|---|---|---|---|---|---|"]
REN = {"G05", "P3", "G12", "G28"}
for L in d['layers']:
    for g in L['groups']:
        if g['id'] in oldg:
            st = "renamed (was " + oldg[g['id']]['name'] + ")" if g['id'] in REN else ("kept" if [c['id'] for c in g['components']] == [c['id'] for c in oldg[g['id']]['components']] else "kept, lost or gained components")
        else:
            st = "new" if all(c['id'] not in old for c in g['components']) else "split"
        for c in g['components']:
            cv.append(f"| {L['id']} | {g['id']} {g['name']} | {st} | {c['id']} | {c['name']} | {'yes' if c['id'] not in old else ''} |")
open('/home/claude/sell-arch/coverage.md', 'w').write("\n".join(cv) + "\n")
print('ok')
