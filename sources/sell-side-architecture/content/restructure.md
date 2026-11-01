# Restructure: stage view to layered functional architecture

Backups: spec.stage-view.bak.json, notes.stage-view.bak.md. Build and check scripts: /home/claude/sell-arch-tools/ (layout.py, families.json, build.py, validate.py; validate.py passes).

## Before and after: groups
Old location is the owner's stage strip (S0 to S9) or the cross-cutting platform strip. Every one of the 100 components appears exactly once; no component was added, deleted or edited.

| Old stage | Old group | New layer | New group | Components | Change |
|---|---|---|---|---|---|
| S0 Onboarding | G01 Client Lifecycle | L1 Client coverage and onboarding | G01 Client Lifecycle | C01, C02, C03 | unchanged |
| S0 Onboarding | G02 Credit and Documentation | L1 Client coverage and onboarding | G02 Credit and Documentation | C04, C05, C06, C07 | unchanged |
| S1 Origination | G03 Sales and Coverage | L1 Client coverage and onboarding | G03 Sales and Coverage | C08, C09 | unchanged |
| S1 Origination | G04 Quoting and Pricing | L2 Pricing, structuring and origination | G04 Quoting and Pricing | C10, C11, C12, C103 | unchanged |
| S1 Origination | G05 Structuring and Suitability | L2 Pricing, structuring and origination | G05 Structuring and Suitability | C13, C14, C15 | unchanged |
| S2 Execution | G06 Order Management | L3 Execution, trading and booking | G06 Order Management | C16, C17, C18 | unchanged |
| S2 Execution | G07 Execution and Routing | L3 Execution, trading and booking | G07 Execution and Routing | C19, C20, C21 | unchanged |
| S2 Execution | G08 Trading Desk | L3 Execution, trading and booking | G08 Trading Desk | C22, C23 | stays; C24 leaves for G07 |
| S2 Execution | G08 Trading Desk | L3 Execution, trading and booking | G07 Execution and Routing | C24 | C24 moves: venue gateways carry routed and DMA orders (links C19, C17 to C24) |
| S3 Confirmation | G09 Trade Capture and Booking | L3 Execution, trading and booking | G09 Trade Capture and Booking | C25, C26, C101 | unchanged |
| S3 Confirmation | G10 Allocation and Affirmation | L4 Confirmation, clearing and margin | G10 Allocation and Affirmation | C27, C28 | unchanged |
| S3 Confirmation | G11 OTC and Structured Confirmation and Lifecycle | L4 Confirmation, clearing and margin | G11 OTC Confirmation and Lifecycle | C29, C30, C31, C102 | renamed to fit 4 words; structured products lifecycle (C102) stays inside |
| S4 Risk and Reporting | G12 Daily Risk and P&L | L7 Risk, control and regulatory reporting | G12 Daily Risk and P&L | C32, C33, C34 | unchanged |
| S4 Risk and Reporting | G13 Regulatory Trade Reporting | L7 Risk, control and regulatory reporting | G13 Regulatory Trade Reporting | C35, C36, C37 | unchanged |
| S5 Clearing | G15 CCP and Listed Clearing | L4 Confirmation, clearing and margin | G15 CCP and Listed Clearing | C40, C41, C42 | unchanged |
| S5 Clearing | G16 Margin and Netting | L4 Confirmation, clearing and margin | G16 Margin and Netting | C43, C44, C45 | unchanged |
| S6 Settlement | G17 Settlement Processing | L5 Settlement and custody | G17 Settlement Processing | C46, C47, C48 | unchanged |
| S6 Settlement | G18 Market Infrastructure | L5 Settlement and custody | G18 Market Infrastructure | C49, C50, C51 | unchanged |
| S7 Custody | G20 Safekeeping and Segregation | L5 Settlement and custody | G20 Safekeeping and Segregation | C54, C55, C56 | unchanged |
| S7 Custody | G21 Asset Servicing | L5 Settlement and custody | G21 Asset Servicing | C57, C58, C59 | unchanged |
| S8 Financing and Prime | G22 Securities Finance | L6 Financing and collateral | G22 Securities Finance | C60, C61 | unchanged |
| S8 Financing and Prime | G23 Prime Services | L6 Financing and collateral | G23 Prime Services | C62, C63, C64 | unchanged |
| S8 Financing and Prime | G24 Financing Controls | L6 Financing and collateral | G24 Financing Controls | C65, C67 | stays; C66 leaves for G13 |
| S8 Financing and Prime | G24 Financing Controls | L7 Risk, control and regulatory reporting | G13 Regulatory Trade Reporting | C66 | C66 moves: all regulatory trade reporting in one group |
| S9 Market Data | G25 Feed Acquisition | L8 Common services | G25 Feed Acquisition | C68, C70 | unchanged |
| S9 Market Data | G26 Distribution and Licensing | L8 Common services | G26 Distribution and Licensing | C71, C72, C73 | unchanged |
| PLATFORM Cross-cutting platform | P1 Reference Data | L8 Common services | P1 Reference Data | C74, C75, C76 | unchanged |
| PLATFORM Cross-cutting platform | P2 Risk and Limits | L7 Risk, control and regulatory reporting | P2 Risk and Limits | C77, C78, C79 | unchanged |
| PLATFORM Cross-cutting platform | P3 Collateral, Liquidity and Cash | L6 Financing and collateral | P3 Collateral, Liquidity and Cash | C80, C81, C52 | stays; C53 leaves for G28 |
| PLATFORM Cross-cutting platform | P3 Collateral, Liquidity and Cash | L8 Common services | G28 Reconciliation Services | C53 | C53 moves: reconciliation is a shared service |
| PLATFORM Cross-cutting platform | P4 Data and Analytics | L8 Common services | P4 Data and Analytics | C83, C84, C85 | unchanged |
| PLATFORM Cross-cutting platform | P5 Integration and Messaging | L8 Common services | P5 Integration and Messaging | C86, C87, C89 | unchanged |
| PLATFORM Cross-cutting platform | P6 Conduct, Surveillance and Reporting Oversight | L7 Risk, control and regulatory reporting | G27 Conduct and Client Assets | C90 | C90 moves to new group G27 |
| PLATFORM Cross-cutting platform | P6 Conduct, Surveillance and Reporting Oversight | L7 Risk, control and regulatory reporting | G13 Regulatory Trade Reporting | C91 | C91 moves: control hub sits with the reports it controls |
| PLATFORM Cross-cutting platform | P6 Conduct, Surveillance and Reporting Oversight | L7 Risk, control and regulatory reporting | P6 Surveillance and Control Room | C92, C100, C38, C39 | stays; renamed to fit 4 words |
| PLATFORM Cross-cutting platform | P7 Controls and Resilience | L8 Common services | P7 Controls and Resilience | C93, C95, C96, C97, C98 | stays; C94 and C99 leave |
| PLATFORM Cross-cutting platform | P7 Controls and Resilience | L7 Risk, control and regulatory reporting | G27 Conduct and Client Assets | C94 | C94 moves: client assets oversight is a control, new group G27 |
| PLATFORM Cross-cutting platform | P7 Controls and Resilience | L8 Common services | G28 Reconciliation Services | C99 | C99 moves to new group G28 |

