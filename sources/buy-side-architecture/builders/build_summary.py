import json, html, re
spec = json.load(open('/home/claude/am-arch/spec.json'))
OUT = '/home/claude/am-arch-canvas/project/Summary.dc.html'

LAYER_LABEL = {
 'L1': 'Clients and Distribution', 'L2': 'Investment Management', 'L3': 'Trading and Execution',
 'L4': 'Operations and Accounting', 'L5': 'Risk, Compliance and Regulatory', 'L6': 'Platform: Data, Finance and Controls'}
GROUP_LABEL = {
 'Client and Distributor Management': 'Clients and Distributors',
 'Onboarding and Agreements': 'Onboarding and Agreements',
 'Digital Channels': 'Digital Channels',
 'Client Reporting and Servicing': 'Reporting and Servicing',
 'Research and Insight': 'Research and Insight',
 'Portfolio Management': 'Portfolio Management',
 'Index and Replication (Passive)': 'Index and Replication',
 'Private Markets Deal Management (Alternatives)': 'Deal Management',
 'Portfolio Monitoring and Value Creation (Alternatives)': 'Portfolio Monitoring',
 'Stewardship': 'Stewardship',
 'Order Management': 'Order Management',
 'Execution and Best Execution': 'Execution and Best Execution',
 'ETF Primary Market (Passive)': 'ETF Primary Market',
 'Private Markets Transaction Execution (Alternatives)': 'Private Markets Execution',
 'Treasury, FX and Collateral': 'Treasury, FX and Collateral',
 'Trade Support and Settlement': 'Trade Support and Settlement',
 'Positions, Cash and Events': 'Positions and Cash',
 'Valuation and Performance': 'Valuation and Performance',
 'Fund Accounting and NAV': 'Fund Accounting and NAV',
 'Fund Dealing and Register': 'Dealing and Register',
 'Distribution Data and Platforms': 'Distribution Data',
 'Compliance Monitoring': 'Compliance Monitoring',
 'Conduct and Promotions': 'Conduct and Promotions',
 'Identity and Access': 'Identity and Access',
 'Private Fund Administration (Alternatives)': 'Private Fund Admin',
 'Product Governance': 'Product Governance',
 'Investment Risk': 'Investment Risk',
 'Financial Crime': 'Financial Crime',
 'Delegate Oversight': 'Delegate Oversight',
 'Regulatory and Sustainability Reporting': 'Regulatory and ESG Reporting',
 'Reference and Market Data': 'Reference and Market Data',
 'Data and Analytics': 'Data and Analytics',
 'Integration and Interoperability': 'Integration and APIs',
 'Controls, Records and Resilience': 'Controls and Resilience',
 'Enterprise Finance': 'Enterprise Finance'}
# R6: curated one-line summaries per group (two lines at box width; 192 px with 6 groups, 236 px with 5, 302 px with 4)
GROUP_EX = {
 'Client and Distributor Management': 'CRM, RFP and LP pipelines',
 'Onboarding and Agreements': 'Onboarding, mandates, LPAs',
 'Digital Channels': 'Client portal, LP portal, website',
 'Client Reporting and Servicing': 'Client and LP reports, complaints',
 'Research and Insight': 'Research, ESG data',
 'Portfolio Management': 'Portfolio system, optimiser, IBOR',
 'Index and Replication (Passive)': 'Index, rebalancing, tracking error',
 'Private Markets Deal Management (Alternatives)': 'Pipeline, diligence, IC',
 'Portfolio Monitoring and Value Creation (Alternatives)': 'Companies, loans, real assets',
 'Stewardship': 'Proxy voting, engagement',
 'Order Management': 'Order system, pre-trade checks',
 'Execution and Best Execution': 'Execution system, TCA',
 'ETF Primary Market (Passive)': 'Create/redeem, baskets, iNAV, APs',
 'Private Markets Transaction Execution (Alternatives)': 'Closing, exits, fund financing',
 'Treasury, FX and Collateral': 'FX, cash, collateral, lending',
 'Trade Support and Settlement': 'Capture, matching, settlement',
 'Positions, Cash and Events': 'ABOR, recs, events, CASS',
 'Valuation and Performance': 'Prices, private marks, performance',
 'Fund Accounting and NAV': 'NAV, swing pricing, fund statements',
 'Fund Dealing and Register': 'Unit dealing, register, box',
 'Distribution Data and Platforms': 'Target market and costs data',
 'Compliance Monitoring': 'Surveillance, post-trade checks',
 'Conduct and Promotions': 'Promotions, SM&CR register',
 'Identity and Access': 'Access, information barriers',
 'Private Fund Administration (Alternatives)': 'Partnership books, calls, carry, SPVs',
 'Product Governance': 'Product approval, value, disclosures',
 'Investment Risk': 'Market, liquidity, counterparty',
 'Financial Crime': 'KYC and sanctions screening',
 'Delegate Oversight': 'NAV, admin, TA, depositary checks',
 'Regulatory and Sustainability Reporting': 'Transaction, EMIR, AIFM, ESG returns',
 'Reference and Market Data': 'Security, party, market data',
 'Data and Analytics': 'Data platform, governance',
 'Integration and Interoperability': 'APIs, messaging, desktop links',
 'Controls, Records and Resilience': 'Records, resilience',
 'Enterprise Finance': 'Manager ledger, billing, capital'}
