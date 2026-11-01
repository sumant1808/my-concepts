import json
A,P,L,ALL=["A"],["P"],["L"],["ALL"]
AP=["A","P"]; APL=["A","P","L"]; AL=["A","L"]
# (name, does, seg, sor, external, bian, msg, calm)
layers=[
("Clients and Distribution","How clients, distributors and LPs are won, onboarded, served and reported to.",[
 ("Client and Distributor Management",[
  ("Client CRM","Records clients, intermediaries, consultants, contacts and interactions",ALL,"engagement",False,"Customer Relationship Management","","system"),
  ("Sales Pipeline and RFP","Tracks opportunities, RFPs, due diligence questionnaires and consultant ratings",AP,"engagement",False,"Lead and Opportunity Management","","system"),
  ("Fundraising and LP Pipeline","Manages target LPs, commitments, closings and side-letter negotiation",L,"engagement",False,"","","system")]),
 ("Onboarding and Agreements",[
  ("Client Onboarding Workflow","Orchestrates classification, due diligence, account opening and documentation",ALL,"engagement",False,"Party Lifecycle Management","ISO 20022 acmt (account management)","service"),
  ("Mandate and Agreement Repository","Holds IMAs, LPAs, side letters, fee terms and investment guidelines",ALL,"system of record",False,"Customer Agreement","","database")]),
 ("Digital Channels",[
  ("Client and Adviser Portal","Self-service holdings, reports, documents and dealing for clients and advisers",AP,"engagement",False,"","","webclient"),
  ("LP Investor Portal","Delivers capital notices, LP reports, tax documents and data-room access",L,"engagement",True,"","","webclient"),
  ("Public Fund Website","Publishes prices, factsheets, holdings disclosures and legal documents",ALL,"engagement",False,"","","webclient")]),
 ("Distribution Data and Platforms",[
  ("Distributor Data Hub","Exchanges target market, costs, share-class and listing data with distributors",AP,"integration",False,"Product Directory","ISO 20022 reda (reference data)","service")]),
 ("Client Reporting and Servicing",[
  ("Client Reporting Engine","Produces factsheets, mandate reports, statements and commentary packs",AP,"calculation",False,"","","service"),
  ("LP Reporting Engine","Produces quarterly LP reports and ILPA fee and performance templates",L,"calculation",True,"","ILPA Reporting and Performance Templates","service"),
  ("Client Case Management","Logs queries, complaints and outcomes as Consumer Duty evidence",ALL,"engagement",False,"Customer Case Management","","system")]),
]),
("Investment Management","Where investment decisions are researched, made and monitored across the three segments.",[
 ("Research and Insight",[
  ("Research Management","Captures notes, models, ratings, house views and company engagement",A,"system of record",False,"Financial Market Research","","system"),
  ("ESG and Sustainability Data","Holds ESG scores, controversies, climate metrics and exclusion lists",ALL,"data",False,"","","data-asset")]),
 ("Portfolio Management (Active)",[
  ("Portfolio Management System","Models portfolios, cash, target weights and what-if scenarios",AP,"system of record",False,"Investment Portfolio Management","","system"),
  ("Portfolio Optimiser","Constructs portfolios against risk model, constraints and transaction costs",A,"calculation",False,"","","service"),
  ("Investment Book of Record","Real-time start-of-day and intraday positions and cash for decisions",AP,"system of record",False,"Securities Position Keeping","","database")]),
 ("Index and Replication (Passive)",[
  ("Index Data Management","Ingests constituents, weights, index events and licence entitlements",P,"data",False,"","","data-asset"),
  ("Replication and Rebalance Engine","Generates model baskets, sampling and rebalance trade lists",P,"calculation",False,"","","service"),
  ("Tracking Error Analytics","Measures and attributes tracking difference and tracking error",P,"calculation",False,"","","service")]),
 ("Private Markets Deal Management (Alternatives)",[
  ("Deal Pipeline Management","Logs, screens and tracks deals from origination to committee",L,"engagement",False,"","","system"),
  ("Due Diligence Workspace","Coordinates data-room review, adviser workstreams, findings and red flags",L,"engagement",False,"","","system"),
  ("Deal Modelling and IC","Hosts returns models, investment papers, IC decisions and cross-fund allocations",L,"calculation",False,"","","service")]),
 ("Portfolio Monitoring and Value Creation (Alternatives)",[
  ("Portfolio Company Monitoring","Collects portfolio company KPIs, financials and value-creation plan progress",L,"data",False,"","","system"),
  ("Loan and Covenant Monitoring","Tracks private credit loans, covenants, interest, amortisation and watchlists",L,"system of record",False,"Corporate Loan","","system"),
  ("Real Asset Management","Holds property and infrastructure data, leases, capex and operations",L,"system of record",False,"","","system")]),
 ("Stewardship",[
  ("Proxy Voting Platform","Receives ballots, applies voting policy, lodges and records votes",AP,"system of record",True,"","ISO 20022 seev (securities events)","system"),
  ("Engagement Tracker","Records engagement objectives, escalations and outcomes for stewardship reporting",ALL,"system of record",False,"","","system")]),
]),
("Trading and Execution","Turning decisions into executed trades, primary-market ETF activity, deal completion and treasury.",[
 ("Order Management",[
  ("Order Management System","Captures orders, aggregates blocks and allocates fills fairly to accounts",AP,"system of record",False,"Market Order","FIX","system"),
  ("Pre-Trade Compliance","Checks orders against mandate, regulatory and house restrictions",AP,"control",False,"Guideline Compliance","","service")]),
 ("Execution and Best Execution",[
  ("Execution Management System","Routes orders to brokers, venues and algorithms; captures fills",AP,"engagement",False,"Market Order Execution","FIX","system"),
  ("TCA and Best Execution","Measures execution quality; evidences best-execution policy, venue and broker reviews",AP,"control",False,"","","service")]),
 ("ETF Primary Market (Passive)",[
  ("Creation and Redemption Platform","Takes authorised participant orders; manages in-kind and cash settlement",P,"system of record",False,"","","system"),
  ("Basket and iNAV Publication","Publishes daily baskets, indicative NAV and premium/discount monitoring",P,"calculation",True,"","","service")]),
 ("Private Markets Transaction Execution (Alternatives)",[
  ("Deal Closing Management","Manages signing, consents, completion funds flows and deal financing",L,"engagement",False,"","","system"),
  ("Fund Financing Management","Manages subscription lines, asset-level debt, drawdowns and deal hedging",L,"system of record",False,"","","system")]),
 ("Treasury, FX and Collateral",[
  ("FX and Cash Management","Executes share-class hedging, FX, cash sweeps and liquidity forecasts",ALL,"system of record",False,"","FIX","system"),
  ("Collateral and Margin Management","Calculates margin, eligible collateral and haircuts for OTC derivatives",ALL,"system of record",False,"Collateral Allocation Management","ISO 20022 colr; ISDA CDM","system"),
  ("Securities Lending Oversight","Oversees agent lending, loans, recalls, collateral and revenue split",AP,"control",True,"Stock Lending and Repos","ISDA CDM (securities lending scope)","service")]),
]),
("Investment Operations and Accounting","Post-trade, books of record, valuation, NAV, investor servicing and private fund administration.",[
 ("Trade Support and Settlement",[
  ("Trade Capture and Enrichment","Books executions, enriches settlement instructions and validates trade data",AP,"system of record",False,"","FIX","service"),
  ("Confirmation and Matching","Matches allocations and confirmations with brokers and custodians",AP,"integration",False,"Trade Confirmation Matching","FIX; ISO 20022 setr","service"),
  ("Settlement and Fails Management","Instructs settlement, tracks status and manages fails and penalties",AP,"system of record",False,"Trade Settlement","ISO 20022 sese; ISO 15022 MT 540-543","service")]),
 ("Positions, Cash and Events",[
  ("Accounting Book of Record","Official positions, transactions, accruals and income of record",ALL,"system of record",True,"Financial Accounting","","database"),
  ("Reconciliation Engine","Reconciles positions, cash and trades with custodians and administrators",ALL,"control",False,"Account Reconciliation","ISO 20022 semt; camt","service"),
  ("Corporate Actions and Income","Captures events, takes elections, reconciles entitlements, reclaims withholding tax",AP,"system of record",False,"Corporate Action","ISO 20022 seev","system")]),
 ("Valuation and Performance",[
  ("Pricing and Valuation Control","Sources prices, runs tolerance, stale-price and fair-value challenges",AP,"control",False,"Financial Instrument Valuation","","service"),
  ("Illiquid Asset Valuation","Runs periodic private asset valuations and valuation committee evidence",L,"calculation",False,"Financial Instrument Valuation","","service"),
  ("Performance and Attribution","Calculates returns, attribution, composites, IRR and multiples",ALL,"calculation",False,"Investment Portfolio Analysis","","service")]),
 ("Fund Accounting and Transfer Agency",[
  ("Fund Accounting and NAV","Calculates daily NAV, fee accruals and fund financial statements",AP,"system of record",True,"Mutual Fund Administration","","system"),
  ("Transfer Agency and Register","Processes dealing, unitholder register, distributions and investor tax reporting",AP,"system of record",True,"Unit Trust Administration","ISO 20022 setr (fund orders)","system")]),
 ("Private Fund Administration (Alternatives)",[
  ("Partnership Accounting","Maintains fund, feeder and SPV accounts and investor allocations",L,"system of record",True,"","","system"),
  ("LP Register and Commitments","Holds commitments, unfunded amounts, transfers and side-letter terms",L,"system of record",True,"","","database"),
  ("Capital Call and Distribution","Calculates and issues capital calls, distributions and equalisation",L,"calculation",True,"","ILPA Capital Call and Distribution Template","service"),
  ("Fee and Carry Engine","Calculates management fees, offsets, waterfalls and carried interest",L,"calculation",False,"","ILPA Reporting Template","service")]),
 ("Corporate Finance and Billing",[
  ("Corporate Finance and Billing","Manager's ledger, mandate fee billing, revenue, expenses and regulatory capital",ALL,"system of record",False,"Financial Control","","system")]),
]),
("Product, Risk, Compliance and Regulatory","Second-line oversight, product governance and regulatory output across all segments.",[
 ("Product Governance",[
  ("Product Lifecycle and Approval","Runs product approval, target market, periodic reviews and closures",ALL,"system of record",False,"Product Design","","system"),
  ("Value and Outcomes Assessment","Assesses fair value and consumer outcomes for board reporting",ALL,"control",False,"","","service"),
  ("Product Disclosure Documents","Produces prospectus, CCI product summary, costs and sustainability disclosures",ALL,"system of record",False,"","","service")]),
 ("Investment Risk",[
  ("Market and Liquidity Risk","Computes VaR, stress tests, exposures, leverage and liquidity risk",ALL,"calculation",False,"Market Risk","","service"),
  ("Counterparty and Credit Exposure","Monitors counterparty, issuer and collateral exposure against limits",ALL,"calculation",False,"Counterparty Risk","","service")]),
 ("Compliance and Surveillance",[
  ("Post-Trade Compliance Monitor","Monitors portfolios for guideline breaches and runs breach workflow",AP,"control",False,"Regulatory Compliance","","service"),
  ("Market Abuse Surveillance","Detects abuse patterns across orders, trades, voice and chat",AP,"control",False,"","","service"),
  ("Financial Promotions Approval","Reviews marketing communications, including anti-greenwashing checks",ALL,"control",False,"","","service"),
  ("Conduct and SM&CR Register","Holds responsibilities map, certifications, conflicts, gifts and breaches registers",ALL,"control",False,"","","database")]),
 ("Financial Crime",[
  ("KYC and Screening","Performs investor, counterparty and deal-party due diligence, sanctions and PEP screening",ALL,"control",False,"","","service")]),
 ("Regulatory and Sustainability Reporting",[
  ("Transaction Reporting","Generates and reconciles regulatory transaction reports for listed trades",AP,"control",False,"Trade and Price Reporting","","service"),
  ("Regulatory Returns Engine","Produces AIFM, fund, prudential and conduct returns to regulators",ALL,"calculation",False,"Regulatory Reporting","ISO 20022 auth (authorities)","service"),
  ("Sustainability and Stewardship Reporting","Produces SDR, climate and Stewardship Code reports",ALL,"calculation",False,"","","service")]),
]),
("Platform: Data, Integration and Controls","Cross-cutting shared services every layer depends on.",[
 ("Reference and Market Data",[
  ("Security Master","Golden source for instruments, identifiers, classifications and terms",ALL,"data",False,"Financial Instrument Reference Data Management","ISIN (ISO 6166); FIGI","database"),
  ("Entity and Party Master","Golden source for issuers, counterparties and clients, keyed by LEI",ALL,"data",False,"Legal Entity Directory","LEI (ISO 17442)","database"),
  ("Market Data Distribution","Acquires, entitles and distributes prices, curves and benchmark data",ALL,"data",False,"Market Information Management","","service")]),
 ("Data and Analytics",[
  ("Enterprise Data Platform","Integrated, governed store for positions, transactions, risk and client data",ALL,"data",False,"","","database"),
  ("Data Governance and Lineage","Catalogue, quality rules, ownership and lineage for critical data",ALL,"control",False,"","","service")]),
 ("Integration and Interoperability",[
  ("Integration and API Gateway","Mediates APIs, events and files between internal and external systems",ALL,"integration",False,"","","service"),
  ("Financial Messaging Gateway","Connects custodians, brokers and administrators over Swift and FIX",ALL,"integration",False,"","Swift ISO 20022 / ISO 15022; FIX","network"),
  ("Desktop Interoperability","Links front-office desktop apps through shared context and intents",AP,"integration",False,"","FDC3","service")]),
 ("Identity and Access",[
  ("Identity and Access Management","Authentication, entitlements, privileged access and public/private-side information barriers",ALL,"control",False,"Party Authentication","","ldap")]),
 ("Controls, Records and Resilience",[
  ("Document and Records Archive","Retains documents, communications and books and records",ALL,"data",False,"Archive Services","","database"),
  ("Operational Resilience Hub","Maps important business services, impact tolerances, scenarios and testing",ALL,"control",False,"","","service"),
  ("Third-Party Oversight","Oversees administrator, custodian, TA and vendor performance and exits",ALL,"control",False,"Contractor and Supplier Agreement","","system")]),
]),
]
out={"title":"UK Asset Manager Functional Architecture: Active, Passive/ETF and Alternatives","layers":[],"links":[],"externals":[],"standards":[],"assumptions":[]}
ids={}; n=0
for li,(ln,lp,groups) in enumerate(layers,1):
  L_={"id":f"L{li}","name":ln,"purpose":lp,"groups":[]}
  for gn,comps in groups:
    G={"name":gn,"components":[]}
    for (nm,does,seg,sor,ext,bian,msg,calm) in comps:
      n+=1; cid=f"C{n:02d}"; ids[nm]=cid
      if len(nm.split())>4 or len(does.split())>14: print("BAD",nm,len(nm.split()),len(does.split()))
      G["components"].append({"id":cid,"name":nm,"does":does,"seg":seg,"sor":sor,"external":ext,"bian":bian,"msg":msg,"calm":calm})
    L_["groups"].append(G)
  out["layers"].append(L_)
