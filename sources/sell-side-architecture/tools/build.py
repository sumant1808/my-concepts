import json, sys, copy
sys.path.insert(0, '/home/claude/sell-arch-tools')
from layout import BANDS, LAYERS, SERVES
SRC = '/home/claude/sell-arch/spec.stage-view.bak.json'
OUT = '/home/claude/sell-arch/spec.json'
d = json.load(open(SRC))
C = {}
OLD = {}  # component id -> old location
for s in d['stages']:
    for g in s['groups']:
        for c in g['components']:
            C[c['id']] = c; OLD[c['id']] = (s['id'], g['id'], g['name'])
for g in d['platform']['groups']:
    for c in g['components']:
        C[c['id']] = c; OLD[c['id']] = ('PLATFORM', g['id'], g['name'])

RENAME = {"G11": "OTC Confirmation and Lifecycle", "P6": "Surveillance and Control Room"}
layers = []; CL = {}; CG = {}
for lid, band, name, purpose, office, groups in LAYERS:
    gl = []; st = []
    for gid, gname, gst, goff, origin, cids in groups:
        gname = RENAME.get(gid, gname)
        gl.append({"id": gid, "name": gname, "stages": gst, "office": goff, "origin": origin,
                   "components": [copy.deepcopy(C[i]) for i in cids]})
        for x in gst:
            if x not in st: st.append(x)
        for i in cids: CL[i] = lid; CG[i] = gid
    L = {"id": lid, "band": band, "name": name, "purpose": purpose, "office": office,
         "stages": st, "groups": gl}
    if lid in SERVES: L["serves"] = SERVES[lid]
    layers.append(L)

# links: keep from/to, label, std, thread; add layer endpoints
links = []
for l in d['links']:
    n = dict(l)
    n['from_layer'] = CL.get(l['from'], 'EXT')
    n['to_layer'] = CL.get(l['to'], 'EXT')
    links.append(n)

EXT_LAYERS = {"X01":["L1","L2","L3"],"X02":["L3","L4"],"X03":["L2","L3"],"X04":["L4"],"X05":["L5"],
 "X06":["L5"],"X07":["L5"],"X08":["L8"],"X09":["L7"],"X10":["L7"],"X11":["L7"],"X12":["L8"],
 "X13":["L4"],"X14":["L6"],"X15":["L6"],"X16":["L5","L6"],"X17":["L4"],"X18":["L3"],"X19":["L7"],
 "X20":["L5"],"X21":["L5"]}
externals = []
for e in d['externals']:
    n = dict(e); n['layers'] = EXT_LAYERS[e['id']]; externals.append(n)

# standards: keep every field and flag; add 'layers' derived from component fields and tags
REGROW = {
 "US T+1 (SEC": ["US T+1"], "UK T+1 on": ["UK/EU T+1"],
 "EU T+1 on 11 October 2027 and CSDR": ["UK/EU T+1", "EU CSDR settlement discipline"],
 "EU T+1: Regulation": ["UK/EU T+1"], "MiFIR Article 26": ["MiFIR Art 26"],
 "UK MiFIR transaction": ["UK MiFIR"],
 "MiFID II / UK best execution": ["MiFID II best execution", "UK best execution (COBS 11.2A)"],
 "MiFIR / UK pre- and post-trade": ["MiFIR post-trade transparency", "MiFIR SI regime"],
 "EMIR Refit": ["EMIR Refit", "UK EMIR"],
 "EMIR timely confirmation": ["EMIR timely confirmation", "EMIR portfolio reconciliation", "EMIR clearing obligation", "EMIR client clearing"],
 "CFTC Part 45": ["CFTC Part 45", "Dodd-Frank counterparty status"],
 "CFTC Part 43": ["CFTC Part 43", "SEC Reg SBSR", "CFTC customer segregation"],
 "SFTR (ESMA)": ["SFTR", "UK SFTR", "SFTR Art 15 reuse"], "UK MAR Article 16": ["UK MAR Art 16"],
 "ISDA SIMM": ["ISDA SIMM"], "Uncleared margin rules": ["UMR", "UMR (CSA terms)", "CCP initial margin models"],
 "FCA operational resilience": ["FCA PS21/3"], "EU DORA": ["EU DORA"],
 "Client asset rules": ["FCA CASS", "SEC Rule 15c3-3"], "SEC Regulation SHO": ["Reg SHO", "EU/UK short selling rules"],
 "SEC Rule 15c3-5": ["SEC Rule 15c3-5", "MiFID II RTS 6"], "KYC and AML": ["UK MLRs", "EU AMLD", "US BSA/CIP"],
 "MiFID II client categorisation": ["MiFID II client categorisation", "MiFID II suitability and appropriateness", "MiFID II costs and charges"],
 "Basel trading book": ["Basel trading book (FRTB)", "Basel SA-CCR", "Basel CVA risk framework", "BCBS 239"],
 "US broker-dealer regimes": ["SEC CAT (Rule 613)", "FINRA TRACE", "SEC Rules 605/606", "Reg T", "FINRA Rule 4210", "SEC Rule 17a-4", "Volcker rule metrics"],
 "MiFID II recording of communications": ["MiFID II recording of communications (Art 16(7))", "MiFID II record keeping"],
 "UK MAR Articles 11 and 18": ["UK MAR Art 11 and 18", "EU MAR"],
}
COMPROW = {"CLS payment": ["C50"], "ISDA Master Agreement": ["C05", "C60", "C61"], "LEI (ISO 17442)": ["C74", "C75"],
           "ISDA Digital Regulatory": ["C36"], "Swift CBPR+": ["C52"], "UK bond consolidated tape": ["C37"]}