COMP_SHORT = {
 'Client CRM': 'Client CRM', 'Sales Pipeline and RFP': 'RFP pipeline', 'Fundraising and LP Pipeline': 'LP pipeline',
 'Client Onboarding Workflow': 'Onboarding', 'Mandate and Agreement Repository': 'Mandates',
 'Client and Adviser Portal': 'Client portal', 'LP Investor Portal': 'LP portal', 'Public Fund Website': 'Fund website',
 'Distributor Data Hub': 'Distributor data hub',
 'Client Reporting Engine': 'Client reports', 'LP Reporting Engine': 'LP reports', 'Client Case Management': 'Case handling',
 'Research Management': 'Research', 'ESG and Sustainability Data': 'ESG data',
 'Portfolio Management System': 'Portfolio system', 'Portfolio Optimiser': 'Optimiser', 'Investment Book of Record': 'IBOR',
 'Index Data Management': 'Index data', 'Replication and Rebalance Engine': 'Rebalancing', 'Tracking Error Analytics': 'Tracking error',
 'Deal Pipeline Management': 'Deal pipeline', 'Due Diligence Workspace': 'Due diligence', 'Deal Modelling and IC': 'Deal model and IC',
 'Portfolio Company Monitoring': 'Company monitoring', 'Loan and Covenant Monitoring': 'Covenants', 'Real Asset Management': 'Real assets',
 'Proxy Voting Platform': 'Proxy voting', 'Engagement Tracker': 'Engagement log',
 'Order Management System': 'Order system', 'Pre-Trade Compliance': 'Pre-trade checks',
 'Execution Management System': 'Execution system', 'TCA and Best Execution': 'TCA',
 'Creation and Redemption Platform': 'ETF creation', 'Basket (PCF) and iNAV Publication': 'Baskets and iNAV',
 'Deal Closing Management': 'Deal closing', 'Fund Financing Management': 'Fund financing',
 'FX and Cash Management': 'FX and cash', 'Collateral and Margin Management': 'Collateral', 'Securities Lending Programme Oversight': 'Lending oversight',
 'Trade Capture and Enrichment': 'Trade capture', 'Confirmation and Matching': 'Matching', 'Settlement and Fails Management': 'Settlement',
 'Accounting Book of Record': 'ABOR', 'Reconciliation Engine': 'Reconciliation', 'Corporate Actions and Income': 'Corporate actions',
 'Pricing and Valuation Control': 'Pricing', 'Illiquid Asset Valuation': 'Illiquid valuation', 'Performance and Attribution': 'Performance',
 'Fund Accounting and NAV': 'NAV', 'Transfer Agency and Register': 'Dealing and register',
 'Partnership Accounting': 'Partnership books', 'LP Register and Commitments': 'LP register', 'Capital Call and Distribution': 'Capital calls', 'Fee and Carry Engine': 'Fees and carry',
 'Corporate Finance and Billing': 'Manager finance',
 'Product Lifecycle and Approval': 'Product approval', 'Assessment of Value and Fair Value': 'Value assessment', 'Product Disclosure Documents': 'Disclosures',
 'Market and Liquidity Risk': 'Market and liquidity risk', 'Counterparty and Credit Exposure': 'Counterparty risk',
 'Post-Trade Compliance Monitor': 'Post-trade checks', 'Market Abuse Surveillance': 'Surveillance', 'Financial Promotions Approval': 'Promotions', 'Conduct and SM&CR Register': 'Conduct register',
 'KYC and Screening': 'KYC and sanctions',
 'Transaction Reporting': 'Transaction reports', 'Regulatory Returns Engine': 'Regulatory returns', 'Sustainability and Stewardship Reporting': 'ESG reports',
 'Security Master': 'Security master', 'Entity and Party Master': 'Party master', 'Market Data Distribution': 'Market data',
 'Enterprise Data Platform': 'Data platform', 'Data Governance and Lineage': 'Data governance',
 'Integration and API Gateway': 'API gateway', 'Financial Messaging Gateway': 'Messaging', 'Desktop Interoperability': 'Desktop links',
 'Identity and Access Management': 'Access control',
 'Document and Records Archive': 'Records archive', 'Operational Resilience Hub': 'Resilience', 'Third-Party Oversight': 'Third-party oversight',
 'NAV and Administrator Oversight': 'NAV oversight', 'Depositary and Trustee Liaison': 'Depositary liaison',
 'Box Management and Dealing Control': 'Box and dealing', 'Client Money and Assets (CASS)': 'Client money (CASS)',
 'Derivatives and SFT Reporting': 'EMIR and SFTR reports', 'Exit and Realisation Management': 'Exits', 'Legal Entity and SPV Management': 'Entity management',
 'Fund Investment Dealing and Look-Through': 'Fund-of-funds dealing', 'Restricted and Insider Lists': 'Insider lists', 'ETF Listing and AP Management': 'AP management'}

