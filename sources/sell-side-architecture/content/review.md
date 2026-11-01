# Independent review: sell-side global markets functional architecture

Reviewer role: enterprise architect with sell-side capital markets technology and operations experience (sales and trading, front to back; UK, EU and US).
Scope: `sell-arch/spec.json`, `sell-arch/notes.md`, `sell-arch-canvas/build.py`, `build_summary.py`, `common.py`, `label_map.json`, `heights.json`, `check.py`, `project/Main.dc.html`, `project/Summary.dc.html`, `project/canvas.json`, and the screenshots `shots/onepage.png` and `shots/detailed-top.png`. Lessons from `am-arch/review.md` were applied. No files other than this one were changed.

## Reviewer assumptions
1. The pitch audience is a bank's markets COO, CTO, Head of Operations or Head of Change, plus their architecture leads. They know the domain better than the deck.
2. The owner's 10-stage chain (S0 to S9, names included) is fixed input. Findings that touch stage names propose display wording or footnotes, not structural renames.
3. Fixes are written against `spec.json` and the builders. The `.dc.html` files are generated, so after any spec change, re-run `build.py` then `build_summary.py`, then `check.py`. `build.py` no longer writes `canvas.json`, so buy-side finding R27 does not recur (checked).
4. New component ids continue from C99. New external ids continue from X17. Every new component uses the existing field set: `id, name, does, ac, sor, external, bian, msg, calm, fix, fpml_cdm, iso20022, swift_mt, regs`. Unstated fields are `""`, `[]` or `false`.
5. Line-fit for one-page labels was estimated with the builder's own `nlines()` (0.57 em). That estimate is conservative: it predicts 3 lines for "KYC, onboarding, categorisation", which renders in 2. Labels proposed below are 2 lines or fewer by that estimate unless stated.
6. Tags: (checked) means confirmed in this review against a source listed at the end. (reviewer knowledge) means not checked here.

## One-line verdict
The structure is credible and the standards discipline is better than most vendor reference models. All 61 BIAN labels are verbatim, the counts reconcile, and the source is clean. The control spine a bank COO looks for first is thin, though: no front-to-back reconciliation or break management, no control room, US regimes are sketchy, and derivatives reporting is drawn as OTC-only. Two standards labels are now out of date (MT103/202 and the EU T+1 legal basis).

---

## Critical

### R1. Critical. Front-to-back reconciliation and break management are missing
- Where: the whole spec. The only reconciliation component is C53 "Nostro and Depot Reconciliation" (cash and depository statements). C30 is OTC portfolio reconciliation with counterparties.
- What is wrong: the biggest operations cost pool on the sell side is trade and position reconciliation (front office vs books vs settlement; vs exchanges, CCPs, clearing brokers, triparty agents and agents) and the ageing and escalation of breaks (reviewer knowledge). The architecture's own value lines say so. S3: "Cost sits here: breaks, late confirmations and manual affirmation". S6: "fails, CSDR penalties". Yet no component owns this, and no link touches C83 (the firm trade and position store). An operations audience will ask about it within minutes.
- FIX:
  1. Add to P7 "Controls and Resilience": `{"id":"C99","name":"Trade, Position and Market Reconciliations","does":"Reconciles trades and positions front to back and against exchanges, CCPs, clearing brokers, triparty agents and counterparties; ages and escalates breaks","ac":["ALL"],"sor":"control","external":false,"bian":"","msg":"FIX PositionReport (CCP statements)","calm":"service","fix":"PositionReport","fpml_cdm":"","iso20022":"semt","swift_mt":"","regs":[]}`.
  2. Add links `{"from":"C83","to":"C99","label":"trades and positions of record","std":"","thread":"Flow trade"}` and `{"from":"C41","to":"C99","label":"CCP position and margin statements","std":"FIX PositionReport","thread":"Flow margin and collateral"}`.
  3. In build_summary.py set `EX['P7']='Recs, client money, resilience, records'`. This is 3 lines on the estimator and fits `ex_h=66`.
  4. In build.py set `NCOLS['P7']=2` (unchanged; 7 cards over 2 columns).
  5. In notes.md, Layer logic, change the counts to "74 stage components ... 26 platform components (99 in total)". Adjust these again after R2, R9, R11, R17 and R18.

---

## High

