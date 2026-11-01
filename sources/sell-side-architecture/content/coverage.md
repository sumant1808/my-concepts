# Coverage expansion: before and after

Groups per layer row on the one-page slide (7 equal slots per row) and components per layer. Backup of the previous spec: spec.pre-coverage.bak.json.

## Summary by layer
| Layer | Groups before | Groups after | Components before | Components after | New components |
|---|---|---|---|---|---|
| L1 Client coverage and onboarding | 3 | 6 | 9 | 11 | C104, C105 |
| L2 Pricing, structuring and origination | 2 | 6 | 7 | 11 | C106, C107, C108, C109 |
| L3 Execution, trading and booking | 4 | 7 | 12 | 12 | none |
| L4 Confirmation, clearing and margin | 4 | 6 | 12 | 13 | C110 |
| L5 Settlement and custody | 4 | 6 | 12 | 13 | C111 |
| L6 Financing and collateral | 4 | 6 | 10 | 12 | C112, C113 |
| L7 Risk, control and regulatory reporting | 5 | 7 | 17 | 20 | C116, C115, C114 |
| L8 Common services | 7 | 7 | 21 | 22 | C117 |
| Total | 33 | 51 | 100 | 114 | 14 |

## Groups and components after the expansion
New = component added in this expansion (C104 to C117). Group status: kept, renamed or split (new group from an existing one), or new.