def union(comps):
    s = set()
    for c in comps:
        for x in c['seg']:
            s |= {'A','P','L'} if x == 'ALL' else {x}
    return s
def chips(s):
    return [] if s == {'A','P','L'} else [x for x in 'APL' if x in s]  # R22: no chip when shared by all three
assert all(c['name'] in COMP_SHORT for L in spec['layers'] for g in L['groups'] for c in g['components']), 'COMP_SHORT gap'
assert set(GROUP_EX) == set(GROUP_LABEL) == {g['name'] for L in spec['layers'] for g in L['groups']}

COLORS = dict(A='#1F4E8C', P='#0B6E70', L='#8A5600', All='#46546A')
TINT = {'P': ('#D3ECEC', '#0F8B8D'), 'L': ('#FAE6BF', '#8A5600'), 'A': ('#DCE8F7', '#1F4E8C')}
NAVY = '#0B1F3A'; INK = '#243553'

X0, GW, LBLW = 172, 1518, 140
SLOTS = 7  # one 7-column grid shared by all rows
ROW_H, ROW_GAP, Y0 = 144, 4, 108
def e(s): return html.escape(s, quote=True)

# functional clusters per row, in work-flow order; a thin divider separates clusters
CLUSTERS = {
 'L1': [['Client and Distributor Management', 'Onboarding and Agreements', 'Distribution Data and Platforms'], ['Digital Channels', 'Client Reporting and Servicing']],
 'L2': [['Research and Insight', 'Portfolio Management', 'Index and Replication (Passive)', 'Stewardship'],
        ['Private Markets Deal Management (Alternatives)', 'Portfolio Monitoring and Value Creation (Alternatives)']],
 'L3': [['Order Management', 'Execution and Best Execution', 'Treasury, FX and Collateral'],
        ['ETF Primary Market (Passive)', 'Private Markets Transaction Execution (Alternatives)']],
 'L4': [['Trade Support and Settlement', 'Positions, Cash and Events', 'Valuation and Performance'],
        ['Fund Accounting and NAV', 'Fund Dealing and Register', 'Private Fund Administration (Alternatives)']],
 'L5': [['Product Governance', 'Investment Risk', 'Compliance Monitoring', 'Conduct and Promotions', 'Financial Crime'],
        ['Delegate Oversight', 'Regulatory and Sustainability Reporting']],
 'L6': [['Reference and Market Data', 'Data and Analytics', 'Integration and Interoperability'],
        ['Identity and Access', 'Controls, Records and Resilience', 'Enterprise Finance']],
}
GAP = 10
els_bg, els = [], []
dashed_groups, tinted, labelmap = [], {}, []
for ri, L in enumerate(spec['layers']):
    y = Y0 + ri * (ROW_H + ROW_GAP)
    els.append(f'<div style="position: absolute; left: 24px; top: {y}px; width: {LBLW}px; height: {ROW_H}px; box-sizing: border-box; padding: 8px 6px; display: flex; align-items: center; background: {NAVY}; color: #FFFFFF; border-radius: 8px; font-size: 19px; line-height: 24px; font-weight: 700">{e(LAYER_LABEL[L["id"]])}</div>')
    n = len(L['groups']); cl = CLUSTERS[L['id']]
    assert n <= SLOTS and sorted(sum(cl, [])) == sorted(g['name'] for g in L['groups']), (L['id'], n)
    w = (GW - GAP * (SLOTS - 1)) // SLOTS
    byname = {g['name']: g for g in L['groups']}
    slot = 0
    for ci, names in enumerate(cl):
      if ci:
        els.append(f'<div style="position: absolute; left: {X0 + slot * (w + GAP) - GAP // 2 - 1}px; top: {y + 8}px; width: 2px; height: {ROW_H - 16}px; background: #8795AB"></div>')
      for gname in names:
        g = byname[gname]
        x = X0 + slot * (w + GAP); slot += 1
        u = union(g['components']); cs = chips(u)
        ext = sum(1 for c in g['components'] if c['external']) * 2 > len(g['components'])
        label = GROUP_LABEL[g['name']]
        labelmap.append((L['id'], g['name'], label, ''.join(cs), GROUP_EX[g['name']], ext))
        if ext: dashed_groups.append(label)
        tint = None
        if len(u) == 1:
            tint = list(u)[0]; tinted.setdefault(tint, []).append(label)
        bg, bd = TINT[tint] if tint else ('#FFFFFF', '#8795AB')
        style = 'dashed' if ext else 'solid'
        chip_html = ''.join(f'<span style="display: inline-block; margin-right: 6px; padding: 0 7px; border-radius: 4px; background: {COLORS[c]}; color: #FFFFFF; font-size: 18px; line-height: 24px; font-weight: 700">{c}</span>' for c in cs)
        els.append(f'<div style="position: absolute; left: {x}px; top: {y}px; width: {w}px; height: {ROW_H}px; box-sizing: border-box; padding: 6px 8px; background: {bg}; border: 2px {style} {bd}; border-radius: 8px; color: {NAVY}">'
                   f'<b style="display: block; height: 52px; overflow: hidden; font-size: 22px; line-height: 26px; font-weight: 700">{e(label)}</b>'
                   f'<span style="display: block; height: 42px; overflow: hidden; font-size: 18px; line-height: 21px; color: {INK}">{e(GROUP_EX[g["name"]])}</span>'
                   f'<span style="display: block; margin-top: 2px; height: 24px">{chip_html}</span></div>')