### R2. High. There is no control room: restricted and watch lists, information barriers, wall-crossing
- Where: P6 "Conduct and Reporting Oversight" (C90 to C92). C93 covers staff access only.
- What is wrong: a markets division trades while it holds inside information (block trades, wall-crossed market soundings, issuer-client flow, ECM/DCM adjacency even with primary out of scope). The control room's restricted and watch lists feed pre-trade controls and surveillance. This is a core second-line control in all three jurisdictions (reviewer knowledge).
- FIX:
  1. Add to P6: `{"id":"C100","name":"Control Room and Restricted Lists","does":"Runs watch and restricted lists, insider lists, wall-crossings, market soundings and information barrier controls","ac":["ALL"],"sor":"control","external":false,"bian":"Regulatory Compliance","calm":"database","regs":["UK MAR Art 11 and 18","EU MAR"]}`.
  2. Add links `{"from":"C100","to":"C17","label":"restricted list checks","std":"","thread":"Flow reporting"}` and `{"from":"C100","to":"C38","label":"watch list for surveillance","std":"","thread":"Flow reporting"}`.
  3. Set `EX['P6']='Surveillance, control room, best ex, STORs'` (3 lines; this also absorbs R10).

### R3. High. US regimes are thin for an archetype that claims US legal entities
- Where: assumption 1 "UK, EU and US legal entities". Regulation tags on C35, C37, C62, C90, C97 and C78.
- What is wrong: the US side shows only T+1, 15c3-3, 15c3-5, Reg SHO, CFTC Parts 43/45 and SBSR. A US broker-dealer audience will look for the equities and options audit trail (SEC CAT), bond trade reporting (FINRA TRACE), order routing and execution disclosure (SEC Rules 605/606), margin lending (Reg T and FINRA 4210), books and records (SEC 17a-4) and the Volcker rule (reviewer knowledge, all unverified here).
- FIX (append to `regs`; add one standards row, `verified:false`, named "US broker-dealer regimes: SEC CAT, FINRA TRACE, Rules 605/606, Reg T and FINRA 4210, Rule 17a-4, Volcker"):
  - C35 add "SEC CAT (Rule 613)".
  - C37 add "FINRA TRACE".
  - C90 add "SEC Rules 605/606".
  - C62 add "Reg T", "FINRA Rule 4210".
  - C97 add "SEC Rule 17a-4".
  - C78 add "Volcker rule metrics".

### R4. High. Derivatives reporting is drawn as OTC-only and fed from confirmation
- Where: build_summary.py `EX['G13']='Transaction, OTC, transparency'`. Link 29 `{"from":"C29","to":"C36"}`. C36 `does`.
- What is wrong: EU and UK EMIR reporting covers exchange-traded as well as OTC derivatives, and is due T+1 from execution whether or not the trade is confirmed (reviewer knowledge). Showing "OTC" on the client slide and sourcing reports from the confirmation engine gets both scope and timing wrong. A regulatory reporting lead will correct it.
- FIX:
  1. `EX['G13']='MiFIR, EMIR, CFTC, public'` (2 lines).
  2. Change link 29 to `{"from":"C25","to":"C36","label":"derivative trades at execution","std":"ISO 20022 auth; CDM event model","thread":"Flow reporting"}`.
  3. Add link `{"from":"C31","to":"C36","label":"lifecycle events","std":"CDM event model","thread":"Flow reporting"}`.
  4. Change C36 `does` to "Reports OTC and exchange-traded derivative trades, valuations, collateral and lifecycle events to trade repositories and SDRs".

### R5. High. MT103 and MT202 are shown as current, but Swift retired them for cross-border payments in November 2025
- Where: C52 `swift_mt:"MT103/MT202"`; C87 `swift_mt:"MT54x, MT56x, MT103/202"`; the standards row "Swift MT message numbers (... MT103/202 ...)"; notes.md "Payments are a separate migration and were not checked here."
- Evidence (checked): Swift ended CBPR+ coexistence on 22 November 2025, and MT103 and MT202 were "formally retired in favour of their ISO 20022 equivalents" (paymentexpert.com).
- FIX:
  1. Set C52 `swift_mt:""` and `iso20022:"pacs, camt"` (unchanged). Set `msg` to "ISO 20022 pacs.008/pacs.009 (CBPR+); camt".
  2. Set C87 `swift_mt:"MT54x, MT56x"` and `iso20022:"sese, semt, seev"`, and change `does` to "Translates between ISO 15022 MT and ISO 20022 MX for securities, where coexistence continues".
  3. Change the notes sentence to "Cross-border payments moved to ISO 20022 on Swift on 22 November 2025 (MT103/202 retired); securities MT/MX coexistence continues."
  4. Add a standards row `{"name":"Swift CBPR+ end of MT/MX coexistence for payments (22 November 2025)","used_for":"Cash legs and margin payments use pacs/camt","source_url":"https://paymentexpert.com/2025/11/21/swifts-iso-20022-cutover-the-end-of-mt-and-a-20-year-promise/","verified":true}`. A Swift primary source is better if one is available.

