# Sell-side global markets functional architecture: notes

## Layer logic
- The architecture is now a functional layer view, not a sequence of stages. It reads top to bottom from pre-trade to post-trade, with a clear split between lifecycle layers (what happens to a trade), cross-lifecycle services (business services that act on positions at several points of the lifecycle) and common services (shared data, technology and control used by every layer).
- Shape: 5 bands, 8 layers, 51 groups, 114 components, 21 externals and 60 key flows in three threads (trade, margin and collateral, reporting). The coverage expansion (v4, below) split groups and added 14 components (C104 to C117); the original 100 components keep every field.
- Why the stage view was wrong for an architecture: it drew Financing and prime (S8) and Market data (S9) as the last two steps of a trade. Financing acts on positions that already exist, from trade date through settlement and for as long as the position is held, and its collateral, liquidity and cash also serve margin and settlement. Market data is consumed by quoting, execution, margin, valuation, risk and surveillance. Neither is a step. The same applies to Risk and reporting (S4): limits gate onboarding and pre-trade checks, reports are due at execution and on lifecycle events, and surveillance reads orders as well as trades.
- The owner's stage numbering survives as a traceability tag ('stages') on every layer and group, so each group still maps back to the slides. Former platform groups carry the tag PLATFORM.
- Not every trade passes every lifecycle layer. FX skips custody. Uncleared OTC trades skip the CCP. Listed derivatives skip CSD settlement.

## Bands and layers
| Band | Layer | Office | Groups | Group count | Components | Traces to |
|---|---|---|---|---|---|---|
| B1 Pre-trade | L1 Client coverage and onboarding | Middle | G03 Sales and Coverage, G01 Client Lifecycle, G29 KYC and Screening, G02 Credit and Documentation, G30 Accounts and SSIs, G31 Client Service and Reporting | 6 | 11 | S1, S0 |
| B1 Pre-trade | L2 Pricing, structuring and origination | Front | G04 Quoting and Pricing, G32 Electronic Client Channels, G33 Voice and Sales-Trading, G05 Structuring and Term Sheets, G34 Suitability and Product Governance, G35 Pricing Models and XVA | 6 | 11 | S1, S2 |
| B2 Trade | L3 Execution, trading and booking | Front | G06 Order Management, G36 Pre-Trade Risk Controls, G07 Execution and Routing, G37 Venue and Liquidity Access, G08 Trading Desk, G09 Trade Capture and Booking, G38 Fees and Commissions | 7 | 12 | S2, S3 |
| B3 Post-trade | L4 Confirmation, clearing and margin | Back | G10 Allocation and Affirmation, G11 OTC Confirmation and Lifecycle, G39 Structured Products Lifecycle, G15 CCP and Listed Clearing, G40 Client Clearing and FCMs, G16 Margin and Netting | 6 | 13 | S3, S5 |
| B3 Post-trade | L5 Settlement and custody | Back | G17 Settlement Processing, G41 Fails, Penalties and Buy-ins, G18 Market Infrastructure, G20 Safekeeping and Segregation, G21 Asset Servicing, G42 Tax and Withholding | 6 | 13 | S6, S7 |
| B4 Cross-lifecycle services | L6 Financing and collateral | Cross-cutting | G23 Prime Services, G43 Synthetic Financing, G22 Securities Finance, G24 Financing Controls, P3 Collateral Management, G44 Liquidity, Funding and Payments | 6 | 12 | S8, PLATFORM |
| B4 Cross-lifecycle services | L7 Risk, control and regulatory reporting | Middle | G12 Risk, P&L and Profitability, G46 Valuation and Model Control, P2 Risk and Limits, G45 Counterparty Credit and XVA, G13 Regulatory Trade Reporting, P6 Surveillance and Control Room, G27 Conduct and Client Assets | 7 | 20 | S4, PLATFORM, S8 |
| B5 Common services | L8 Common services | Cross-cutting | G25 Feed Acquisition, G26 Distribution and Licensing, P1 Reference Data, P4 Data and Analytics, P5 Integration and Messaging, P7 Controls and Resilience, G28 Reconciliation and Exceptions | 7 | 22 | S9, PLATFORM |