| Layer | Group | Group status | Component | Name | New |
|---|---|---|---|---|---|
| L1 | G03 Sales and Coverage | kept | C08 | Sales CRM and Coverage |  |
| L1 | G03 Sales and Coverage | kept | C09 | Axes and Indications |  |
| L1 | G01 Client Lifecycle | kept, lost or gained components | C01 | Client Onboarding Workflow |  |
| L1 | G01 Client Lifecycle | kept, lost or gained components | C03 | Client Categorisation Register |  |
| L1 | G29 KYC and Screening | split | C02 | KYC and Sanctions Screening |  |
| L1 | G02 Credit and Documentation | kept, lost or gained components | C04 | Counterparty Credit Approval |  |
| L1 | G02 Credit and Documentation | kept, lost or gained components | C05 | Master Agreement Repository |  |
| L1 | G30 Accounts and SSIs | split | C06 | Standing Settlement Instructions |  |
| L1 | G30 Accounts and SSIs | split | C07 | Account and Access Setup |  |
| L1 | G31 Client Service and Reporting | new | C104 | Client Service Desk | yes |
| L1 | G31 Client Service and Reporting | new | C105 | Client Statements and Reporting | yes |
| L2 | G04 Quoting and Pricing | kept, lost or gained components | C10 | RFQ and Quote Management |  |
| L2 | G04 Quoting and Pricing | kept, lost or gained components | C11 | Bond and Credit RFQ |  |
| L2 | G04 Quoting and Pricing | kept, lost or gained components | C12 | FX Streaming Prices |  |
| L2 | G32 Electronic Client Channels | split | C103 | Single-Dealer Platform and Client APIs |  |
| L2 | G33 Voice and Sales-Trading | new | C106 | Voice and Sales-Trading | yes |
| L2 | G05 Structuring and Term Sheets | renamed (was Structuring and Suitability) | C13 | Structuring and Pricing Models |  |
| L2 | G05 Structuring and Term Sheets | renamed (was Structuring and Suitability) | C107 | Term Sheet and Disclosures | yes |
| L2 | G34 Suitability and Product Governance | split | C14 | Suitability and Appropriateness |  |
| L2 | G34 Suitability and Product Governance | split | C15 | New Product Approval |  |
| L2 | G35 Pricing Models and XVA | new | C108 | Quant Model Library | yes |
| L2 | G35 Pricing Models and XVA | new | C109 | XVA Desk Pricing | yes |
| L3 | G06 Order Management | kept, lost or gained components | C16 | Order Management System |  |
| L3 | G06 Order Management | kept, lost or gained components | C18 | Client DMA Gateway |  |
| L3 | G36 Pre-Trade Risk Controls | split | C17 | Pre-Trade Risk Controls |  |
| L3 | G07 Execution and Routing | kept, lost or gained components | C19 | Execution and Smart Routing |  |
| L3 | G07 Execution and Routing | kept, lost or gained components | C20 | Algorithmic Execution Engine |  |
| L3 | G37 Venue and Liquidity Access | split | C21 | FX Aggregation and Internalisation |  |
| L3 | G37 Venue and Liquidity Access | split | C24 | Venue Connectivity Gateways |  |
| L3 | G08 Trading Desk | kept | C22 | Trader Workstation |  |
| L3 | G08 Trading Desk | kept | C23 | Trader Position Management |  |
| L3 | G09 Trade Capture and Booking | kept, lost or gained components | C25 | Trade Capture and Booking |  |
| L3 | G09 Trade Capture and Booking | kept, lost or gained components | C26 | Trade Enrichment |  |
| L3 | G38 Fees and Commissions | split | C101 | Commissions, Fees and Client Billing |  |
| L4 | G10 Allocation and Affirmation | kept | C27 | Allocation and Affirmation |  |
| L4 | G10 Allocation and Affirmation | kept | C28 | Trade Matching Utility |  |
| L4 | G11 OTC Confirmation and Lifecycle | kept, lost or gained components | C29 | OTC Confirmation Matching |  |
| L4 | G11 OTC Confirmation and Lifecycle | kept, lost or gained components | C30 | Portfolio Reconciliation and Disputes |  |
| L4 | G11 OTC Confirmation and Lifecycle | kept, lost or gained components | C31 | Lifecycle Event Processing |  |
| L4 | G39 Structured Products Lifecycle | split | C102 | Structured Products Lifecycle |  |
| L4 | G15 CCP and Listed Clearing | kept, lost or gained components | C40 | Clearing Gateway and Give-ups |  |
| L4 | G15 CCP and Listed Clearing | kept, lost or gained components | C41 | CCP Novation Service |  |
| L4 | G40 Client Clearing and FCMs | split | C42 | Client Clearing Accounts |  |
| L4 | G40 Client Clearing and FCMs | split | C110 | Clearing Broker Connectivity | yes |
| L4 | G16 Margin and Netting | kept | C43 | Margin Calculation |  |
| L4 | G16 Margin and Netting | kept | C44 | Margin Call Management |  |
| L4 | G16 Margin and Netting | kept | C45 | Netting and Compression |  |
| L5 | G17 Settlement Processing | kept, lost or gained components | C46 | Settlement Instruction Engine |  |
| L5 | G17 Settlement Processing | kept, lost or gained components | C47 | Settlement Status and Matching |  |
| L5 | G41 Fails, Penalties and Buy-ins | split | C48 | Fails and Penalties Management |  |
| L5 | G18 Market Infrastructure | kept | C49 | CSD and ICSD Settlement |  |
| L5 | G18 Market Infrastructure | kept | C50 | FX PvP Settlement |  |
| L5 | G18 Market Infrastructure | kept | C51 | Agent Bank Management |  |
| L5 | G20 Safekeeping and Segregation | kept | C54 | Securities Position Keeping |  |
| L5 | G20 Safekeeping and Segregation | kept | C55 | Custody Account Administration |  |
| L5 | G20 Safekeeping and Segregation | kept | C56 | Custody Account Segregation |  |
| L5 | G21 Asset Servicing | kept, lost or gained components | C57 | Corporate Actions Processing |  |
| L5 | G21 Asset Servicing | kept, lost or gained components | C58 | Income and Entitlements |  |
| L5 | G42 Tax and Withholding | split | C59 | Withholding Tax and Reclaims |  |
| L5 | G42 Tax and Withholding | split | C111 | Transaction and Derivative Taxes | yes |
| L6 | G23 Prime Services | kept, lost or gained components | C62 | Prime Margin Lending |  |
| L6 | G23 Prime Services | kept, lost or gained components | C64 | Client Financing Reporting |  |
| L6 | G43 Synthetic Financing | split | C63 | Synthetic Financing and TRS |  |
| L6 | G22 Securities Finance | kept | C60 | Securities Lending and Borrowing |  |
| L6 | G22 Securities Finance | kept | C61 | Repo and Funding Desk |  |
| L6 | G24 Financing Controls | kept | C65 | Locates and Short Controls |  |
| L6 | G24 Financing Controls | kept | C67 | Rehypothecation Controls |  |
| L6 | P3 Collateral Management | renamed (was Collateral, Liquidity and Cash) | C80 | Collateral Inventory and Optimisation |  |
| L6 | P3 Collateral Management | renamed (was Collateral, Liquidity and Cash) | C112 | Collateral Eligibility and Haircuts | yes |
| L6 | G44 Liquidity, Funding and Payments | split | C81 | Treasury Funding and Liquidity |  |
| L6 | G44 Liquidity, Funding and Payments | split | C113 | Funds Transfer Pricing | yes |
| L6 | G44 Liquidity, Funding and Payments | split | C52 | Payments and Nostro Funding |  |
| L7 | G12 Risk, P&L and Profitability | renamed (was Daily Risk and P&L) | C32 | Trading Risk Engine |  |
| L7 | G12 Risk, P&L and Profitability | renamed (was Daily Risk and P&L) | C33 | P&L and Product Control |  |
| L7 | G12 Risk, P&L and Profitability | renamed (was Daily Risk and P&L) | C116 | Desk Profitability and Costs | yes |
| L7 | G46 Valuation and Model Control | split | C34 | Independent Price Verification |  |
| L7 | G46 Valuation and Model Control | split | C115 | Model Inventory and Validation | yes |
| L7 | P2 Risk and Limits | kept, lost or gained components | C77 | Exposure and Limits |  |
| L7 | P2 Risk and Limits | kept, lost or gained components | C78 | Market Risk and Capital |  |
| L7 | G45 Counterparty Credit and XVA | split | C79 | XVA and Counterparty Exposure |  |
| L7 | G45 Counterparty Credit and XVA | split | C114 | Counterparty Credit Capital | yes |
| L7 | G13 Regulatory Trade Reporting | kept | C35 | Transaction Reporting |  |
| L7 | G13 Regulatory Trade Reporting | kept | C36 | Derivatives Trade Reporting |  |
| L7 | G13 Regulatory Trade Reporting | kept | C37 | Pre- and Post-Trade Transparency |  |
| L7 | G13 Regulatory Trade Reporting | kept | C66 | SFTR Reporting |  |
| L7 | G13 Regulatory Trade Reporting | kept | C91 | Regulatory Reporting Control Hub |  |
| L7 | P6 Surveillance and Control Room | kept | C38 | Trade and Order Surveillance |  |
| L7 | P6 Surveillance and Control Room | kept | C39 | Communications Surveillance |  |
| L7 | P6 Surveillance and Control Room | kept | C92 | Compliance Monitoring and STORs |  |
| L7 | P6 Surveillance and Control Room | kept | C100 | Control Room and Restricted Lists |  |
| L7 | G27 Conduct and Client Assets | kept | C90 | Best Execution Oversight |  |
| L7 | G27 Conduct and Client Assets | kept | C94 | Client Money and Assets |  |
| L8 | G25 Feed Acquisition | kept | C68 | Feed Handlers |  |
| L8 | G25 Feed Acquisition | kept | C70 | Colocation and Low-Latency |  |
| L8 | G26 Distribution and Licensing | kept | C71 | Market Data Distribution |  |
| L8 | G26 Distribution and Licensing | kept | C72 | Entitlements and Licence Reporting |  |
| L8 | G26 Distribution and Licensing | kept | C73 | Tick and Historical Store |  |
| L8 | P1 Reference Data | kept | C74 | Instrument Reference Data |  |
| L8 | P1 Reference Data | kept | C75 | Party and Entity Data |  |
| L8 | P1 Reference Data | kept | C76 | Curves, Calendars and Holidays |  |
| L8 | P4 Data and Analytics | kept | C83 | Trade and Position Store |  |
| L8 | P4 Data and Analytics | kept | C84 | Finance Subledger Feed |  |
| L8 | P4 Data and Analytics | kept | C85 | Data Governance and Lineage |  |
| L8 | P5 Integration and Messaging | kept | C86 | Financial Message Gateway |  |
| L8 | P5 Integration and Messaging | kept | C87 | Message Translation Service |  |
| L8 | P5 Integration and Messaging | kept | C89 | Event Streaming and APIs |  |
| L8 | P7 Controls and Resilience | kept | C93 | Identity and Access |  |
| L8 | P7 Controls and Resilience | kept | C95 | Operational Resilience Mapping |  |
| L8 | P7 Controls and Resilience | kept | C96 | Third-Party and FMI Oversight |  |
| L8 | P7 Controls and Resilience | kept | C97 | Records and Audit Archive |  |
| L8 | P7 Controls and Resilience | kept | C98 | Operational Risk and Incidents |  |
| L8 | G28 Reconciliation and Exceptions | renamed (was Reconciliation Services) | C99 | Trade, Position and Market Reconciliations |  |
| L8 | G28 Reconciliation and Exceptions | renamed (was Reconciliation Services) | C53 | Nostro and Depot Reconciliation |  |
| L8 | G28 Reconciliation and Exceptions | renamed (was Reconciliation Services) | C117 | Workflow and Exception Management | yes |
