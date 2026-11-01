# Independent review: UK buy-side asset manager functional architecture

Reviewer role: enterprise architect with buy-side asset management and capital markets operations experience, UK context.
Scope reviewed: `am-arch/spec.json`, `am-arch/notes.md`, `am-arch-canvas/project/Main.dc.html` (2400x5654), `am-arch-canvas/project/Summary.dc.html` (1920x1080), `am-arch-canvas/build_summary.py`, `am-arch-canvas/build.py` (read for geometry), and `am-chain/active.json`, `passive.json`, `alts.json` for scope. Source and data were reviewed. Nothing was rendered.

## Reviewer assumptions
1. The audience is a UK authorised fund manager (AFM/ACD) plus UK AIFM, as the spec says. A pitch audience is COO, CTO, Head of Operations or Head of Change.
2. Text fit was estimated with Inter Regular and Inter or Inter Display Bold as a stand-in for DM Sans, because DM Sans is not installed. Inter is a little wider, so the estimates lean safe. A fit marked OK is very likely OK. A fit marked tight needs checking in the canvas.
3. "Fixes" are written against `spec.json` and the two builder scripts. The `.dc.html` files are generated, so re-run `build.py` and then `build_summary.py` after any spec change. See R27 on the canvas.json overwrite.
4. Statements marked (reviewer knowledge) are mine and were not verified in this review. Statements marked (checked) were confirmed against a source listed at the end.
5. "Client-facing" means the Summary slide is shown on screen and the detailed board may be handed out or shown zoomed.

## Overall verdict in one line
The structure is sound and unusually honest: the six-layer logic, segment tagging, the IBOR/ABOR split and the "standards as inputs" stance are all right. It is not yet pitch-ready. Two things would get it challenged in the first five minutes by a UK operations audience. First, it outsources NAV, TA and administration but has almost no manager-side oversight capability (NAV oversight, depositary, box, client money). Second, the two views use opposite colours for Active and Passive.

---

## Critical

### R1. Critical. Manager-side oversight of outsourced fund administration is missing
- Where: spec.json L4 "Fund Accounting and Transfer Agency" (C49, C50 are external=true), L4 "Private Fund Administration" (C51-C53 external=true), C43 external=true, and L6 C80 "Third-Party Oversight". The summary marks both administration groups dashed ("Mostly third-party run").
- What is wrong: the drawing tells the client that NAV, register and private fund books sit with a third party. The only thing it shows the manager keeping is one generic vendor-oversight card, and that card sits in the Platform layer. A UK AFM/ACD keeps regulatory responsibility for NAV accuracy, pricing errors, dealing, the box and depositary relationships. The value chains name this activity: active.json "Oversee the depositary and administrator", passive.json "Investigate and sign off NAV exceptions", alts.json "Oversee administrator and depositary-lite controls". No component delivers it. This is the first question an outsourced-model client will ask.
- Evidence: there is no component whose `does` mentions NAV oversight, shadow NAV, NAV error, pricing error, depositary or box. C80 `does` = "Oversees administrator, custodian, TA and vendor performance and exits", which covers commercial and SLA oversight only.
- FIX:
  1. Add an L5 group named "Delegate Oversight" (summary label "Delegate Oversight". "Delegate and Third-Party Oversight" wraps to 3 lines at 192 px).
  2. Add C81: `{"id":"C81","name":"NAV and Administrator Oversight","does":"Exception-based or shadow NAV checks, NAV and pricing error handling, TA and administrator KPI review, sign-off evidence","seg":["ALL"],"sor":"control","external":false,"bian":"","msg":"","calm":"service"}`.
  3. Add C82: `{"id":"C82","name":"Depositary and Trustee Liaison","does":"Manages depositary oversight queries, cash-monitoring breaks, unit issue/cancellation confirmations and breach reporting","seg":["ALL"],"sor":"control","external":false,"bian":"","msg":"","calm":"service"}`.
  4. Move C80 from L6 "Controls, Records and Resilience" into this new L5 group. Leave C79 in L6.
  5. Add link `{"from":"C49","to":"C81","label":"NAV and exception pack","std":""}`.
  6. Notes, external=true bullet: change "through L6 Third-Party Oversight" to "through L5 Delegate Oversight (C80-C82)".