### R6. High. Key externals are missing
- Where: spec `externals` (X01 to X16). build.py `SIDES`. Summary "External parties" line.
- What is wrong: five parties a markets COO expects to see are absent (reviewer knowledge unless marked):
  - clearing brokers and FCMs: the bank is not a direct member of every CCP or exchange, and client clearing runs through FCM relationships;
  - interdealer brokers (voice and electronic) for rates, credit and FX;
  - consolidated tape providers: the UK bond tape went live on 22 June 2026 (checked, FCA);
  - issuers, agents and paying agents, who source corporate actions and income;
  - tax authorities, which receive reclaims.
- FIX:
  1. Add `X17 {"name":"Clearing brokers and FCMs","role":"Give clearing access where the bank is not a direct member; clear and margin on its behalf","side":"provider"}`.
  2. Add `X18 {"name":"Interdealer brokers","role":"Voice and electronic dealer-to-dealer liquidity in rates, credit and FX","side":"market"}`.
  3. Add `X19 {"name":"Consolidated tape providers","role":"Publish consolidated post-trade data; UK bond tape live since June 2026","side":"infrastructure"}`.
  4. Add `X20 {"name":"Issuers, agents and paying agents","role":"Announce corporate actions and pay income and redemptions","side":"provider"}`.
  5. Add `X21 {"name":"Tax authorities","role":"Receive withholding tax reclaims and relief claims","side":"regulator"}`.
  6. Put them in build.py `SIDES`: X18 under Markets, X19 under Infrastructure, X17 and X20 under Service providers, X21 under Regulators.

### R7. High. The deliverable carries internal-draft wording, and several "not verified" items can now be verified or corrected
- Where:
  - build.py `chip_txt='Draft · analyst design · not yet reviewed'`.
  - build.py `lims[4]` "...Validate before external use." and `lims[7]` "Status: draft analyst design, not yet reviewed...".
  - build_summary.py footer "Draft, analyst design."
  - spec standards rows "EU DORA" (`verified:false`) and "EU CSDR amendment to T+1 (political agreement, June 2025)".
- What is wrong: the first is the same lesson as buy-side R8. An instruction to oneself printed on a pitch board embarrasses the owner. The second: the EU T+1 row describes a political agreement that is now law. Regulation (EU) 2025/2075 amends CSDR and applies from 11 October 2027 (checked, A&O Shearman). The DORA date is checkable: applicable 17 January 2025 (checked, secondary).
- FIX:
  1. `chip_txt='Illustrative archetype · AI-reviewed, not practitioner-validated · Nov 2026'`. Recompute `chip_w`. The 8.2 px/char estimate gives about 600 px, which fits right of the 2200 px title.
  2. Replace `lims[4]` ending "Validate before external use." with "Regimes marked not verified are named from analyst knowledge; mapping to components is indicative, not legal or regulatory advice."
  3. In `lims[7]` replace "Status: draft analyst design, not yet reviewed, not practitioner-validated." with "Status: AI-reviewed, not practitioner-validated."
  4. Summary footer: start with "Illustrative archetype, AI-reviewed, not practitioner-validated." instead of "Draft, analyst design."
  5. Rename the standards row to "EU T+1: Regulation (EU) 2025/2075 amending CSDR, applies 11 October 2027", source `https://finreg.aoshearman.com/Regulation-to-shorten-settlement-cycle-to-T1-publ`, `verified:true`.
  6. DORA row: name "EU DORA (Regulation (EU) 2022/2554, applicable 17 January 2025)", `verified:true`, source `https://natlawreview.com/article/dora-becomes-applicable-eu`. Swap in EUR-Lex if preferred.
  7. Keep UK T+1 as verified. The gov.uk press release confirms 11 October 2027 (checked). Change its `source_url` to the gov.uk page.