- L6 serves L3 to L5; L7 serves L1 to L6; L8 serves every layer (field 'serves').
- Slide fit: seven layer rows (L1 to L7) plus one common services foundation strip (L8), as the platform strip was before. To reach that, execution merges with trading and booking (L3), confirmation with clearing (L4) and settlement with custody (L5). If seven rows must include common services, the next merge is L1 with L2.
- Office is a convention; banks differ. Layer office is the dominant owner, and each group keeps its stage-view office in its own 'office' field (for example G03 Sales and Coverage is Front inside a Middle layer, G09 booking is Middle inside a Front layer, and the financing desks G22 and G23 are Front inside the cross-cutting L6).

## Stage to layer traceability
| Owner stage | Now delivered by |
|---|---|
| S0 Onboarding | L1: G01, G29, G02, G30 |
| S1 Origination | L1: G03, G31; L2: G04, G32, G33, G05, G34, G35 |
| S2 Execution | L2: G33; L3: G06, G36, G07, G37, G08 |
| S3 Confirmation | L3: G09, G38; L4: G10, G11, G39 |
| S4 Risk and Reporting | L7: G12, G46, G13 |
| S5 Clearing | L4: G15, G40, G16 |
| S6 Settlement | L5: G17, G41, G18 |
| S7 Custody | L5: G20, G21, G42 |
| S8 Financing and Prime | L6: G23, G43, G22, G24; L7: G13 |
| S9 Market Data | L8: G25, G26 |
| PLATFORM Cross-cutting platform | L6: P3, G44; L7: P2, G45, G13, P6, G27; L8: P1, P4, P5, P7, G28 |

The same table, with each stage's slide purpose, value line and office, is in xref_matrix.stage_traceability.

## What moved and why
- Stage groups moved as whole groups into layers; only G08, G24, P3, P6 and P7 lost components. The full before and after table is in restructure.md.
- C24 Venue Connectivity Gateways moved from G08 Trading Desk to G07 Execution and Routing: gateways carry routed and DMA orders (links C19 and C17 to C24), which is execution, not desk tooling.
- G09 Trade Capture and Booking (owner stage S3) sits in the Trade band: booking happens on trade date and feeds every later layer.
- C66 SFTR Reporting moved from G24 Financing Controls to G13, and C91 Regulatory Reporting Control Hub moved from P6 to G13, so all regulatory trade reporting and its control sit in one group in L7.
- P6 kept surveillance and the control room (C38, C39, C92, C100) and was renamed Surveillance and Control Room to fit four words. C90 Best Execution Oversight and C94 Client Money and Assets (from P7) form new group G27 Conduct and Client Assets in L7, because both are second-line oversight of client outcomes.
- P3 Collateral, Liquidity and Cash (C80, C81, C52) moved to L6: collateral, funding and payments serve margin (L4), settlement (L5) and financing, which is why they are cross-lifecycle and not a settlement step.
- C99 Trade, Position and Market Reconciliations (from P7) and C53 Nostro and Depot Reconciliation (from P3) form new group G28 Reconciliation Services in L8. Reconciliation is a shared service: both read from every lifecycle layer and from L6. C30 OTC portfolio reconciliation stays in L4 as a bilateral confirmation and EMIR duty.
- Market data (G25, G26) moved from stage S9 to L8 beside reference data, data and analytics, integration, controls and reconciliation.
- G11 renamed OTC Confirmation and Lifecycle (was six words); structured products lifecycle (C102) stays inside.
- Externals now carry 'layers' (where they attach); links carry from_layer and to_layer; standards carry the layers that use them. Threads are unchanged.

