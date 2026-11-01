import json, copy, collections
SRC = '/home/claude/sell-arch/spec.pre-coverage.bak.json'
OUT = '/home/claude/sell-arch/spec.json'
d = json.load(open(SRC))
C = {c['id']: c for L in d['layers'] for g in L['groups'] for c in g['components']}
G = {g['id']: g for L in d['layers'] for g in L['groups']}

def comp(i, name, does, ac, sor, calm, bian='', fix='', fpml='', iso='', mt='', regs=None):
    msg = '; '.join(x for x in [('FIX ' + fix.split(',')[0]) if fix else '', fpml, ('ISO 20022 ' + iso) if iso else '', mt] if x)
    return {"id": i, "name": name, "does": does, "ac": ac, "sor": sor, "external": False, "bian": bian,
            "msg": msg, "calm": calm, "fix": fix, "fpml_cdm": fpml, "iso20022": iso, "swift_mt": mt, "regs": regs or []}

NEW = [
 comp("C104", "Client Service Desk", "Handles client queries on trades, settlements and breaks as tracked cases with escalation", ["ALL"], "engagement", "service", bian="Customer Case Management"),
 comp("C105", "Client Statements and Reporting", "Issues trade, position and valuation statements and ex-post costs and charges reports to clients", ["ALL"], "engagement", "service", regs=["MiFID II costs and charges"]),
 comp("C106", "Voice and Sales-Trading", "Lets sales-traders work voice orders and quotes, capture client trades and log recorded calls", ["ALL"], "engagement", "webclient", bian="Dealer Desk", regs=["MiFID II recording of communications (Art 16(7))"]),
 comp("C107", "Term Sheet and Disclosures", "Generates term sheets, final terms and key information documents for structured products", ["DR", "EQ", "FI"], "engagement", "service", regs=["EU PRIIPs KID"]),
 comp("C108", "Quant Model Library", "Maintains approved pricing models, calibrations and analytics shared by pricing, risk and valuation", ["ALL"], "calculation", "service", bian="Quant Model"),
 comp("C109", "XVA Desk Pricing", "Prices CVA and FVA charges into client trades and hedges counterparty and funding risk", ["DR", "FX", "FI"], "calculation", "service"),
 comp("C110", "Clearing Broker Connectivity", "Manages clearing broker and FCM accounts, give-ins, statements and fees where not a member", ["DR", "FI", "EQ"], "integration", "service"),
 comp("C111", "Transaction and Derivative Taxes", "Calculates stamp duty, transaction taxes and dividend-equivalent withholding on trades and derivatives", ["EQ", "DR"], "calculation", "service", regs=["UK stamp duty and SDRT", "EU financial transaction taxes", "US IRC 871(m)"]),
 comp("C112", "Collateral Eligibility and Haircuts", "Holds eligibility schedules, haircuts, concentration limits and substitution rules per agreement", ["ALL"], "system of record", "database", fpml="CDM eligible collateral", regs=["UMR"]),
 comp("C113", "Funds Transfer Pricing", "Charges desks for funding, liquidity buffers and balance sheet used by tenor and currency", ["ALL"], "calculation", "service"),
 comp("C114", "Counterparty Credit Capital", "Calculates SA-CCR exposure at default and CVA capital by legal entity and netting set", ["ALL"], "calculation", "service", regs=["Basel SA-CCR", "Basel CVA risk framework"]),
 comp("C115", "Model Inventory and Validation", "Registers pricing and risk models, records independent validation, limitations and approval for use", ["ALL"], "control", "service", regs=["PRA SS1/23 model risk", "US SR 11-7"]),
 comp("C116", "Desk Profitability and Costs", "Allocates costs, funding and capital charges to desks and clients to show returns", ["ALL"], "calculation", "service", bian="Contribution Analysis"),
 comp("C117", "Workflow and Exception Management", "Routes breaks, exceptions and approvals to owners with ageing, escalation and audit trail", ["ALL"], "control", "service"),
]
for c in NEW: C[c['id']] = c

def grp(gid, name, stages, office, origin, cids):
    return {"id": gid, "name": name, "stages": stages, "office": office, "origin": origin,
            "components": [copy.deepcopy(C[i]) for i in cids]}