# external strips
ext_by_id = {x['id']: x for x in spec['externals']}
STRIPS = [
 ('right', 'Markets and counterparties', ['X04', 'X05', 'X12', 'X18', 'X13'], 0, 3,
  ['Brokers and trading venues', 'Authorised participants, market makers', 'Banks, prime brokers, lenders', 'Clearing brokers and CCPs', 'Deal advisers, portfolio companies']),
 ('right', 'Service providers', ['X06', 'X16', 'X07', 'X17', 'X08', 'X09', 'X10', 'X11'], 3, 3,
  ['Custodian', 'Depositary or trustee', 'Administrator, transfer agent', 'Independent valuers', 'Index providers', 'Data and ESG vendors', 'Proxy advisers', 'Securities lending agent']),
]
used_ids = sorted(i for s in STRIPS for i in s[2])
OMITTED = sorted(set(ext_by_id) - set(used_ids))  # left-hand stakeholder strips removed on the one-pager by owner instruction
assert OMITTED == ['X01', 'X02', 'X03', 'X14', 'X15', 'X19'], OMITTED
for side, title, ids, r0, span, items in STRIPS:
    x = 24 if side == 'left' else 1704
    y = Y0 + r0 * (ROW_H + ROW_GAP); h = span * ROW_H + (span - 1) * ROW_GAP
    body = ''.join(f'<span style="display: block; margin-top: 6px">{e(t)}</span>' for t in items)
    els.append(f'<div style="position: absolute; left: {x}px; top: {y}px; width: 192px; height: {h}px; box-sizing: border-box; padding: 10px 10px; background: #E1E7F0; border: 2px solid #5B6B85; border-radius: 8px; color: {NAVY}">'
              f'<b style="display: block; font-size: 22px; line-height: 26px; font-weight: 700">{e(title)}</b>'
              f'<span style="display: block; font-size: 18px; line-height: 22px; color: {INK}">{body}</span></div>')