### R8. High. Revenue and fee capture is missing: commissions, fees and client billing
- Where: no component. C08 does "revenue attribution" (sales credits) only.
- What is wrong: execution commissions, clearing and custody fees, prime financing charges, exchange, CCP and broker fee reconciliation, and CSDR penalty pass-through are all sell-side revenue and cost leakage points (reviewer knowledge). A COO or CFO audience expects to see where fees are billed.
- FIX:
  1. Add to S3 G09 "Trade Capture and Booking": `{"id":"C101","name":"Commissions, Fees and Client Billing","does":"Calculates commissions and clearing, custody and financing fees; invoices clients; reconciles exchange, CCP and broker fees and passes on penalties","ac":["ALL"],"sor":"calculation","external":false,"bian":"Commissions","calm":"service"}`. "Commissions" is a verbatim v10 domain (checked).
  2. `EX['G09']='Capture, booking, fees'`.

---

## Medium

### R9. Medium. Several standards labels are mis-applied
- C46 `fix:"SettlementInstructions"`. FIX SettlementInstructions (MsgType T) is mainly a standing settlement instruction message, with an order-specific override mode (checked, OnixS). It is not the instruction a bank sends to a CSD. FIX: set C46 `fix:""`, set C06 `fix:"SettlementInstructions, SettlementInstructionRequest"`, and update S3/S6 matrix counts.
- Link 11 C40→C41 `std:"ISO 20022 secl"`, together with C41 `iso20022:"secl"` and `regs:["EMIR clearing obligation"]`. secl serves securities CCP clearing. OTC derivative and futures clearing interfaces are FIXML, FpML or CCP-specific (reviewer knowledge). FIX: set the link std to "FIXML or FpML (CCP-specific); ISO 20022 secl for securities", and change C41 `iso20022` to "secl (securities only)".
- C43 `regs` "SPAN" is a single CCP's proprietary methodology name. FIX: replace it with "CCP initial margin models", and rename that standards row "Uncleared margin rules phase-in and thresholds; CCP margin models".
- C48 `regs` "CSDR settlement discipline" applies to EU CSDs. The UK did not bring the discipline regime into force (reviewer knowledge). FIX: write "EU CSDR settlement discipline".
- C48 `does` "...penalties and buy-ins". After CSDR Refit, EU mandatory buy-ins apply only if the Commission activates them by implementing act, as a last resort (checked, Norton Rose Fulbright). FIX: `does` "Prioritises fails, manages partials, cash penalties, claims and contractual or regulatory buy-ins".

### R10. Medium. Surveillance sits in a middle-office stage, split from its case management
- Where: S4 group G14 (C38, C39), with S4 `office:"Middle"`. C92 STOR cases are in P6.
- What is wrong: surveillance is a second-line compliance function. Drawing it under the middle office mislabels ownership and splits detection from case handling.
- FIX: move C38 and C39 from G14 into P6 and delete G14. Rename P6 to "Conduct, Surveillance and Reporting Oversight" in spec. Keep `LABEL['P6']='Conduct and Reporting Oversight'` on the slide (title fits 2 lines) and use the R2 EX string. S4 then has 2 groups (G12, G13). Delete `G14` from the `LABEL` and `EX` dicts.

### R11. Medium. FMIs are drawn twice, as stage components and as externals, and one group is mis-dashed
- Where: C28/X13, C41/X04, C49/X05, C50/X07, C69/X12, C82/X14, C88/X08. On the slide, G25 "Feed Acquisition" is dashed ("mostly third-party run") because of C69 and C70.
- What is wrong: double-counting inflates the component count (98), and P3 "Collateral and Liquidity" and P5 contain third-party agents as if they were bank platform services. Feed handling is bank-run, but the slide says otherwise.
- FIX:
  1. Delete C69, C82 and C88. Their roles are carried by X12, X14 and X08.
  2. Change link `C80→C82` to `C80→X14`.
  3. Keep C28, C41, C49 and C50 as stage touchpoints, because the flows need them. Add to notes: "Four FMI touchpoints (C28, C41, C49, C50) are drawn in-stage to show the flow; they are the same parties as X13, X04, X05 and X07."
  4. Set `EX['G25']='Feeds, colocation'`, `EX['P3']='Collateral, funding, liquidity'` and `EX['P5']='Message gateway, translation, APIs'`.
  5. Update the notes external=true list to C28, C41, C49, C50, C70.