FIELDROW = {"BIAN Service": lambda c: c['bian'], "FINOS CALM": lambda c: c['calm'], "FIX Latest": lambda c: c['fix'],
            "FpML (ISDA)": lambda c: 'FpML' in c['fpml_cdm'], "FINOS Common Domain": lambda c: 'CDM' in c['fpml_cdm'],
            "ISO 20022 business areas": lambda c: c['iso20022'], "Swift securities": lambda c: c['swift_mt'],
            "Swift MT message numbers": lambda c: c['swift_mt']}
order = [L['id'] for L in layers]
allregs = {r for c in C.values() for r in c['regs']}
used = set()
standards = []
for s in d['standards']:
    n = dict(s); hit = set()
    for k, f in FIELDROW.items():
        if s['name'].startswith(k): hit |= {CL[i] for i, c in C.items() if f(c)}
    for k, tags in REGROW.items():
        if s['name'].startswith(k):
            used |= set(tags); hit |= {CL[i] for i, c in C.items() if set(c['regs']) & set(tags)}
    for k, ids in COMPROW.items():
        if s['name'].startswith(k): hit |= {CL[i] for i in ids}
    n['layers'] = [x for x in order if x in hit]
    standards.append(n)
assert allregs <= used, allregs - used
assert all(s['layers'] for s in standards), [s['name'] for s in standards if not s['layers']]

# xref matrix rows by layer
FAM = json.load(open('/home/claude/sell-arch-tools/families.json'))
def counts(cs):
    return {"BIAN": sum(1 for c in cs if c['bian']), "FIX": sum(1 for c in cs if c['fix']),
            "FpML_CDM": sum(1 for c in cs if c['fpml_cdm']), "ISO20022": sum(1 for c in cs if c['iso20022']),
            "SWIFT_MT": sum(1 for c in cs if c['swift_mt']), "regs": sum(1 for c in cs if c['regs'])}
rows = []
for L in layers:
    cs = [c for g in L['groups'] for c in g['components']]
    rows.append({"layer": L['id'], "band": L['band'], "name": L['name'], "components": len(cs),
                 "counts": counts(cs), "families": FAM[L['id']]})
allc = [c for L in layers for g in L['groups'] for c in g['components']]
cov = copy.deepcopy(d['xref_matrix']['coverage'])
tot = counts(allc)
cov['total_components'] = len(allc)
cov['BIAN']['matched'] = tot['BIAN']; cov['CALM']['matched'] = sum(1 for c in allc if c['calm'])
cov['FIX']['matched'] = tot['FIX']; cov['FpML_CDM']['matched'] = tot['FpML_CDM']
cov['ISO20022']['matched'] = tot['ISO20022']; cov['SWIFT_MT']['matched'] = tot['SWIFT_MT']; cov['regs']['matched'] = tot['regs']
cov['total_groups'] = sum(len(L['groups']) for L in layers); cov['total_layers'] = len(layers)
cov['by_band'] = {b['id']: {"layers": sum(1 for L in layers if L['band'] == b['id']),
                            "groups": sum(len(L['groups']) for L in layers if L['band'] == b['id']),
                            "components": sum(len(g['components']) for L in layers if L['band'] == b['id'] for g in L['groups'])} for b in BANDS}

# stage traceability
oldstage = {s['id']: s for s in d['stages']}
STNOTE = {
 "S0": "Pre-trade: onboarding, KYC, credit and documentation sit in L1 with sales coverage.",
 "S1": "Pre-trade: coverage moves to L1 beside onboarding; quoting, pricing and structuring form L2.",
 "S2": "Trade: order, execution and trading desk groups form L3; venue gateways now sit with routing.",
 "S3": "Split across bands: booking is a trade-date function in L3; allocation, confirmation and OTC lifecycle are post-trade in L4.",
 "S4": "Not a sequential step: risk, P&L and regulatory reporting run across the lifecycle in L7, which also takes SFTR reporting and the reporting control hub.",
 "S5": "Post-trade: clearing and margin sit in L4 with confirmation.",
 "S6": "Post-trade: settlement sits in L5 with custody.",
 "S7": "Post-trade: custody and asset servicing sit in L5; client money and assets oversight is a control in L7.",
 "S8": "Not a final step: financing and prime act on positions from trade date to settlement and beyond, so they form cross-lifecycle layer L6 with collateral, liquidity and cash; SFTR reporting moves to L7.",
 "S9": "Not a step at all: market data feeds every layer, so it sits in the common services layer L8.",
 "PLATFORM": "The former cross-cutting platform is split by purpose: risk and limits, surveillance, conduct and client assets join L7; collateral, liquidity and cash join L6; the rest form L8 common services.",
}
trace = []
for sid in [f"S{i}" for i in range(10)] + ["PLATFORM"]:
    gs = [(L['id'], g['id'], g['name']) for L in layers for g in L['groups']
          if any(OLD[c['id']][0] == sid for c in g['components'])]
    row = {"stage": sid, "name": oldstage[sid]['name'] if sid in oldstage else "Cross-cutting platform",
           "kind": {"S4": "cross-lifecycle", "S8": "cross-lifecycle", "S9": "common"}.get(sid, "platform" if sid == "PLATFORM" else "lifecycle"),
           "layers": sorted({x[0] for x in gs}, key=order.index),
           "groups": [f"{a}/{b} {c}" for a, b, c in gs], "note": STNOTE[sid]}
    if sid in oldstage:
        row["purpose_on_slide"] = oldstage[sid]['purpose']; row["value_on_slide"] = oldstage[sid]['value']
        row["office_on_slide"] = oldstage[sid]['office']
    trace.append(row)