## Oversight functions, by layer
- Conduct, best execution and control room: C90 (L7 G27), C92 and C100 (L7 P6).
- Limits and credit: C04 (L1), C17 (L3) and C77 (L7).
- Client money and assets: C56 (L5), C67 (L6) and C94 (L7).
- Reconciliation and break management: C99 and C53 (L8 G28), alongside C30 (L4, OTC portfolio reconciliation).
- Operational resilience and third-party and FMI oversight: C95 and C96 (L8 P7), with C51 Agent Bank Management (L5). Oversight of outsourced or third-party-run services is drawn, not implied.
- Regulatory reporting is never missing from the trade flow. It is produced and controlled in L7 G13 (C35 transaction reporting, C36 derivatives, C37 pre- and post-trade transparency, C66 SFTR, C91 control hub), and surveillance (C38, C39, fed by the control room C100) runs to C92 STOR cases in P6. Derivative reports are sourced at execution (C25) and from lifecycle events (C31), not from confirmation.
- external=true appears on 5 components: C28 matching utility and C41 CCP (L4), C49 CSD/ICSD and C50 FX PvP (L5) and C70 colocation (L8). The four FMI touchpoints are the same parties as X13, X04, X05 and X07. Data vendors, triparty agents and the Swift network are drawn only as externals (X12, X14, X08). The bank's own custody business (L5) is internal, and the CSDs it uses are external.