### R12. Medium. Client-asset functions overlap
- Where: C56 "Client Asset Segregation" (S7), C94 "Client Money and Assets" (P7) and C67 "Rehypothecation Controls" (S8) all carry CASS and 15c3-3.
- FIX:
  1. Rename C56 "Custody Account Segregation", with `does` "Maintains segregated, omnibus and individual client custody accounts and their asset registers".
  2. Keep C94 as the firm-wide CASS and 15c3-3 control: add "external and internal reconciliations, CASS resolution pack and reserve computation" to `does`.
  3. Leave C67 as is.
  4. Set C56 `regs:[]`.

### R13. Medium. Counterparty credit capital and XVA are under-specified
- Where: C79 "Counterparty Valuation Adjustments", `ac:["DR","FX"]`, `regs:[]`. Summary P2 shows "valuation adjustments".
- What is wrong: CVA/FVA/MVA and exposure apply to repo and SFTs too. A capital audience expects SA-CCR and the CVA capital framework next to FRTB (reviewer knowledge).
- FIX:
  1. Rename C79 "XVA and Counterparty Exposure", with `ac:["ALL"]` and `regs:["Basel SA-CCR","Basel CVA risk framework"]`.
  2. Add those two terms to the "Basel trading book (FRTB) and BCBS 239" standards row (verified:false).
  3. Set `EX['P2']='Exposure, limits, capital, XVA'`.

### R14. Medium. Four BIAN mappings mislead, although all 61 labels are verbatim
- Evidence (checked): every spec BIAN value appears verbatim in the v10 value-chain view. "Financial Instrument Reference Data Management" wraps across two text lines in the SVG. "Corporate Treasury", "Commissions", "Customer Billing", "Credit Risk Operations" and "Liquidity Risk Models" also exist.
- FIX:
  - C78: change `bian` "Market Risk; Economic Capital" to "Market Risk". Economic capital is internal capital, not FRTB regulatory capital.
  - C98: change "Operational Risk Models" to "". The component logs incidents and losses; it does not build models.
  - C81: change "" to "Corporate Treasury" (closest fit).
  - C83 "Position Keeping" is BIAN's account-level transaction log. Keep it, but list it under "Closest fit" in notes.md.
  - C59 "Customer Tax Handling" is a customer-tax domain, closest fit: say so in notes.md.

### R15. Medium. The structured products lifecycle stops at pricing
- Where: S1 C13 (pricing only), S3 C31 (`ac:["DR","FX"]`).
- What is wrong: a structured note, or an equity- or rates-linked OTC product, needs term sheet and issuance documentation, barrier and observation monitoring, coupon and autocall fixings, and secondary market making (reviewer knowledge). The brief names structured products lifecycle as required coverage.
- FIX:
  1. Add to G11: `{"id":"C102","name":"Structured Products Lifecycle","does":"Issues notes and certificates under programmes, monitors barriers and fixings, processes coupons, autocalls and redemptions","ac":["DR","EQ","FI"],"sor":"system of record","external":false,"bian":"","calm":"system","fpml_cdm":"CDM product and event model"}`.
  2. Change C31 `ac` to `["DR","FX","EQ","FI"]`.
  3. Change the G11 group name to "OTC and Structured Confirmation and Lifecycle". Keep `LABEL['G11']='OTC Confirmation'` on the slide and set `EX['G11']='Matching, recs, lifecycle'`.

### R16. Medium. The electronic client channel and voice trading are missing
- Where: S1 and S2. C07 only entitles clients. C97 retains communications.
- FIX:
  1. Add to G04: `{"id":"C103","name":"Single-Dealer Platform and Client APIs","does":"Gives clients branded web and API access to prices, RFQ, orders, post-trade status and analytics","ac":["ALL"],"sor":"engagement","external":false,"bian":"","calm":"webclient","fix":"QuoteRequest, NewOrderSingle"}`.
  2. Set `EX['G04']='RFQ, streaming, e-channels'`.
  3. Change C22 `does` to "Trader desktop for blotters, quotes, orders, voice trade capture and intraday risk".
  4. Change C97 `does` to "Retains orders, trades, communications and reports, and supports trade reconstruction".

### R17. Medium. Pre-trade transparency and client disclosures are missing
- What is wrong: systematic internaliser quoting and pre-trade transparency, and costs and charges disclosures, are standard MiFID II/UK MiFIR sell-side obligations (reviewer knowledge). Only post-trade transparency (C37) is drawn.
- FIX:
  1. Change C37 `name` to "Pre- and Post-Trade Transparency", with `does` "Publishes SI quotes and post-trade price and volume via APAs and consolidated tapes", and add "MiFIR SI regime" to `regs`.
  2. Add "MiFID II costs and charges" to C14 `regs`.
  3. Add a link `{"from":"C37","to":"X19","label":"post-trade data to tape","std":"","thread":"Flow reporting"}` after R6.