A = list(d['assumptions'])
A[2] = ("The bank runs its own custody business (L5, owner stage S7), so custody components are internal; CSDs, ICSDs, CCPs, CLS, agent banks, "
        "trade repositories, triparty agents, data vendors and the messaging network are third-party run and appear as external parties. "
        "Four FMI touchpoints (C28, C41, C49, C50) are drawn inside their lifecycle layer (L4, L5) to show the flow; they are the same parties as X13, X04, X05 and X07.")
A[3] = ("The architecture is a functional layer view, read top to bottom from pre-trade to post-trade: three lifecycle bands (B1 to B3, five layers), "
        "one cross-lifecycle band (B4, two layers) and one common services band (B5, one layer). The owner's 10-stage Trade Flow Value Chain is kept only "
        "as a traceability tag ('stages') on every layer and group. A trade does not pass every lifecycle layer: FX skips custody, OTC uncleared skips CCP clearing, listed derivatives skip CSD settlement.")
A[6] = ("Regulatory reporting is produced and controlled in one cross-lifecycle layer, L7: G13 holds transaction, derivative, transparency and SFTR reporting (C35, C36, C37, C66) "
        "with the reporting control hub (C91). Surveillance and the control room (P6) and conduct and client assets oversight (G27) sit in L7 as second-line functions.")
A[11] = ("Office assignment is a convention; banks differ (for example some run prime services or clearing under Middle Office). Layer office is the dominant owner; "
         "each group keeps its own office from the stage view.")
A += [
 "Financing is not the last step of a trade. Securities lending, repo, prime margin lending and synthetic financing finance positions that already exist, from trade date to settlement and for as long as the position is held, and collateral, liquidity and cash serve margin (L4), settlement (L5) and financing alike. They form cross-lifecycle layer L6, not a stage after custody.",
 "Market data is not a step in the trade. Prices, curves and ticks are consumed by quoting (L2), execution and algos (L3), margin (L4), valuation and risk (L7) and surveillance (L7), so market data sits in common services (L8) beside reference data and is available to every layer.",
 "Risk, control and regulatory reporting are not a step between confirmation and clearing. Limits gate onboarding and pre-trade checks, reports are due at execution and on lifecycle events, and surveillance reads orders as well as trades, so they form cross-lifecycle layer L7.",
 "Reconciliation is a shared service (L8, G28): C99 reconciles front to back and against CCPs, clearing brokers, triparty agents and counterparties, and C53 reconciles nostros and depots, so both read from every lifecycle layer and from L6. OTC portfolio reconciliation (C30) stays in L4 because it is a bilateral confirmation duty with counterparties.",
 "The 'stages' tag on a group names where its content sits on the owner's current slides: S0 to S9 for the stage strip and PLATFORM for the cross-cutting platform strip. Each group also carries 'origin' (old stage or platform group).",
 "Slide fit: seven layer rows for the lifecycle and cross-lifecycle bands (L1 to L7), with common services (L8) drawn as one foundation strip beneath them, as the platform was before. L1 and L2 are kept apart, while L3 merges execution with trading and booking, L4 merges confirmation with clearing and L5 merges settlement with custody.",
 "Links, threads and component fields are unchanged; links gain from_layer and to_layer, externals gain layers, and standards gain the layers that use them. Verified and unverified flags are exactly as before.",
]

spec = {"title": "Sell-side global markets functional architecture (layered view, pre-trade to post-trade)",
        "bands": BANDS, "layers": layers, "links": links, "externals": externals, "standards": standards,
        "assumptions": A,
        "xref_matrix": {"layers": rows, "stage_traceability": trace, "coverage": cov}}
json.dump(spec, open(OUT, 'w'), indent=1, ensure_ascii=False)
json.dump({k: [list(v[:2]) + [v[2]] for v in [OLD[k]]][0] + [CL[k], CG[k]] for k in OLD}, open('/home/claude/sell-arch-tools/moves.json', 'w'))
print("written", len(allc), cov['total_groups'])