ext=[("X01","Retail investors, advisers and platforms","Buy and hold funds via intermediated channels"),
("X02","Institutional clients and consultants","Award and oversee segregated mandates and pooled holdings"),
("X03","Limited partners","Commit capital to private funds; receive calls, distributions, reports"),
("X04","Brokers and trading venues","Execute listed trades; provide research and liquidity"),
("X05","Authorised participants and market makers","Create and redeem ETF units; quote on exchange"),
("X06","Custodian and depositary","Safekeep assets, settle trades, oversee fund on investors' behalf"),
("X07","Fund administrator and transfer agent","Outsourced fund accounting, NAV, register and private fund administration"),
("X08","Index providers","License benchmarks; supply constituents, weights and index events"),
("X09","Market, ESG and reference data vendors","Supply prices, reference data, ESG and research data"),
("X10","Proxy advisers","Supply voting research and vote execution services"),
("X11","Securities lending agent","Lends securities, manages collateral, returns revenue"),
("X12","Banks, prime brokers and lenders","Derivative counterparties, FX, fund financing and deal debt"),
("X13","Deal advisers and portfolio companies","Source and diligence deals; report portfolio performance"),
("X14","Regulators and code bodies","FCA supervision and returns; FRC Stewardship Code; tax authority"),
("X15","Auditors","Audit fund and manager financial statements and controls")]
out["externals"]=[{"id":a,"name":b,"role":c} for a,b,c in ext]
I=lambda s: ids[s]
lk=[("Client CRM","Client Onboarding Workflow","client won",""),
("Client Onboarding Workflow","KYC and Screening","due diligence request",""),
("Mandate and Agreement Repository","Pre-Trade Compliance","coded investment guidelines",""),
("Security Master","Investment Book of Record","instrument and identifier data","ISIN; FIGI; LEI"),
("Portfolio Management System","Order Management System","orders",""),
("Replication and Rebalance Engine","Order Management System","rebalance trade lists",""),
("Order Management System","Execution Management System","routed orders","FIX"),
("Execution Management System","X04","orders and fills","FIX"),
("Execution Management System","Trade Capture and Enrichment","executions","FIX"),
("Settlement and Fails Management","X06","settlement instructions","ISO 20022 sese"),
("X06","Reconciliation Engine","holdings and cash statements","ISO 20022 semt; camt"),
("X06","Corporate Actions and Income","event notifications","ISO 20022 seev"),
("Pricing and Valuation Control","Fund Accounting and NAV","validated prices",""),
("X01","Transfer Agency and Register","subscriptions and redemptions","ISO 20022 setr"),
("X05","Creation and Redemption Platform","create/redeem orders",""),
("Deal Pipeline Management","Deal Modelling and IC","screened deal",""),
("Illiquid Asset Valuation","Partnership Accounting","period-end fair values",""),
("Capital Call and Distribution","LP Investor Portal","call and distribution notices","ILPA CC&D Template"),
("Fee and Carry Engine","LP Reporting Engine","fees, expenses, carry","ILPA Reporting Template"),
("Regulatory Returns Engine","X14","regulatory returns","")]
for f,t,l,s in lk:
  assert len(l.split())<=4
  out["links"].append({"from":f if f.startswith("X") else I(f),"to":t if t.startswith("X") else I(t),"label":l,"std":s})