### R18. Medium. The flows have gaps and never reach an external party, although the panel says they do
- Where: build.py flows note "...flows between components and external parties". All 36 links are C-to-C.
- What is wrong:
  - DMA dead-ends: C18→C17 and nothing after it.
  - RFQ and streaming trades never reach booking.
  - Exchange trades never reach the CCP.
  - Allocations do not drive settlement.
  - Nothing reaches the ledger.
  - No report reaches an ARM or TR.
- FIX: add these links.
  - `C17→C24` "checked DMA orders to venues", FIX NewOrderSingle, Flow trade.
  - `C10→C25` "RFQ and streamed trades booked", FIX ExecutionReport, Flow trade.
  - `X02→C41` "exchange trades to CCP", "", Flow trade.
  - `C27→C46` "allocations to settle", "", Flow trade.
  - `C83→C84` "trading activity to ledger", "", Flow reporting.
  - `C35→X10` "transaction reports via ARM", ISO 20022 auth, Flow reporting.
  - `C36→X09` "derivative reports", ISO 20022 auth, Flow reporting.
  - `C06→C26` "SSIs for enrichment", "", Flow trade.
  - Also, `name_of()` already resolves X ids, so no builder change is needed.

### R19. Medium. "Origination" collides with DCM/ECM origination, which is out of scope
- Where: S1 `name:"Origination"`. Assumption 2 excludes primary issuance.
- What is wrong: to a markets audience, "origination" means debt and equity capital markets mandates. The slide invites the question "where is DCM?".
- FIX: keep the owner's name and add meaning. Set S1 `purpose` to "Win secondary-market client business: coverage, quoting, structuring and suitability (primary issuance out of scope)". In build_summary.py, add a footer clause "Stage 1 is secondary-market origination; primary issuance is out of scope."

### R20. Medium. One-page: uneven blank boxes waste the best real estate
- Where: Summary stages with 2 groups (S0, S5, S7, S9 after R10, and S4) get boxes about 260 px tall holding 2 to 3 lines. See onepage.png: "Client Lifecycle", "CCP and Listed Clearing" and "Feed Acquisition" are about 70% empty.
- FIX: in build_summary.py, use a fixed 3-slot grid, `bh=(ZH-2*GAP)//3`, for every stage. In 2-group stages, fill the third slot with a tinted "economics" box (no border, background = office tint, 18 px INK) holding a per-stage hook dict:
  - `HOOK={'S0':'Time to first trade','S4':'Fines, capital, remediation','S5':'Margin funding and fees','S7':'Asset servicing fees','S9':'Licence and latency cost'}`.
  - Use the same style, as a 4th line, for 3-group stages only if there is room. Otherwise leave them as they are.
  - All hooks are 2 lines or fewer (estimated). This turns blank space into the "where margin and cost sit" story already in spec `value`.

### R21. Medium. One-page short labels drop or misstate meaning
- FIX (build_summary.py `EX`):
  - G05 "Pricing models, suitability" drops new product approval → "Pricing, NPA, suitability".
  - G20 "Positions, segregation" → "Positions, client assets".
  - G10 "Affirmation, matching utility" drops allocation, the group's first word → "Allocation, affirmation".
- External parties line: a 16-item (21 after R6) run-on sentence at 18 px is unreadable at a glance. Replace it with four labelled runs in one line each: "Clients: ... | Markets: ... | Infrastructure: ... | Providers and regulators: ...", using the build.py `SIDES` grouping. If it overflows 2 lines, reduce to category names plus counts.

### R22. Medium. Detailed board: uneven column bottoms and blank platform cells
- Where: Main.dc.html. S6 (8 cards in 3 groups) ends about 400 px below S0 to S2 and S9 (detailed-top.png). Platform groups are drawn at the max height `pmax`, so P1, P2, P4 and P6 are about 40% blank.
- FIX (optional):
  1. Move G19 "Cash and Payments" (C52, C53) from S6 to P3 and rename P3 "Collateral, Liquidity and Cash". Payments and nostro funding are shared treasury operations serving margin (S5), settlement (S6) and financing (S8). Set `NCOLS['P3']=2`.
  2. Set `NCOLS['P7']=3` after R1 and R2 so platform heights even out.
  3. Rerun `measure.py`, then `build.py`.