def keep(gid, cids, name=None, origin_add=''):
    g = G[gid]
    return grp(gid, name or g['name'], g['stages'], g['office'], g['origin'] + origin_add, cids)

PLAN = {
 "L1": [keep("G03", ["C08", "C09"]),
        keep("G01", ["C01", "C03"], origin_add=' (less C02)'),
        grp("G29", "KYC and Screening", ["S0"], "Middle", "S0/G01 (C02), split", ["C02"]),
        keep("G02", ["C04", "C05"], origin_add=' (less C06, C07)'),
        grp("G30", "Accounts and SSIs", ["S0"], "Middle", "S0/G02 (C06, C07), split", ["C06", "C07"]),
        grp("G31", "Client Service and Reporting", ["S1"], "Middle", "new (C104, C105)", ["C104", "C105"])],
 "L2": [keep("G04", ["C10", "C11", "C12"], origin_add=' (less C103)'),
        grp("G32", "Electronic Client Channels", ["S1"], "Front", "S1/G04 (C103), split", ["C103"]),
        grp("G33", "Voice and Sales-Trading", ["S1", "S2"], "Front", "new (C106)", ["C106"]),
        keep("G05", ["C13", "C107"], name="Structuring and Term Sheets", origin_add=' (less C14, C15) + new C107'),
        grp("G34", "Suitability and Product Governance", ["S1"], "Middle", "S1/G05 (C14, C15), split", ["C14", "C15"]),
        grp("G35", "Pricing Models and XVA", ["S1"], "Front", "new (C108, C109)", ["C108", "C109"])],
 "L3": [keep("G06", ["C16", "C18"], origin_add=' (less C17)'),
        grp("G36", "Pre-Trade Risk Controls", ["S2"], "Front", "S2/G06 (C17), split", ["C17"]),
        keep("G07", ["C19", "C20"], origin_add=' (less C21, C24)'),
        grp("G37", "Venue and Liquidity Access", ["S2"], "Front", "S2/G07 (C21) + S2/G08 (C24), split", ["C21", "C24"]),
        keep("G08", ["C22", "C23"]),
        keep("G09", ["C25", "C26"], origin_add=' (less C101)'),
        grp("G38", "Fees and Commissions", ["S3"], "Middle", "S3/G09 (C101), split", ["C101"])],
 "L4": [keep("G10", ["C27", "C28"]),
        keep("G11", ["C29", "C30", "C31"], origin_add=' (less C102)'),
        grp("G39", "Structured Products Lifecycle", ["S3"], "Middle", "S3/G11 (C102), split", ["C102"]),
        keep("G15", ["C40", "C41"], origin_add=' (less C42)'),
        grp("G40", "Client Clearing and FCMs", ["S5"], "Back", "S5/G15 (C42), split + new C110", ["C42", "C110"]),
        keep("G16", ["C43", "C44", "C45"])],
 "L5": [keep("G17", ["C46", "C47"], origin_add=' (less C48)'),
        grp("G41", "Fails, Penalties and Buy-ins", ["S6"], "Back", "S6/G17 (C48), split", ["C48"]),
        keep("G18", ["C49", "C50", "C51"]),
        keep("G20", ["C54", "C55", "C56"]),
        keep("G21", ["C57", "C58"], origin_add=' (less C59)'),
        grp("G42", "Tax and Withholding", ["S7"], "Back", "S7/G21 (C59), split + new C111", ["C59", "C111"])],
 "L6": [keep("G23", ["C62", "C64"], origin_add=' (less C63)'),
        grp("G43", "Synthetic Financing", ["S8"], "Front", "S8/G23 (C63), split", ["C63"]),
        keep("G22", ["C60", "C61"]),
        keep("G24", ["C65", "C67"]),
        keep("P3", ["C80", "C112"], name="Collateral Management", origin_add=' (less C81, C52) + new C112'),
        grp("G44", "Liquidity, Funding and Payments", ["PLATFORM"], "Cross-cutting", "PLATFORM/P3 (C81, C52), split + new C113", ["C81", "C113", "C52"])],
 "L7": [keep("G12", ["C32", "C33", "C116"], name="Risk, P&L and Profitability", origin_add=' (less C34) + new C116'),
        grp("G46", "Valuation and Model Control", ["S4"], "Middle", "S4/G12 (C34), split + new C115", ["C34", "C115"]),
        keep("P2", ["C77", "C78"], origin_add=' (less C79)'),
        grp("G45", "Counterparty Credit and XVA", ["PLATFORM"], "Cross-cutting", "PLATFORM/P2 (C79), split + new C114", ["C79", "C114"]),
        keep("G13", ["C35", "C36", "C37", "C66", "C91"]),
        keep("P6", ["C38", "C39", "C92", "C100"]),
        keep("G27", ["C90", "C94"])],
 "L8": [keep(g, [c['id'] for c in G[g]['components']]) for g in ["G25", "G26", "P1", "P4", "P5", "P7"]] +
       [keep("G28", ["C99", "C53", "C117"], name="Reconciliation and Exceptions", origin_add=' + new C117')],
}