def chip(c): return f'<span style="display: inline-block; margin-right: 8px; padding: 0 7px; border-radius: 4px; background: {COLORS[c]}; color: #FFFFFF; font-size: 18px; line-height: 24px; font-weight: 700">{c}</span>'
def sw(bg, bd, st='solid'): return f'<span style="display: inline-block; vertical-align: middle; margin-right: 8px; width: 30px; height: 20px; box-sizing: border-box; background: {bg}; border: 2px {st} {bd}; border-radius: 4px"></span>'
LEGW = [
 (chip('A') + 'Active', 130), (chip('P') + 'Passive/ETF', 190), (chip('L') + 'Alternatives', 190),
 ('No letter: shared by all three', 310),
 (sw(*TINT['P']) + 'Passive only', 180), (sw(*TINT['L']) + 'Alternatives only', 240),
 (sw('#FFFFFF', '#8795AB', 'dashed') + 'Mostly third-party run', 290)]
leg = []; _x = 24
for inner, w in LEGW:
    leg.append((_x, w, inner)); _x += w + 24
assert _x - 24 <= 1896, _x
for x, w, inner in leg:
    els.append(f'<div style="position: absolute; left: {x}px; top: 1010px; width: {w}px; height: 28px; font-size: 18px; line-height: 28px; color: {NAVY}; white-space: nowrap">{inner}</div>')
NCOMP = sum(len(g['components']) for L in spec['layers'] for g in L['groups'])
els.append(f'<div style="position: absolute; left: 24px; top: 1046px; width: 1872px; height: 24px; font-size: 18px; line-height: 24px; color: #3A4A63; white-space: nowrap">Draft, analyst design, AI-reviewed, not practitioner-validated. Inputs: BIAN labels, CALM vocabulary, ISO 20022, FIX, ILPA. Detailed {NCOMP}-component view available.</div>')

head = f'''<div style="position: absolute; left: 0px; top: 0px; width: 1920px; height: 96px; background: {NAVY}"></div>
<div style="position: absolute; left: 0px; top: 96px; width: 960px; height: 4px; background: #0F8B8D"></div>
<div style="position: absolute; left: 960px; top: 96px; width: 960px; height: 4px; background: #C27C00"></div>
<h1 style="position: absolute; left: 24px; top: 8px; width: 1872px; height: 54px; margin: 0; font-family: 'Fraunces', Georgia, serif; font-size: 42px; line-height: 54px; font-weight: 600; color: #FFFFFF; white-space: nowrap">One operating backbone, three investment engines</h1>
<div style="position: absolute; left: 24px; top: 62px; width: 1872px; height: 28px; font-size: 22px; line-height: 28px; color: #D5DFEE; white-space: nowrap">UK buy-side functional architecture: one architecture for Active, Passive/ETF and Alternatives</div>
'''
doc = f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>UK buy-side asset manager: functional architecture, one page</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&amp;family=Fraunces:wght@600&amp;display=swap">
<style>
body{{margin:0}}
</style>
</helmet>
<div style="position: relative; width: 1920px; height: 1080px; background: #F4F6F9; font-family: 'DM Sans', system-ui, sans-serif; overflow: hidden">
{head}{chr(10).join(els)}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1920,"height":1080}}}}'>
class Component extends DCLogic {{
renderVals() {{
return {{}};
}}
}}
</script>
</body>
</html>
'''
open(OUT, 'w').write(doc)
for r in labelmap: print(*r, sep=' | ')
print('groups per row:', [len(L['groups']) for L in spec['layers']])
print('dashed:', dashed_groups); print('tinted:', {k: len(v) for k, v in tinted.items()})