S=[("BIAN Service Landscape (v10 value chain view)","Cross-check of component names; service domain names used only where visible","https://bian.org/servicelandscape-10-0-0/views/view_51974.html",True),
("FINOS CALM 1.1 meta-schema (node-type enum, relationship types)","Diagram legend: node-type per component; links as interacts/connects; composed-of for layers/groups","https://calm.finos.org/release/1.1/meta/core.json",True),
("FINOS CALM concepts: relationships, flows, controls","Legend vocabulary for flows (ordered transitions over relationships) and controls (requirement-url, config-url)","https://calm.finos.org/core-concepts/relationships",True),
("ISO 20022 business areas (setr, sese, semt, seev, secl, colr, reda, auth)","Fund orders, settlement, holdings statements, corporate actions, collateral, reference data, authority reporting","https://www.iso20022.org/sites/default/files/media/file/ISO20022_BusinessAreas.pdf",True),
("ISO 15022 / ISO 20022 securities mapping over Swift","Settlement and statement messages (e.g. MT 540-543 and sese/semt/seev equivalents)","https://swift.com/node/10286",True),
("FIX protocol (FIX Trading Community)","Order routing, executions and allocations between manager, brokers and venues","https://fixtrading.org/fix-protocol-enables-pre-trade-allocation-global-trading-article/",True),
("Common Domain Model (FINOS with ISDA, ICMA, ISLA)","Optional model for OTC derivatives, repo/bonds and securities lending events","https://www.finos.org/press/finos-launches-common-domain-model-project-in-partnership-with-isda-isla-and-icma",True),
("ILPA Reporting Template v2.0, Performance Templates, Capital Call and Distribution Template","Alternatives LP reporting, fee/carry transparency, call and distribution notices","https://ilpa.org/ilpa-reporting-template/",True),
("LEI (ISO 17442) and ISIN (ISO 6166), GLEIF-ANNA ISIN-to-LEI mapping","Entity and instrument identifiers in party and security masters","https://www.gleif.org/lei-data/lei-mapping/download-isin-to-lei-relationship-files/2021-06-08_isin-to-lei_factsheet_v1.pdf",True),
("FIGI (Object Management Group)","Open instrument identifier, including asset classes lacking ISINs","https://www.openfigi.com/about/figi",True),
("FDC3 (FINOS)","Front-office desktop interoperability via intents and context data","https://fdc3-new.finos.org/docs/fdc3-standard",True),
("ArchiMate (The Open Group)","Optional notation: application components/services/data objects in business, application, technology layers","https://pubs.opengroup.org/architecture/archimate30-doc/chap03.html",True),
("FCA SDR, investment labels and anti-greenwashing rule","Product disclosure, financial promotions and sustainability reporting components","https://www.fca.org.uk/news/press-releases/sustainability-disclosure-and-labelling-regime-confirmed-fca",True),
("FCA Consumer Composite Investments regime (PS25/20)","CCI product summary replacing PRIIPs and UCITS disclosure; rules effective 8 June 2027","https://www.regulationtomorrow.com/2025/12/fca-publishes-final-rules-in-relation-to-consumer-composite-investments/",True),
("UK Stewardship Code 2026 (FRC)","Stewardship reporting: policy and context disclosure plus annual activities and outcomes report","https://www.dechert.com/knowledge/onpoint/2025/8/new-uk-stewardship-code-2026-published-by-the-financial-reportin.html",True),
("FCA Consumer Duty","Value and outcomes assessment, case management, client reporting","",False),
("SM&CR","Conduct and responsibilities register","",False),
("UK UCITS and COLL","Fund rules behind pre/post-trade compliance, liquidity risk, fund accounting","",False),
("UK AIFM regime","Alternatives risk, valuation, depositary and regulatory returns","",False),
("UK MiFIR transaction reporting","Transaction reporting component","",False),
("FATCA and CRS","Investor tax classification in transfer agency and LP onboarding","",False),
("FCA operational resilience rules","Operational resilience hub and third-party oversight","",False)]
out["standards"]=[{"name":a,"used_for":b,"source_url":c,"verified":d} for a,b,c,d in S]
out["assumptions"]=[
"Archetype: UK-authorised manager acting as authorised fund manager for UK UCITS/OEICs and ETFs, and as UK AIFM for closed-ended private funds; segregated institutional mandates also in scope.",
"Fund accounting, NAV, transfer agency and private fund administration are often outsourced; components flagged external=true are commonly run by an administrator, TA, custodian or specialist agent, but the manager keeps oversight and data ownership.",
"Hedge funds, synthetic replication, wealth/advice and the manager's own HR/procurement are out of scope; derivatives appear only as overlay, hedging and collateral.",
"Segment tags: A = Active long-only listed, P = Passive/ETF, L = Alternatives (PE, private credit, real assets); ALL = shared across all three. Components tagged A,P serve both listed businesses.",
"BIAN names come from the publicly visible v10 value chain view; later releases may rename or add domains. BIAN is bank-centric, so mapped names are closest-fit, not exact equivalence; empty means no matching domain was seen.",
"CALM node-type values used are from the CALM 1.1 schema enum (actor, ecosystem, system, service, database, network, ldap, webclient, data-asset). External parties are CALM actor or ecosystem nodes.",
"ISO 20022 entries cite verified business areas (setr, sese, semt, seev, colr, reda, auth, acmt via Swift doc); specific message-level mapping (e.g. setr for fund orders, seev for proxy voting, camt for cash statements) is analyst knowledge and should be confirmed.",
"UK rules named but not verified in this run: Consumer Duty, SM&CR, UK UCITS/COLL, UK AIFM regime, UK MiFIR transaction reporting, FATCA/CRS, operational resilience. SDR, CCI (PS25/20) and Stewardship Code 2026 were verified.",
"Functional system view only: no agentic AI layer, no vendor or product names, no market statistics.",
"Links show 20 representative flows only, not the full integration estate; most components also read from the Platform layer.",
"IBOR sits in Investment Management (decision support); ABOR sits in Operations (official record). Many firms merge them or outsource ABOR to the administrator."]
json.dump(out,open("/home/claude/am-arch/spec.json","w"),indent=1)
segs={}
for l in out["layers"]:
  c=sum(len(g["components"]) for g in l["groups"]); print(l["id"],l["name"],len(l["groups"]),c)
print("total",n,"links",len(out["links"]))