### R23. Medium. Asset-class tags need small corrections
- C61 Repo `ac:["FI"]` → `["FI","EQ"]` (equity repo is common in financing and prime).
- C27 Allocation `["EQ","FI"]` → `["EQ","FI","DR"]` (listed derivative allocations and give-ups).
- C42 Client Clearing `["DR","FI"]` → keep, and add "and cash equities via general clearing membership" to `does` only if the bank acts as GCM.
- C19 `sor:"system of record"` → `"calculation"`. The router is not a book of record. Only C16 (orders) and C25 (trades) should be.
- C40 add "FX" to `ac` and "FX prime brokerage give-ups" to `does` (reviewer knowledge).

### R24. Medium. CCP membership and default management are missing
- FIX: change C42 `does` to "Runs client clearing as clearing member: account segregation, margin pass-through, porting, default fund contributions and CCP default management drills". Add "EMIR client clearing" to the existing `regs` (already present).

---

## Low

### R25. Low. Chevron numbers misalign when stage names wrap
- Where: Summary S4 "Risk and reporting" and S8 "Financing and prime". Their numbers sit higher than the others (onepage.png).
- FIX: in build_summary.py h2 style, change `justify-content:center` to `justify-content:flex-start` and `padding:6px 20px 6px 24px` to `padding:8px 20px 6px 24px`. Numbers then align on one row.

### R26. Low. The "no vendor names" claim needs nuance
- Where: notes.md "contains no vendor names". "Swift" appears in C86 to C88 and the standards rows, "CLS" appears in standards, and "SPAN" is in C43 (see R9).
- FIX: write "no vendor product names; FMIs and standards bodies (for example Swift, CLS) appear only as standards or networks".

### R27. Low. Communications surveillance and recording tags
- FIX: add "MiFID II recording of communications (Art 16(7))" to C39 `regs` and C97 `regs`, with `verified:false`.

### R28. Low. Market data reads as the last lifecycle step
- Where: S9 is the tenth chevron.
- FIX: keep the owner's 0 to 9 order. It is sensible because 0 signals pre-trade readiness and keeps the owner's numbering. Set `SHORT['S9']='Market data'` and add `aria-label` text and a footer clause: "Stage 9 feeds every stage." On the detailed board, change S9 `purpose` to start "Feeds every stage:".

### R29. Low. The Swift MT sample is correct, apart from R5
- The reviewer's spot check (reviewer knowledge, not source-verified here) finds these numbers correct:
  - MT540-543 settlement instructions and MT544-547 confirmations;
  - MT548 status, and MT535/536/537 holdings, transactions and pending;
  - MT564-568 corporate actions;
  - MT300 FX and MT305 FX option confirmations;
  - MT950 statement;
  - MT527/558 triparty;
  - MT670/671 SSI update.
- FIX: keep `verified:false` until a Swift standards page is read. Then flip the row and cite it.

### R30. Low. Booking model across legal entities
- FIX: change C25 `does` to "Books executed trades to books and UK, EU or US legal entities, including back-to-back and intercompany legs". Booking models are a live client topic for multi-entity banks.

### R31. Low. The source passes x-dc hygiene (no fix)
- Both boards:
  - `<script src="./support.js"></script>` is in head;
  - the root is fixed (3200x5096 and 1920x1080, matching `$preview`);
  - there is no svg, img or iframe;
  - the only URL is Google Fonts;
  - markup is balanced, node `--check` passes, and no `data-k` attributes are left;
  - there are no em or en dashes;
  - minimum font is 12 px (Main) and 18 px (Summary);
  - all text and fill pairs are at least 7:1.
- `canvas.json` keeps both boards (checked by running check.py, a read-only script).

### R32. Low. The verified flags are honest
- The xref counts reconcile with the component fields: BIAN 61, FIX 21, FpML/CDM 16, ISO 20022 26, MT 15, regs 36 (checked by recomputation).
- All 61 BIAN labels are verbatim v10 (checked).
- US T+1 (28 May 2024), UK T+1 and EU T+1 (11 October 2027) are correct. UK and EU were checked; US is as sourced.
- The only stale "verified" item is the EU T+1 legal basis (R7).

---