### R2. Critical. Segment colours are inverted between the detailed and one-page views
- Where: build.py `SEGC={'A':'#0B6E70','P':'#1F4E8C',...}` and `CARDT`/`GRPT` (Active = teal, Passive = blue). build_summary.py `COLORS = dict(A='#0B1F3A', P='#0B6E70', ...)` and `TINT['P']=('#D3ECEC','#0F8B8D')` (Active = navy, Passive = teal).
- What is wrong: teal means Active on the detailed board and Passive on the slide. When both appear in the same deck, the client reads the wrong segment. On the slide the A chip (#0B1F3A) is also the same navy as the title bar and layer labels, so it reads as structure, not as a segment.
- FIX: use one palette in both builders. Recommended: A = `#1F4E8C` (blue), P = `#0B6E70` (teal), L = `#8A5600` (amber), All = `#46546A`. In build.py set `SEGC={'A':'#1F4E8C','P':'#0B6E70','L':'#8A5700','ALL':'#3A4556'}`, `CARDT={'A':'#DCE8F7','P':'#D9F0EC','L':'#FAE8C6'}` and `GRPT={'A':'#C5D8F0','P':'#BFE3DD','L':'#F2D9A6'}`. Change the legend rows to "Pale blue fill: Active-only" and "Pale teal fill: Passive and ETF only". In build_summary.py set `COLORS['A']='#1F4E8C'` and `TINT['A']=('#DCE8F7','#1F4E8C')`. Both blue and teal on white pass 4.5:1 for 18 px bold chip text (teal 6.0:1, checked by calculation).

---

## High

### R3. High. UK authorised-fund dealing mechanics and client money are absent
- Where: L4 "Fund Accounting and Transfer Agency" and L4 "Positions, Cash and Events". The value chain asks for this in active.json "Process investor dealing and register".
- What is wrong: three things a UK AFM audience expects to see are missing (reviewer knowledge): (a) box management and dealing as principal, often kept in-house even when the TA is outsourced; (b) client money and custody asset protection (CASS) for dealing flows and segregated mandates; (c) liquidity management tools (swing pricing, dilution levy, deferral and suspension). The task brief names client money explicitly.
- FIX:
  1. Add C83 to "Fund Accounting and Transfer Agency": `{"id":"C83","name":"Box Management and Dealing Control","does":"Manages the manager's box, dealing as principal, daily unit creation and cancellation instructions, and dealing errors","seg":["A","P"],"sor":"system of record","external":false,"bian":"","msg":"","calm":"system"}`.
  2. Add C84 to "Positions, Cash and Events": `{"id":"C84","name":"Client Money and Assets (CASS)","does":"Client money and custody asset records, daily internal and external reconciliations, DvP exemption tracking, resolution pack and regulatory return","seg":["A","P"],"sor":"control","external":false,"bian":"","msg":"","calm":"service"}`.
  3. Change C49 `does` to "Calculates daily NAV, fee accruals, swing pricing or dilution adjustments, and fund financial statements".
  4. Change C59 `does` to "Computes VaR, stress tests, exposures, leverage, liquidity risk and liquidity-tool triggers".
  5. Add "CASS (client assets)" to standards with `verified:false`.

### R4. High. Derivatives and securities financing reporting, plus exchange-traded margin, are missing
- Where: C66 `does` = "...regulatory transaction reports for listed trades". C38 `does` = "...for OTC derivatives". C39. There is no trade-repository or CCP external.
- What is wrong: the scope includes hedging overlays, share-class FX hedging, futures overlay ("Manage cash and futures overlay" in passive.json) and securities lending. Those trigger UK EMIR derivative reporting and SFTR reporting (reviewer knowledge). Neither appears. Futures need clearing-broker margin, which "OTC derivatives" excludes. MiFIR reports normally go through an approved reporting mechanism (ARM), not straight to "Regulators".
- FIX:
  1. Add C85 to L5 "Regulatory and Sustainability Reporting": `{"id":"C85","name":"Derivatives and SFT Reporting","does":"Generates and reconciles UK EMIR derivative and SFTR securities-financing reports to trade repositories","seg":["ALL"],"sor":"control","external":false,"bian":"","msg":"","calm":"service"}`.
  2. Change C38 `does` to "Calculates margin, eligible collateral and haircuts for OTC and exchange-traded derivatives".
  3. Add externals `X18 {"name":"Clearing brokers and CCPs","role":"Clear futures and cleared OTC derivatives; call initial and variation margin"}` and `X19 {"name":"Trade repositories and ARMs","role":"Receive EMIR, SFTR and MiFIR transaction reports"}`.
  4. Add links C66→X19 "transaction reports" and C85→X19 "derivative and SFT reports".
  5. Add "UK EMIR and SFTR reporting" to standards with `verified:false`.

### R5. High. The Alternatives exit stage and fund/SPV entity management have no component
- Where: L3 "Private Markets Transaction Execution" (C35, C36). The alts.json block "Exit & Realisation" has 8 activities. "Design fund structure and domiciles" sits in ALT-B1.
- What is wrong: C35 covers acquisition closing only. Sale processes, escrows, earn-outs and proceeds allocation have no home, so the notes' claim that every block maps to at least one component does not hold. A PE/infra house runs dozens to hundreds of GP, feeder and SPV entities, and entity management is a standard platform for that.
- FIX:
  1. Add C86 to L3 "Private Markets Transaction Execution": `{"id":"C86","name":"Exit and Realisation Management","does":"Runs sale processes, vendor diligence, completion proceeds, escrows, earn-outs and warranty claims","seg":["L"],"sor":"engagement","external":false,"bian":"","msg":"","calm":"system"}`.
  2. Add C87 to L4 "Private Fund Administration": `{"id":"C87","name":"Legal Entity and SPV Management","does":"Holds fund, GP, feeder and SPV structures, directors, filings and entity governance calendar","seg":["L"],"sor":"system of record","external":false,"bian":"Legal Entity Directory","msg":"LEI (ISO 17442)","calm":"database"}`.
  3. Add external `X17 {"name":"Independent valuers","role":"Provide or review private asset valuations"}` and link X17→C47 "valuation reports".

### R6. High. The one-page examples silently drop the components a client looks for first
- Where: build_summary.py `examples(comps, budget)` takes the first 3 short names that fit 33 or 44 characters.
- What is wrong: the truncation removes Settlement (Trade Support and Settlement shows only "Trade capture, Matching", though the group title says Settlement), Investment book/IBOR, Tracking error, IC, Real assets, Corporate actions, Attribution/performance, Capital calls, Fees and carry, the SM&CR conduct register and ESG reports. The slide therefore under-sells precisely the points of differentiation: IBOR, carry and TE.
- Evidence: label map output from build_summary.py logic, for example "Private Fund Admin | Partnership books, LP register" and "Compliance and Surveillance | Post-trade checks, Surveillance, Promotions".
- FIX: replace `examples(...)` with a hand-curated dict `GROUP_EX`. All strings below were measured to fit 2 lines at the stated widths (192 px when a layer has 6 groups, 236 px when it has 5):
  Clients and Distributors "CRM, RFP and LP pipelines"; Onboarding "Onboarding, mandates, LPAs"; Digital Channels "Client portal, LP portal, website"; Distribution Data "Target market and costs data"; Reporting "Client and LP reports, complaints"; Research "Research, ESG data"; Portfolio Management "Portfolio system, optimiser, IBOR"; Index "Index, rebalancing, tracking error"; Deal Management "Pipeline, diligence, IC"; Portfolio Monitoring "Companies, loans, real assets"; Stewardship "Proxy voting, engagement"; Order Management "Order system, pre-trade checks"; Execution "Execution system, TCA"; ETF Primary "Create/redeem, baskets, iNAV"; PM Execution "Closing, exits, fund financing"; Treasury "FX, cash, collateral, lending"; Trade Support "Capture, matching, settlement"; Positions "ABOR, recs, events, CASS"; Valuation "Prices, private marks, performance"; Fund Accounting and TA "NAV, dealing, register, box"; Private Fund Admin "Partnership books, calls, carry"; Finance "Manager ledger, fee billing"; Product Governance "Product approval, value, disclosures"; Investment Risk "Market, liquidity, counterparty"; Compliance "Mandate, abuse, promotions, SM&CR"; Financial Crime "KYC, sanctions, insider lists"; Delegate Oversight "NAV, admin, TA, depositary checks"; Regulatory Reporting "Transaction, EMIR, AIFM, ESG returns"; Reference Data "Security, party, market data"; Data "Data platform, governance"; Integration "APIs, messaging, desktop"; Identity "Access, information barriers"; Controls "Records, resilience".

### R7. High. Several short labels change the meaning of their component
- Where: build_summary.py `COMP_SHORT` (it also drives the R6 examples if kept).
- What is wrong and FIX (change the value):
  - "Corporate Finance and Billing" → "Invoicing" hides the manager ledger and regulatory capital. Use "Manager finance".
  - "Performance and Attribution" → "Attribution" drops returns, IRR and composites. Use "Performance".
  - "Transfer Agency and Register" → "Register" drops dealing, the core TA function. Use "Dealing and register".
  - "Securities Lending Oversight" → "Stock lending" implies the manager runs the lending programme. Use "Lending oversight".
  - "Market and Liquidity Risk" → "Market risk" drops liquidity, the most scrutinised UK fund risk. Use "Market and liquidity risk".
  - "Deal Modelling and IC" → "IC papers" understates it. Use "Deal model and IC".
  - "Investment Book of Record" → "Investment book" and "Accounting Book of Record" → "Accounting book": buy-side clients use the acronyms. Use "IBOR" and "ABOR".
  - "Data Governance and Lineage" → "Lineage". Use "Data governance".
  - "Basket and iNAV Publication" → "iNAV". Use "Baskets and iNAV".
  - "KYC and Screening" → "KYC checks". Use "KYC and sanctions".

### R8. High. The detailed board carries internal-only wording, and seven mainstream UK rules are still "Not verified"
- Where: Main.dc.html header chip "Draft · analyst design · not independently reviewed". Honesty panel bullet 2: "...Check them before showing this to a client." spec.json standards entries with `verified:false` (Consumer Duty, SM&CR, UK UCITS/COLL, UK AIFM, UK MiFIR, FATCA/CRS, operational resilience).
- What is wrong: the honesty is right for an internal draft. But this board is meant for pitches, and an instruction to oneself not to show it to clients, printed on the deliverable, would embarrass the owner. These seven regimes are well-established and quick to source (FCA Handbook PRIN 2A, SYSC 24-27, COLL, FUND, SUP 17A, SYSC 15A).
- FIX:
  1. Verify each regime against the FCA Handbook and set `verified:true` with a `source_url`.
  2. In build.py `lims[1]`, replace the bullet with "UK regulatory references are to the FCA Handbook as at <date>; mapping of rules to components is indicative, not legal advice."
  3. Replace `chip_txt` with "Illustrative reference architecture · <month year>".
  4. Keep the current wording only in an internal copy.

### R9. High. Custodian and depositary are merged into one external party
- Where: spec.json X06 "Custodian and depositary". Summary strip text "Custodian, depositary".
- What is wrong: the depositary (trustee for unit trusts) is a separate regulated oversight role with cash-monitoring and oversight duties over the manager. The custodian is a service provider. They are often the same group but a different legal role (reviewer knowledge). For closed-ended AIFs the depositary may be a "depositary-lite" or PE depositary with no custody at all (alts.json names this). Merging them hides the R1 oversight relationship.
- FIX:
  1. Rename X06 to "Custodian" with role "Safekeeps assets, settles trades, reports holdings and events".
  2. Add `X16 {"name":"Depositary or trustee","role":"Independent oversight of the fund, cash monitoring and safekeeping duties"}`.
  3. Add link X16→C82 "oversight queries and breaches".
  4. Put X16 in the build.py RIGHT list next to X06 at layer L4. In build_summary.py, Service providers items, change 'Custodian, depositary' to 'Custodian' and add 'Depositary or trustee'.

---

## Medium

### R10. Medium. C39 is flagged third-party run, but it describes the manager's own oversight
- Where: C39 "Securities Lending Oversight", `external:true`, `sor:"control"`.
- What is wrong: the lending is done by X11. The oversight of it (fee split, borrower limits, recalls for votes) is the manager's own job.
- FIX: set C39 `external:false`. Optionally rename it "Securities Lending Programme Oversight".

### R11. Medium. Wrong segment tags
- Where and FIX:
  - C57 "Value and Outcomes Assessment" `seg:["ALL"]` → `["A","P"]`. The assessment of value and Consumer Duty fair value apply to authorised and retail products. Professional-only closed-ended private funds are largely outside them (reviewer knowledge). Rename it "Assessment of Value and Fair Value".
  - C61 "Post-Trade Compliance Monitor" `["A","P"]` → `["ALL"]`. LPA investment restrictions (concentration, leverage, borrowing limits) need monitoring too.
  - C12 `does` "Logs queries, complaints and outcomes as Consumer Duty evidence" → "Logs queries, complaints and outcomes (Consumer Duty evidence for retail products)".
  - C17 IBOR `["A","P"]`: keep, but add a notes line saying Alternatives positions are held in C24-C26 and C51, and that a total-portfolio view comes from C72.

### R12. Medium. A group name contradicts its own segment tags
- Where: group "Portfolio Management (Active)" holds C15 and C17, both tagged A,P.
- FIX: rename the group to "Portfolio Management" in spec.json and update the key in build_summary.py `GROUP_LABEL`.

### R13. Medium. ABOR, NAV and partnership books overlap, and the ABOR BIAN mapping is misleading
- Where: C43 "Accounting Book of Record" (ALL, external, BIAN Financial Accounting), C49 "Fund Accounting and NAV" (A,P, external), C51 "Partnership Accounting" (L, external). C55 is mapped to BIAN "Financial Control".
- What is wrong: for listed funds, C43 and C49 are usually the same administrator platform. For Alternatives, C51 is the ABOR. Tagging C43 ALL counts the L books twice. In BIAN, "Financial Accounting" is the enterprise's own ledger, which is C55, not the funds' book of record.
- FIX:
  1. Change C43 `seg` to `["A","P"]`.
  2. Change C43 `does` to "Official positions, transactions, accruals and income of record for listed funds and mandates; feeds C49".
  3. Set C43 `bian:""`.
  4. Set C55 `bian:"Financial Accounting"`.
  5. Add link `{"from":"C43","to":"C49","label":"positions and accruals of record","std":""}`.
  6. Add link `{"from":"C17","to":"C44","label":"IBOR vs ABOR reconciliation","std":""}`. This is the most recognisable buy-side control and is currently undrawn.

### R14. Medium. BIAN mappings that mislead
- C49 → "Mutual Fund Administration" and C50 → "Unit Trust Administration". Both BIAN domains are fund-type domains, each spanning the administration of that fund type, so splitting them across NAV and TA implies a functional split BIAN does not make. FIX: set C49 `bian:"Mutual Fund Administration; Unit Trust Administration"` and C50 `bian:""`, and add a notes line explaining this.
- C66 → "Trade and Price Reporting" (the name exists in the v10 view, checked). Its scope reads as market trade/price publication, a sell-side or trading-venue duty, not regulatory transaction reporting (reviewer knowledge; confirm against the domain description). FIX: set C66 `bian:"Regulatory Reporting"` or empty.
- C61 → "Regulatory Compliance". The component monitors mandate guidelines. FIX: set `bian:"Guideline Compliance"` (as C30).
- notes.md "Where BIAN fits" omits two names used in the spec, "Financial Market Research" (C13) and "Trade and Price Reporting" (C66). FIX: add them to the relevant list.
- All 38 names otherwise appear verbatim in the v10 value chain view (checked, including "Stock Lending and Repos", "Lead and Opportunity Management", "Contractor and Supplier Agreement", "Trade Settlement", "Market Risk", "Customer Case Management").

### R15. Medium. ISO 20022 placement errors and missing buy-side data standards
- C67 msg "ISO 20022 auth (authorities)": FCA returns and AIFMD Annex IV use FCA/ESMA XML schemas, while UK MiFIR transaction reports use the ISO 20022-based auth.016 schema (reviewer knowledge). FIX: move "ISO 20022 auth" from C67 to C66 msg, and set C67 msg to "FCA RegData / AIFMD Annex IV XML (confirm)".
- C04 msg "ISO 20022 acmt": acmt is used for investment-fund account opening between distributor and TA. FIX: move it to C50 msg as "ISO 20022 setr (fund orders); acmt (fund accounts)", and clear C04 msg.
- C09 Distributor Data Hub: target market, costs and ESG data exchange with distributors runs on the FinDatEx templates (EMT, EPT, EET) (reviewer knowledge). FIX: C09 msg "FinDatEx EMT/EPT/EET; ISO 20022 reda". Add a standards entry with `verified:false`.
- C48 "composites": add "GIPS (CFA Institute)" to C48 msg and to standards with `verified:false`.
- Standards row "ISO 20022 business areas (... secl ...)": secl is not used by any component. Remove it, or use it on C42 for CCP-cleared trades.

### R16. Medium. The CALM claims go further than the artefact
- Where: notes.md "Key flows are CALM flows... Controls attach to nodes or flows, each with a requirement-url and a config-url." Assumption 6: "External parties are CALM actor or ecosystem nodes."
- What is wrong: spec.json has no relationship-type on links, no flow objects (unique-id, transitions, sequence), no controls and no node-type on externals. The node-type enum and the relationship names are right. The CALM 1.1 core schema lists node types actor, ecosystem, system, service, database, network, ldap, webclient and data-asset (open-ended via anyOf), and relationship types include interacts, connects, deployed-in, composed-of and options (checked). Protocol enum: HTTP, HTTPS, FTP, SFTP, JDBC, WebSocket, SocketIO, LDAP, AMQP, TLS, mTLS, TCP (checked). So FIX and Swift are message standards, not CALM protocols. That is correct as drawn, but say so.
- FIX: either (a) add `"rel":"connects"|"interacts"` to each link, `"calm":"actor"|"ecosystem"` to each external, and one sample `flows` object (for example flows 5, 7, 9, 10: order to settlement), or (b) reword the notes to "Uses CALM 1.1 node-type and relationship vocabulary. This is not a CALM document; flows and controls are not modelled."

### R17. Medium. Fund-of-funds and look-through holdings are missing
- Where: no component covers it.
- What is wrong: multi-asset active funds, passive funds-of-ETFs and alternatives primary/secondary fund investments all deal into other funds and need look-through holdings for risk, compliance and disclosure.
- FIX: add C88 to L4 "Trade Support and Settlement": `{"id":"C88","name":"Fund Investment Dealing and Look-Through","does":"Places subscriptions and redemptions into in-house and third-party funds; captures look-through holdings for risk and compliance","seg":["ALL"],"sor":"system of record","external":false,"bian":"","msg":"ISO 20022 setr","calm":"service"}`.

### R18. Medium. MNPI controls for the private side are missing
- Where: C62 (A,P) and C77 ("information barriers").
- What is wrong: private credit and public-to-private deals bring inside information on listed issuers. Insider lists, wall-crossings and restricted or watch lists are standard second-line controls across all segments.
- FIX: add C89 to L5 "Compliance and Surveillance": `{"id":"C89","name":"Restricted and Insider Lists","does":"Manages wall-crossings, insider lists, restricted and watch lists across public and private sides","seg":["ALL"],"sor":"control","external":false,"bian":"","msg":"","calm":"database"}`. Add link C89→C30 "restricted list".

### R19. Medium. The ETF primary-market component set is incomplete
- Where: L3 "ETF Primary Market" (C33, C34). passive.json lists "Onboard and review authorised participants" and "Support market makers and venue obligations".
- FIX: add C90: `{"id":"C90","name":"ETF Listing and AP Management","does":"Maintains AP and market-maker agreements, onboarding reviews, listings and venue obligations","seg":["P"],"sor":"system of record","external":false,"bian":"","msg":"","calm":"system"}`. Change C34 name to "Basket (PCF) and iNAV Publication".

### R20. Medium. The key flows never touch the administrator and tell no end-to-end story
- Where: spec.json links. None involves X07, X03, X02, X08 or X16.
- FIX: add four links: X08→C18 "constituents and index events"; X07→C81 "NAV, dealing and register reports"; X03→C52 "commitments and transfers"; C53→X03 "capital calls and distributions" (std "ILPA CC&D Template"). Then, in the flows panel, group the rows under three headings: "Life of a listed trade", "Life of a fund deal", "Life of a capital call".

### R21. Medium. The summary layer-label column is too narrow for its longest word
- Where: Summary.dc.html layer label divs (`width: 140px; padding: 8px 10px; font-size: 21px`). The content width is 120 px.
- Evidence: "Management" measures about 129-135 px in bold 21 px (Inter Display Bold / Inter Bold proxy). It cannot wrap, so it overflows into the right padding and can reach the 140 px edge.
- FIX: in build_summary.py layer label style, change `font-size: 21px; line-height: 26px` to `font-size: 19px; line-height: 24px` and `padding: 8px 10px` to `padding: 8px 6px`. 19 px keeps the 18 px minimum. The worst case is then about 122 px in 128 px. "Risk, Compliance and Regulatory" still fits in 4 lines (96 px of 128 px).

### R22. Medium. The summary carries an "All" chip on 22 of 32 groups, which is clutter that carries no information
- Where: build_summary.py `chips()`.
- FIX: return `[]` when the union is all three. Change the legend item "All three" to "No letter: shared by all three". This removes 22 chips and makes the A, P and L groups stand out.

### R23. Medium. The traceability claim is not evidenced
- Where: notes.md "Each value-chain block in am-chain/*.json maps to at least one component."
- What is wrong: there is no mapping file. R5 shows an activity-level gap (Exit & Realisation). Clients ask "how does this tie to our operating model?"
- FIX: add `am-arch/traceability.json` mapping `{block_id: [component ids]}` for every block in the three chains, and add an appendix table to the detailed board. Until it exists, reword the claim to "Each value-chain block was checked against the components; see R5 for gaps."

### R24. Medium. Corporate finance sits in Investment Operations
- Where: C55 is in L4 group "Corporate Finance and Billing".
- FIX: move the group to L6 and rename it "Enterprise Finance". Change C55 `does` to include "regulatory capital and ICARA". This takes L4 back to 5 groups and widens its summary boxes to 236 px.

### R25. Medium. Small single-component groups inflate the slide
- Where: Summary groups "Distribution Data" (C09 only), "Financial Crime" (C65 only), "Identity and Access" (C77 only).
- FIX: merge C09 into "Client and Distributor Management". Merge C65 into the R1 "Delegate Oversight" layer slot, or keep it and merge C77 into "Integration and Interoperability", renamed "Integration, Access and APIs". Aim for no more than 5 groups per row so every box is 236 px wide.

### R26. Medium. Version detail is missing for verified UK and ILPA items (accurate, but incomplete)
- CCI (PS25/20): the FCA page confirms the rules come into effect on 8 June 2027, with an optional transition from 6 April 2026 (checked). FIX: add "optional transition from 6 April 2026" to the standards `used_for`.
- ILPA: the updated Capital Call and Distribution Template was released 11 September 2025, with implementation in Q1 2027. It replaces v1.2 from 2012 (checked, secondary source). FIX: the standard name should read "...Capital Call and Distribution Template (updated Sept 2025, effective Q1 2027)". The source I read gives no version number, so "v2.0" for that template is unconfirmed (ILPA's resource-library URL slug suggests v2.0).
- Stewardship Code 2026 takes effect 1 January 2026 (checked). Correct as stated.

### R27. Medium. Re-running build.py deletes the Summary board from the canvas
- Where: build.py writes `canvas.json` with only `Main.dc.html` in `boards` and `order`. The current canvas.json has both boards, so it was edited after build.py ran.
- FIX: in build.py, load the existing canvas.json and update only `boards["Main.dc.html"]`, or write both boards with Summary at `{"x":2480,"y":0,"w":1920,"h":1080}` and `"launch":{"view":"canvas"}`.

---

## Low

### R28. Low. Notes inconsistencies
- notes.md says "P groups are Index and Replication, ETF Primary Market and securities lending". There is no securities-lending group, and C39 is A,P in "Treasury, FX and Collateral". FIX: delete "and securities lending".

### R29. Low. The FDC3 source URL is non-canonical
- standards FDC3 `source_url` "https://fdc3-new.finos.org/...". FIX: use `https://fdc3.finos.org/docs/fdc3-standard` after checking it.

### R30. Low. Semantic colour reuse on the detailed board
- build.py uses `SEGC["A"]` for the "Verified" badge, the flow numbers and the assumption numbers. After R2 that colour means Active. FIX: use NAVY `#0B1F3A` for these three.

### R31. Low. The detailed board is for screens, not slides
- The minimum font on Main.dc.html is 12 px at 2400 px wide, about 9.6 px if scaled to 1920. The cards fit: the builder's height estimate (0.57/0.62 em per character) never under-counted lines against the Inter proxy, 0 of 80 cards. Text contrast passes AA everywhere (lowest is #445066 on the Passive tint, 6.55:1). FIX: none needed. Add a footer note "Detailed reference view; see one-page view for presentation".

### R32. Low. Summary L-group border contrast
- The amber border `#C27C00` on the `#FAE6BF` fill is about 2.8:1, below 3:1 for non-text UI. That matters on "Private Fund Admin", where the dashed edge carries meaning. FIX: change `TINT['L']` border to `#8A5600`.

### R33. Low. Language attribute
- Summary.dc.html `<html lang="en">` but Main uses `en-GB`. FIX: set `lang="en-GB"` in build_summary.py.

### R34. Low. Minor functional details
- C45: add "fund and treaty tax reclaims", and add a separate line for "UK reporting fund status" for offshore feeders (reviewer knowledge).
- C13: add "research budget and payment account" (active.json "Manage broker research and its budget").
- C04 `does`: add "client categorisation (retail, professional, eligible counterparty) and FATCA/CRS self-certification".

### R35. Low. The source passes x-dc hygiene
- Both files: `<script src="./support.js"></script>` is the head line, the root size is fixed (2400x5654 and 1920x1080, matching `$preview`), there is no svg, img or iframe, the only network URL is Google Fonts, markup is balanced (parser check) and there are no em/en dashes. Summary root has `overflow:hidden`. FIX: none.

---

## Suggestions to make a pitch audience lean in (narrative and structure)
1. Lead with a headline, not a label. Change the Summary h1 to "One operating backbone, three investment engines" and keep "UK buy-side functional architecture" as the subtitle. The current title describes the slide but does not argue anything.
2. Show oversight as a vertical spine. On the slide, draw L5 (Risk, Compliance, Regulatory and the new Delegate Oversight) as a right-hand vertical band spanning L1-L4, rather than a fifth row. That makes the point the notes make ("L5 watches L1 to L4") visible, and the outsourced-model story lands.
3. Add three numbered thread overlays on the slide: (1) listed trade, order to settlement to IBOR/ABOR recon; (2) ETF create/redeem; (3) capital call to LP. Use thin numbered markers on the boxes, with no arrows needed. Clients currently get a capability map with no motion.
4. Add a time-bound UK change hook. The UK moves to T+1 settlement on 11 October 2027, and the FCA supports moving UK fund unit settlement to T+2 from the same date (checked, FCA). CCI takes full effect on 8 June 2027 (checked). The updated ILPA CC&D template applies from Q1 2027 (checked). A small "2027 pressure points" callout mapped to the affected boxes (C41, C42, C50, C58, C53) turns a static map into a reason to act now.
5. Make the outsourcing boundary explicit. Use a single dashed perimeter on the slide around everything usually run by the administrator, TA or custodian, with "Delegate Oversight" sitting across the boundary. That is the real buy-side operating-model decision, and it is where consulting value lies.
6. Offer a "Level 0" for the boardroom. Even at 32 groups the slide is a dense capability map. A 9-box version (three engines A/P/L × Front, Operations, Oversight, on one data and control platform) gives a strong opening slide, with the current Summary as slide 2 and the detailed board as backup.

---

## Finding counts
Critical 2 (R1-R2). High 7 (R3-R9). Medium 18 (R10-R27). Low 8 (R28-R35).

## Verdict
This is a credible, well-layered, carefully caveated archetype. The IBOR/ABOR separation, the segment-tag mechanism, the "BIAN as labels, not structure" stance and the no-vendor, no-statistics discipline are exactly right, and the BIAN names spot-checked are verbatim. The source files are clean. As a UK pitch asset it has three weaknesses. It under-represents what a UK AFM/AIFM keeps when it outsources (NAV and depositary oversight, box, client money, liquidity tools). It misses mainstream regulatory reporting for derivatives and SFTs and the Alternatives exit stage. And the slide's colour scheme and truncated examples undercut its own message. None of these needs a redesign. They are additive components, palette alignment and label curation, and could be done in one pass.

## The 5 changes that matter most
1. R1: add an L5 "Delegate Oversight" group (C81 NAV and administrator oversight, C82 depositary liaison, and move C80 into it).
2. R2: align the A/P/L colours across both builders (A blue, P teal, L amber).
3. R3: add box management (C83), client money/CASS (C84) and liquidity tools to C49/C59.
4. R6 and R7: replace the auto-truncated summary examples with the curated `GROUP_EX` list and fix the meaning-changing short labels.
5. R8 and R9: verify the seven UK rules, remove the "check before showing a client" wording from the deliverable, and split depositary from custodian.

## Sources actually consulted in this review
- BIAN Service Landscape v10 value chain view: https://bian.org/servicelandscape-10-0-0/views/view_51974.html
- FINOS CALM 1.1 core meta-schema: https://calm.finos.org/release/1.1/meta/core.json, and the nodes page https://calm.finos.org/core-concepts/nodes
- FCA PS25/20 (CCI): https://www.fca.org.uk/publications/policy-statements/ps25-20-supporting-informed-decision-making-final-rules-consumer-composite-investments
- ILPA updated CC&D template (secondary): https://gen2fund.com/news/ilpa-releases-new-capital-call-and-distribution-template-effective-q1-2027/
- UK Stewardship Code 2026 effective date: https://www.traverssmith.com/knowledge/knowledge-container/financial-reporting-council-publishes-the-updated-uk-stewardship-code-2026/
- FCA T+1: https://fca.org.uk/markets/about-t1-settlement