Result: 31 groups (24 stage, 7 platform) become 33 groups in 8 layers; two new groups (G27, G28), two renames (G11, P6), seven components moved between groups (C24, C53, C66, C90, C91, C94, C99); C38, C39, C92 and C100 stay together in P6.

## Judgement calls
1. Slide height: 7 layer rows for the lifecycle and cross-lifecycle bands (L1 to L7) plus one common services foundation strip (L8), matching the old platform strip. To get there, the proposed L3 and L4 were merged (Execution, trading and booking), Confirmation joined Clearing (L4) and Settlement joined Custody (L5). L1 and L2 were kept apart so coverage and onboarding read separately from pricing. If the slide must be 7 rows including common services, the next merge is L1 with L2 (Pre-trade, 5 groups).
2. Trade capture and booking (G09, owner stage S3) moved to the Trade band: booking happens on trade date and feeds everything after it; allocation and confirmation stay post-trade.
3. Margin and netting (G16) stays with clearing in L4 rather than with collateral in L6, because margin calculation and calls are driven by CCP and uncleared OTC exposures; collateral sourcing (P3) is in L6 and the link C44 to C80 crosses the layers.
4. Regulatory reporting consolidated: SFTR reporting (C66) and the reporting control hub (C91) join G13, so L7 holds all regulatory trade reporting. P6 renamed Surveillance and Control Room (the old name was 5 words). Best execution oversight (C90) and client money and assets (C94) form new group G27 Conduct and Client Assets.
5. Reconciliation is a shared service: C99 (front to back, CCP, broker, triparty, counterparty) and C53 (nostro and depot) form new group G28 in L8, because both read from every lifecycle layer and from L6. C30 OTC portfolio reconciliation stays in L4 as a bilateral confirmation and EMIR duty.
6. Office: layer office is the dominant owner (L1 Middle, L4 Back, L6 Cross-cutting, L7 Middle); each group keeps its stage-view office in a group 'office' field so no convention is lost. L4 is an even split of Middle (confirmation) and Back (clearing); Back was chosen.
7. Stages tag: groups from the old platform carry ["PLATFORM"], since that is where they sit on the current slides; G13 carries ["S4","S8","PLATFORM"] because it now holds C66 and C91. The traceability table also keeps each stage's slide purpose, value line and office, so no slide content is lost.
8. Kept the group names Trading Desk (now C22, C23) and Controls and Resilience (C93, C95 to C98, including identity, records and third-party oversight) to stay faithful; no new components were needed.
9. Standards: names, text and verified flags unchanged; each row gained 'layers', derived from component fields and regulation tags (CLS, ISDA/GMRA/GMSLA, LEI, ISDA DRR, CBPR+ and the bond tape mapped from named components).