## Suggestions to make a pitch audience lean in
1. **Argue, do not label.** Change the Summary h1 to "T+1 in 2027 compresses stages 3 to 6 into one day" and keep the current title as the subtitle. UK and EU both move on 11 October 2027 (checked). Mark the affected boxes with a small "T+1" tag: G10 allocation and affirmation, G02 SSIs, G17 settlement and fails, G19 funding, G22 recalls. Every sell-side COO has this programme open now.
2. **Show motion.** Add three numbered thread markers (1 trade, 2 margin and collateral, 3 reporting) as small circled numbers on the boxes they pass through. The flows exist in spec but are invisible on the slide.
3. **Make the economics visible.** The per-stage `value` lines are the most client-relevant content in the spec and are absent from the slide. Use R20's hook slots, colour-coded margin vs cost.
4. **Draw the mutualisation boundary.** One dashed perimeter around everything usually run by FMIs and utilities (matching, CCP, CSD, PvP, triparty, tape). The question "what should we build, buy or mutualise?" is where consulting value sits.
5. **Add an asset-class pass-through strip.** A 4x10 mini-matrix (EQ, FI, FX, DR × stages) showing which stages each asset class touches makes the notes' best insight ("FX skips custody, uncleared OTC skips CCP, listed skips CSD") visible in five seconds.
6. **Open with a Level 0.** Five boxes (Client, Trade, Post-trade, Finance and prime, Control) on one data platform. Use the current Summary as slide 2 and the detailed board as backup.

---

## Finding counts
Critical 1 (R1). High 7 (R2-R8). Medium 16 (R9-R24). Low 8 (R25-R32).

## Verdict
This is a well-built, honestly caveated sell-side archetype. The 0 to 9 lifecycle spine is clear, asset-class tagging is mostly right, and FMIs are correctly treated as third-party while the bank's own custody and prime stay internal. The "standards as inputs" discipline holds up under checking: 61 of 61 BIAN labels are verbatim, the counts reconcile, and the FIX names are real. The source files are clean.

As a pitch asset it falls short in four ways:
- **Control spine.** It under-draws what a markets COO and CRO look for first: reconciliation and breaks, the control room, US broker-dealer regimes, and XVA/CCR capital.
- **Regulatory accuracy.** It misdraws derivatives reporting as OTC-only.
- **Stale references.** It carries two items a payments- or regulation-literate audience will catch (MT103/202 retired; the EU T+1 row still says "political agreement").
- **Slide design.** The one-page slide spends its blank space on nothing rather than on the T+1 and economics story.

All of this is additive or relabelling work that can be done in one pass. None of it needs a redesign.

## The 5 changes that matter most
1. R1: add C99 Trade, Position and Market Reconciliations, linked from C83 and C41.
2. R4 and R3: fix derivatives reporting (ETD in scope, sourced at execution, "MiFIR, EMIR, CFTC, public" on the slide) and add the US regime tags (CAT, TRACE, 605/606, Reg T and 4210, 17a-4, Volcker).
3. R2: add C100 Control Room and Restricted Lists, feeding C17 and C38.
4. R5 and R7: retire MT103/202 in favour of pacs (CBPR+), update the EU T+1 row to Regulation (EU) 2025/2075, verify DORA, and set the chip to "Illustrative archetype · AI-reviewed, not practitioner-validated · Nov 2026".
5. R20 with suggestion 1: fill the blank one-page slots with per-stage economics hooks and lead with the 11 October 2027 T+1 headline.

## Sources consulted in this review
- BIAN Service Landscape v10 value chain view (downloaded and all spec labels machine-checked): https://bian.org/servicelandscape-10-0-0/views/view_51974.html
- OnixS FIX Latest, SettlementInstructions (T): https://www.onixs.biz/fix-dictionary/latest/msgType_T_84.html
- Swift CBPR+ end of coexistence, 22 Nov 2025: https://paymentexpert.com/2025/11/21/swifts-iso-20022-cutover-the-end-of-mt-and-a-20-year-promise/
- EU T+1, Regulation (EU) 2025/2075: https://finreg.aoshearman.com/Regulation-to-shorten-settlement-cycle-to-T1-publ
- UK T+1, 11 October 2027 (HM Treasury): https://www.gov.uk/government/news/chancellor-goes-further-and-faster-to-drive-growth-by-speeding-up-securities-trades
- CSDR Refit buy-ins: https://www.nortonrosefulbright.com/en/knowledge/publications/3fec092d/csdr-refit-the-key-changes
- DORA applicability: https://natlawreview.com/article/dora-becomes-applicable-eu
- FCA bond consolidated tape: https://www.fca.org.uk/markets/data-reporting-services-providers/bond-consolidated-tape