## Where BIAN fits and where it does not
- Source: the BIAN Service Landscape v10 value chain view. All 61 BIAN labels were copied from the ServiceDomain labels on that page and machine-checked against the extracted list. BIAN provides labels, not structure, because it is bank-oriented and has no lifecycle view of capital markets.
- **Strong fit** (front office and listed post-trade): Market Order, Market Order Execution, Program Trading, Quote Management, Market Making, eTrading Workbench, Trader Position Operations, Order Allocation, Trade Confirmation Matching, Trade Clearing, Trade Settlement, Securities Fails Processing, Securities Position Keeping, Custody Administration, Corporate Action, Stock Lending and Repos, Collateral Allocation Management, Collateral Asset Administration, Financial Instrument Reference Data Management, Legal Entity Directory, and the market data domains (Information Provider Operation and Administration, Market Data Switch Operation, Market Information Management).
- **Closest fit:**
  - Trading Models (C13), Product Design (C15 new product approval), Trading Book Oversight (C33 P&L) and Market Risk Models (C32).
  - Market Risk; Economic Capital (C78), Credit and Margin Management (C43, C62), Compliance Reporting (C91), Regulatory Compliance (C100) and Commissions (C101).
  - Position Keeping (C83, BIAN's account-level transaction log), Employee Access (C93), Continuity Planning (C95) and Contractor and Supplier Agreement (C96).
  - Corporate Treasury (C81, closest fit) and Customer Tax Handling (C59, a customer-tax domain, closest fit).
- Trade and Price Reporting is used only on C37 (public post-trade transparency), which matches its scope. Regulatory Reporting covers C35, C36 and C66.
- Corrected by the main session after a recheck of the BIAN v10 value chain view: service domains named exactly "Market Risk", "Credit Risk" and "Counterparty Risk" DO exist, alongside "Market Risk Models", "Credit Risk Models" and "Credit Risk Operations". C32 (the risk calculation engine) keeps "Market Risk Models"; C78 now carries "Market Risk; Economic Capital".
- **No BIAN domain was found, so the field is blank, for:** KYC screening, client categorisation, SSIs, booking, enrichment, portfolio reconciliation, front-to-back reconciliation (C99), lifecycle events, structured products lifecycle (C102), single-dealer platform (C103), surveillance, DMA, pre-trade controls, FX aggregation, client clearing, compression, CCP, CSD, PvP, income, client assets, TRS, locates, rehypothecation, valuation adjustments, lineage, best execution, operational risk incidents (C98) and client money.

## Cross-reference by standard
- **CALM 1.1:** all 114 components carry a node type from the core.json enum. This is a legend, not a CALM document: there are no relationship objects, flows or controls. CALM protocols (HTTP, TCP, AMQP and so on) are transport layers, while FIX, Swift and ISO 20022 are message standards.
- **FIX (23 components):** quotes, IOIs, orders and executions (L2, L3), allocations and confirmations (L4), trade capture for booking, clearing and transparency (L3, L4, L7), collateral, margin and position reports (L4, L8), SecurityDefinition (L8 P1) and market data (L8). It is not used for onboarding, custody, cash, or most settlement.
- **FpML and CDM (17 components):** OTC confirmation and lifecycle (L4) and reporting (L7), legal agreements (C05), collateral and margin calls (C43, C44, C80), repo and securities lending (C60, C61), structured products (C102) and product models (C13, C63, C74). They do not cover cash equity or bond settlement, KYC, or market data.
- **ISO 20022 (25 components, business area level only):**
  - secl for securities clearing only (derivative and futures clearing interfaces are FIXML, FpML or CCP-specific), sese and semt for settlement, seev for corporate actions and colr for collateral.
  - reda for reference data, auth for MiFIR, EMIR and SFTR reporting, acmt for custody accounts, and pacs and camt for cash.
  - It is not mapped at execution or confirmation. setr and fxtr exist, but sell-side use was not checked.
- **Swift MT (12 components):** MT54x, MT535-537, MT56x, MT300/305, MT950, MT527/558 and MT670/671. All numbers are unverified. Verified: Swift set no securities migration date and keeps ISO 15022 and ISO 20022 in sync, so "MT54x to ISO 20022" is a coexistence, not a forced cut-over. Cross-border payments moved to ISO 20022 on Swift on 22 November 2025 (MT103/202 retired); securities MT/MX coexistence continues.
- **Regulation tags (38 components):** see the standards list. Verified regimes are US T+1 (28 May 2024), UK T+1 (11 October 2027, gov.uk), EU T+1 (Regulation (EU) 2025/2075, applies 11 October 2027), CSDR settlement discipline changes, DORA (applicable 17 January 2025), the Swift CBPR+ payments cut-over (22 November 2025), the UK bond consolidated tape (FCA), MiFIR Art 26, EMIR Refit (UK from 30 September 2024), CFTC Part 45, SFTR, UK MAR STORs, ISDA SIMM, CLS PvP and FCA PS21/3. US broker-dealer regimes (SEC CAT, FINRA TRACE, Rules 605/606, Reg T and FINRA 4210, Rule 17a-4, Volcker) were added on reviewer knowledge and are not verified.
- **Gaps where no standard exists:** KYC data, pre-trade controls, P&L, IPV, licence reporting, tax reclaims, operational resilience and third-party oversight data. The full list is in xref_matrix.coverage.gaps.

## Limitations and unverified items
- 19 of the 41 standards entries are verified:false. They were not checked against the source for this draft and should be validated before external use. These are UK MiFIR, best execution, pre- and post-trade transparency and the SI regime, EMIR risk-mitigation and clearing duties, CFTC Part 43 and SEC SBSR, UMR phase-in and CCP margin models, CASS and 15c3-3, Reg SHO, 15c3-5 and RTS 6, KYC/AML, MiFID categorisation, suitability and costs and charges, ISDA/GMRA/GMSLA, LEI/ISIN/CFI/FIGI, FRTB, SA-CCR, CVA and BCBS 239, ISDA DRR, US broker-dealer regimes, MiFID II recording of communications, UK MAR Articles 11 and 18, and the Swift MT numbers.
- FIX names were checked against a third-party FIX Latest dictionary, because the FIX Trading Community site needs JavaScript to render. CDM was checked at model level (product, event, legal, process, eligible collateral, repo, securities lending), not at function level.
- BIAN was checked against v10 only, and later releases may rename domains.
- The links are illustrative. This is an archetype for client-facing thought leadership, not a client's estate. It is AI-reviewed and has not been practitioner-validated. It contains no vendor product names (FMIs and standards bodies, for example Swift and CLS, appear only as standards or networks), no statistics and no agentic AI.

- Unchanged by the restructure: every component field, every verified and unverified flag, the 50 links and their threads, and the 21 externals. The layering is an analyst judgement on an archetype and has not been practitioner-validated.

## Review changes (v2)
- Applied independent review findings R1 to R32 (see fixes.md). Surveillance moved to P6, cash and payments moved to P3, derivative reporting re-sourced to execution, five externals and five components added, three FMI components removed as stage components.
- Stage 1 keeps the name Origination; its purpose line states secondary-market origination.

## Layered view (v3)
- Restructured from 10 lifecycle stages plus a platform into 5 bands and 8 layers after owner feedback that financing and market data are not sequential steps. See restructure.md for the group-by-group mapping and judgement calls.

## Coverage expansion (v4)
- Owner feedback: the one-page slide looked thin. Each layer row now holds 6 or 7 group boxes (L1 6, L2 6, L3 7, L4 6, L5 6, L6 6, L7 7, L8 7), up from 2 to 5 (L8 was already 7). Backups: spec.pre-coverage.bak.json, notes.pre-coverage.bak.md. Before and after table: coverage.md. Build and check: /home/claude/sell-arch-tools/coverage_build.py and validate_coverage.py (passes).
- Method: split existing groups along functional seams first, then add components only for genuine sell-side gaps. 18 groups were created, 4 renamed, and 14 components added (100 to 114). Ten illustrative links were added (50 to 60); threads unchanged.

### What was split
| Layer | Old group | Change | Why |
|---|---|---|---|
| L1 | G01 Client Lifecycle | C02 to new G29 KYC and Screening | financial crime checks are run by a distinct team from onboarding orchestration |
| L1 | G02 Credit and Documentation | C06, C07 to new G30 Accounts and SSIs | operational account and SSI set-up is separate from credit and legal terms |
| L2 | G04 Quoting and Pricing | C103 to new G32 Electronic Client Channels | the client-facing e-channel is distinct from pricing engines |
| L2 | G05 Structuring and Suitability | C14, C15 to new G34 Suitability and Product Governance; G05 renamed Structuring and Term Sheets | product governance is a control, structuring is a front-office build |
| L3 | G06 Order Management | C17 to new G36 Pre-Trade Risk Controls | market-access controls are a regulated control in their own right |
| L3 | G07 Execution and Routing | C21, C24 to new G37 Venue and Liquidity Access | connectivity and liquidity access are separate from routing and algo logic |
| L3 | G09 Trade Capture and Booking | C101 to new G38 Fees and Commissions | fee capture and billing was flagged as hidden inside booking |
| L4 | G11 OTC Confirmation and Lifecycle | C102 to new G39 Structured Products Lifecycle | issuance, fixings and autocalls are a distinct servicing line |
| L4 | G15 CCP and Listed Clearing | C42 to new G40 Client Clearing and FCMs | client clearing and broker relationships differ from house CCP access |
| L5 | G17 Settlement Processing | C48 to new G41 Fails, Penalties and Buy-ins | fails, CSDR penalties and buy-ins are a separate cost and control pool |
| L5 | G21 Asset Servicing | C59 to new G42 Tax and Withholding | tax relief and transaction taxes form a distinct service |
| L6 | G23 Prime Services | C63 to new G43 Synthetic Financing | synthetic prime and TRS run as a separate desk from cash prime |
| L6 | P3 Collateral, Liquidity and Cash | C81, C52 to new G44 Liquidity, Funding and Payments; P3 renamed Collateral Management | collateral and treasury funding are different functions |
| L7 | G12 Daily Risk and P&L | C34 to new G46 Valuation and Model Control; G12 renamed Risk, P&L and Profitability | independent valuation and model control are second-line functions |
| L7 | P2 Risk and Limits | C79 to new G45 Counterparty Credit and XVA | XVA and counterparty credit capital were flagged as thin |
| L8 | G28 Reconciliation Services | renamed Reconciliation and Exceptions (gains C117) | break workflow sits with reconciliation |

### What was added
| Id | Name | Layer and group | Why |
|---|---|---|---|
| C104 | Client Service Desk | L1 G31 Client Service and Reporting | client queries and break chasing had no owner on the client side |
| C105 | Client Statements and Reporting | L1 G31 Client Service and Reporting | trade, position and valuation statements and MiFID ex-post costs reports were missing |
| C106 | Voice and Sales-Trading | L2 G33 Voice and Sales-Trading | voice and sales-trading support was flagged missing; complements the e-channel |
| C107 | Term Sheet and Disclosures | L2 G05 Structuring and Term Sheets | structured products need term sheets, final terms and KIDs before sale |
| C108 | Quant Model Library | L2 G35 Pricing Models and XVA | pricing, risk and IPV share a governed quant library |
| C109 | XVA Desk Pricing | L2 G35 Pricing Models and XVA | XVA was only calculated after the trade; the desk prices and hedges it pre-deal |
| C110 | Clearing Broker Connectivity | L4 G40 Client Clearing and FCMs | where the bank is not a CCP member it clears through brokers and FCMs (X17) |
| C111 | Transaction and Derivative Taxes | L5 G42 Tax and Withholding | stamp duty, FTTs and 871(m) withholding are per-trade obligations |
| C112 | Collateral Eligibility and Haircuts | L6 P3 Collateral Management | collateral optimisation needs governed eligibility schedules and haircuts |
| C113 | Funds Transfer Pricing | L6 G44 Liquidity, Funding and Payments | desk funding and liquidity charges drive trading profitability |
| C116 | Desk Profitability and Costs | L7 G12 Risk, P&L and Profitability | desk and client profitability after costs, funding and capital was missing |
| C115 | Model Inventory and Validation | L7 G46 Valuation and Model Control | model risk governance had no component |
| C114 | Counterparty Credit Capital | L7 G45 Counterparty Credit and XVA | counterparty credit capital (SA-CCR, CVA capital) was flagged as thin |
| C117 | Workflow and Exception Management | L8 G28 Reconciliation and Exceptions | exceptions from reconciliation and operations need routed, aged workflow |

### Considered and not added
- Already covered by existing components, so not duplicated: corporate actions (C57), fails and buy-ins (C48), fee billing (C101), client clearing (C42), XVA exposure (C79), collateral optimisation (C80), intraday liquidity (C81), limits and credit exposure (C77), market data entitlements and licences (C72), SSIs (C06), static data (C74, C75), trade reconstruction and records (C97), best execution and TCA (C90), P&L explain (C33).

### Cross-references for new components
- BIAN labels on new components, each found verbatim among the ServiceDomain labels of the v10 value chain view (fetched 1 November 2026): Customer Case Management (C104), Dealer Desk (C106, closest fit), Quant Model (C108) and Contribution Analysis (C116, closest fit). The other ten are blank.
- No FIX, ISO 20022 or Swift MT fields were set on new components; C112 carries CDM eligible collateral. New regulation tags reuse existing rows (MiFID costs and charges, recording of communications, UMR, SA-CCR and CVA) or three new standards rows, all verified false: EU PRIIPs KID; UK stamp duty and SDRT, EU FTTs and US 871(m); PRA SS1/23 and SR 11-7.

### Limitations of the expansion
- The 14 new components, their links and the group splits are analyst design and have not been reviewed by the independent reviewer or a practitioner.
- Eight groups hold one component (G29, G32, G33, G36, G38, G39, G41, G43). Each one's 'does' text supports two example lines, but they are the first candidates to merge if the slide has to shrink.
- Group 'stages' tags on new groups are inferred: G31 Client Service and Reporting is tagged S1 and G33 Voice and Sales-Trading S1 and S2; G44 and G45 inherit PLATFORM from P3 and P2.
- C114 Counterparty Credit Capital and C79 XVA and Counterparty Exposure share SA-CCR and CVA tags: C79 produces exposure, C114 turns it into capital.