for L in d['layers']:
    L['groups'] = PLAN[L['id']]
    st = []
    for g in L['groups']:
        for x in g['stages']:
            if x not in st: st.append(x)
    L['stages'] = st

CL = {c['id']: L['id'] for L in d['layers'] for g in L['groups'] for c in g['components']}
NEWLINKS = [
 ("C106", "C16", "voice orders entered", "", "Flow trade"),
 ("C109", "C10", "XVA charge added to quote", "", "Flow trade"),
 ("C40", "C110", "trades for broker clearing", "", "Flow trade"),
 ("C110", "X17", "trades given in for clearing", "FIX TradeCaptureReport", "Flow trade"),
 ("C111", "C26", "tax amounts for enrichment", "", "Flow trade"),
 ("C112", "C80", "eligibility and haircuts", "CDM eligible collateral", "Flow margin and collateral"),
 ("C25", "C105", "booked trades for statements", "", "Flow reporting"),
 ("C105", "X01", "statements and costs reports", "", "Flow reporting"),
 ("C79", "C114", "exposure profiles for capital", "", "Flow reporting"),
 ("C99", "C117", "breaks routed to owners", "", "Flow reporting"),
]
for f, t, lab, std, th in NEWLINKS:
    d['links'].append({"from": f, "to": t, "label": lab, "std": std, "thread": th,
                       "from_layer": CL.get(f, 'EXT'), "to_layer": CL.get(t, 'EXT')})

d['standards'] += [
 {"name": "EU PRIIPs key information document (KID) for packaged products", "used_for": "Term sheets and disclosure documents for structured products sold to retail distributors", "source_url": "", "verified": False, "layers": ["L2"]},
 {"name": "Transaction and withholding taxes: UK stamp duty and SDRT, EU national financial transaction taxes, US IRC Section 871(m)", "used_for": "Per-trade tax calculation and derivative dividend-equivalent withholding", "source_url": "", "verified": False, "layers": ["L5"]},
 {"name": "Model risk management: PRA SS1/23; US SR 11-7", "used_for": "Model inventory, independent validation and approval for use", "source_url": "", "verified": False, "layers": ["L7"]},
]
# extend layer lists of existing standards used by new components
for s in d['standards']:
    n = s['name']
    if n.startswith('MiFID II client categorisation') and 'L1' not in s['layers']: s['layers'].append('L1')
    if n.startswith('MiFID II recording of communications') and 'L2' not in s['layers']: s['layers'].append('L2')
    if n.startswith('Uncleared margin rules') and 'L6' not in s['layers']: s['layers'].append('L6')
    if n.startswith('FINOS Common Domain Model') and 'L6' not in s['layers']: s['layers'].append('L6')
    if n.startswith('BIAN') or n.startswith('FINOS CALM'): pass
    s['layers'] = sorted(set(s['layers']), key=lambda x: int(x[1:]))

d['assumptions'].append(
 "Coverage expansion (v4): to fill each slide row with 6 or 7 boxes, existing groups were split along functional seams and 14 components (C104 to C117) were added where a sell-side markets function was missing: client service and statements, voice sales-trading, term sheets, quant models and XVA pricing, clearing broker connectivity, transaction taxes, collateral eligibility, funds transfer pricing, counterparty credit capital, model validation, desk profitability and exception workflow. New components are analyst design and have not been reviewed.")

