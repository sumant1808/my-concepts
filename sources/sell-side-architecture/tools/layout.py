# Layer layout definition: (layer id, band, name, purpose, office, [groups])
# group: (id, name, stages, office, origin, [component ids])
BANDS = [
  {"id":"B1","name":"Pre-trade","kind":"lifecycle","reads":"Client is made ready to trade and is priced"},
  {"id":"B2","name":"Trade","kind":"lifecycle","reads":"Orders are executed, positions held and trades booked"},
  {"id":"B3","name":"Post-trade","kind":"lifecycle","reads":"Trades are confirmed, cleared, settled and serviced"},
  {"id":"B4","name":"Cross-lifecycle services","kind":"cross-lifecycle","reads":"Business services that act on positions at several points of the lifecycle"},
  {"id":"B5","name":"Common services","kind":"common","reads":"Shared data, technology and control services used by every layer"},
]
LAYERS = [
 ("L1","B1","Client coverage and onboarding","Know the client, cover them and make them legally, credit and operationally ready to trade.","Middle",[
   ("G03","Sales and Coverage",["S1"],"Front","S1/G03",["C08","C09"]),
   ("G01","Client Lifecycle",["S0"],"Middle","S0/G01",["C01","C02","C03"]),
   ("G02","Credit and Documentation",["S0"],"Middle","S0/G02",["C04","C05","C06","C07"]),
 ]),
 ("L2","B1","Pricing, structuring and origination","Price, quote and structure secondary-market client business within approved products and suitability.","Front",[
   ("G04","Quoting and Pricing",["S1"],"Front","S1/G04",["C10","C11","C12","C103"]),
   ("G05","Structuring and Suitability",["S1"],"Front","S1/G05",["C13","C14","C15"]),
 ]),
 ("L3","B2","Execution, trading and booking","Control, execute and route orders, run trading positions and book every trade once.","Front",[
   ("G06","Order Management",["S2"],"Front","S2/G06",["C16","C17","C18"]),
   ("G07","Execution and Routing",["S2"],"Front","S2/G07 + S2/G08 (C24)",["C19","C20","C21","C24"]),
   ("G08","Trading Desk",["S2"],"Front","S2/G08",["C22","C23"]),
   ("G09","Trade Capture and Booking",["S3"],"Middle","S3/G09",["C25","C26","C101"]),
 ]),
 ("L4","B3","Confirmation, clearing and margin","Allocate, confirm and agree trades, manage OTC lifecycle, clear eligible trades and exchange margin.","Back",[
   ("G10","Allocation and Affirmation",["S3"],"Middle","S3/G10",["C27","C28"]),
   ("G11","OTC and Structured Confirmation and Lifecycle",["S3"],"Middle","S3/G11",["C29","C30","C31","C102"]),
   ("G15","CCP and Listed Clearing",["S5"],"Back","S5/G15",["C40","C41","C42"]),
   ("G16","Margin and Netting",["S5"],"Back","S5/G16",["C43","C44","C45"]),
 ]),
 ("L5","B3","Settlement and custody","Exchange securities and cash with finality, then safekeep and service the assets held.","Back",[
   ("G17","Settlement Processing",["S6"],"Back","S6/G17",["C46","C47","C48"]),
   ("G18","Market Infrastructure",["S6"],"Back","S6/G18",["C49","C50","C51"]),
   ("G20","Safekeeping and Segregation",["S7"],"Back","S7/G20",["C54","C55","C56"]),
   ("G21","Asset Servicing",["S7"],"Back","S7/G21",["C57","C58","C59"]),
 ]),
 ("L6","B4","Financing and collateral","Finance client and firm positions and move collateral, liquidity and cash wherever the lifecycle needs them.","Cross-cutting",[
   ("G23","Prime Services",["S8"],"Front","S8/G23",["C62","C63","C64"]),
   ("G22","Securities Finance",["S8"],"Front","S8/G22",["C60","C61"]),
   ("G24","Financing Controls",["S8"],"Middle","S8/G24 (less C66)",["C65","C67"]),
   ("P3","Collateral, Liquidity and Cash",["PLATFORM"],"Cross-cutting","PLATFORM/P3 (less C53)",["C80","C81","C52"]),
 ]),
 ("L7","B4","Risk, control and regulatory reporting","Measure risk and P&L, hold limits, report every reportable trade and police conduct across the lifecycle.","Middle",[
   ("G12","Daily Risk and P&L",["S4"],"Middle","S4/G12",["C32","C33","C34"]),
   ("P2","Risk and Limits",["PLATFORM"],"Cross-cutting","PLATFORM/P2",["C77","C78","C79"]),
   ("G13","Regulatory Trade Reporting",["S4","S8","PLATFORM"],"Middle","S4/G13 + S8/G24 (C66) + PLATFORM/P6 (C91)",["C35","C36","C37","C66","C91"]),
   ("P6","Surveillance and Control Room",["PLATFORM"],"Cross-cutting","PLATFORM/P6 (less C90, C91)",["C38","C39","C92","C100"]),
   ("G27","Conduct and Client Assets",["PLATFORM"],"Cross-cutting","PLATFORM/P6 (C90) + PLATFORM/P7 (C94)",["C90","C94"]),
 ]),
 ("L8","B5","Common services","Market data, reference data, data, integration, access, records, resilience and reconciliation shared by every layer.","Cross-cutting",[
   ("G25","Feed Acquisition",["S9"],"Cross-cutting","S9/G25",["C68","C70"]),
   ("G26","Distribution and Licensing",["S9"],"Cross-cutting","S9/G26",["C71","C72","C73"]),
   ("P1","Reference Data",["PLATFORM"],"Cross-cutting","PLATFORM/P1",["C74","C75","C76"]),
   ("P4","Data and Analytics",["PLATFORM"],"Cross-cutting","PLATFORM/P4",["C83","C84","C85"]),
   ("P5","Integration and Messaging",["PLATFORM"],"Cross-cutting","PLATFORM/P5",["C86","C87","C89"]),
   ("P7","Controls and Resilience",["PLATFORM"],"Cross-cutting","PLATFORM/P7 (less C94, C99)",["C93","C95","C96","C97","C98"]),
   ("G28","Reconciliation Services",["PLATFORM"],"Cross-cutting","PLATFORM/P7 (C99) + PLATFORM/P3 (C53)",["C99","C53"]),
 ]),
]
SERVES = {"L6":["L3","L4","L5"],"L7":["L1","L2","L3","L4","L5","L6"],"L8":["L1","L2","L3","L4","L5","L6","L7"]}