# xref matrix
comps = [c for L in d['layers'] for g in L['groups'] for c in g['components']]
def n(cs, f): return sum(1 for c in cs if c[f])
FMAP = {"BIAN": "bian", "FIX": "fix", "FpML_CDM": "fpml_cdm", "ISO20022": "iso20022", "SWIFT_MT": "swift_mt", "regs": "regs"}
FAMADD = {
 "L1": {"BIAN": " Customer Case Management for the client service desk (C104). No domain for client statements.",
        "other": " MiFID costs and charges on client statements (C105, unverified)."},
 "L2": {"BIAN": " Dealer Desk is closest fit for voice and sales-trading (C106); Quant Model for the model library (C108). No domain for term sheets or XVA pricing.",
        "FpML_CDM": " Term sheets and XVA pricing carry no message standard here.",
        "other": " EU PRIIPs KID and recording of communications (unverified)."},
 "L4": {"BIAN": " No domain for clearing broker connectivity (C110).",
        "other": " Clearing broker and FCM statements follow no common standard in this map."},
 "L5": {"BIAN": " No domain for transaction taxes (C111).",
        "other": " Stamp duty, SDRT, EU FTTs and US 871(m) (unverified)."},
 "L6": {"BIAN": " No domain for collateral eligibility schedules (C112) or funds transfer pricing (C113).",
        "FpML_CDM": " CDM eligible collateral also for eligibility schedules (C112)."},
 "L7": {"BIAN": " Contribution Analysis is closest fit for desk profitability (C116). No domain for counterparty credit capital or model validation.",
        "other": " PRA SS1/23 and SR 11-7 model risk (unverified)."},
 "L8": {"BIAN": " No domain for exception workflow (C117)."},
}
X = d['xref_matrix']
for r, L in zip(X['layers'], d['layers']):
    cs = [c for g in L['groups'] for c in g['components']]
    r['components'] = len(cs)
    r['groups'] = len(L['groups'])
    r['counts'] = {k: n(cs, f) for k, f in FMAP.items()}
    for k, v in FAMADD.get(L['id'], {}).items():
        if v.strip() not in r['families'].get(k, ''):
            r['families'][k] = r['families'].get(k, '') + v
cov = X['coverage']
cov['total_components'] = len(comps)
for k, f in FMAP.items(): cov[k]['matched'] = n(comps, f)
cov['CALM']['matched'] = n(comps, 'calm')
cov['CALM']['note'] = "Every component has a CALM 1.1 node type."
cov['total_groups'] = sum(len(L['groups']) for L in d['layers'])
bb = collections.OrderedDict()
for L in d['layers']:
    b = bb.setdefault(L['band'], {"layers": 0, "groups": 0, "components": 0})
    b['layers'] += 1; b['groups'] += len(L['groups']); b['components'] += sum(len(g['components']) for g in L['groups'])
cov['by_band'] = dict(bb)
cov['BIAN']['note'] = "All names copied from BIAN v10 value chain view; several are closest fit. New labels (C104, C106, C108, C116) rechecked against the same page."
newgaps = [
 "No BIAN domain for client statements, term sheets, XVA pricing, clearing broker connectivity, transaction taxes, collateral eligibility, funds transfer pricing, counterparty credit capital, model validation or exception workflow",
 "No common messaging standard for clearing broker and FCM statements or for term sheet and KID generation",
 "No data or messaging standard for funds transfer pricing, desk profitability, model inventories or exception workflow",
 "Transaction taxes and 871(m) withholding have tax law but no shared data standard",
]
for gp in newgaps:
    if gp not in cov['gaps']: cov['gaps'].append(gp)

for t in X['stage_traceability']:
    gl, ll = [], []
    for L in d['layers']:
        for g in L['groups']:
            if t['stage'] in g['stages']:
                gl.append(f"{L['id']}/{g['id']} {g['name']}")
                if L['id'] not in ll: ll.append(L['id'])
    t['groups'] = gl; t['layers'] = ll

json.dump(d, open(OUT, 'w'), indent=1, ensure_ascii=False)
print('written', len(comps), 'components', cov['total_groups'], 'groups', len(d['links']), 'links')
