# Review fixes applied (R1-R35)

R1 applied: L5 Delegate Oversight group (C80 moved from L6, new C81, C82), link C49 to C81, notes reworded.
R2 applied: A blue #1F4E8C, P teal #0B6E70, L amber in both builders; legend rows reworded.
R3 applied: C83, C84 added; C49 and C59 text changed; CASS added to standards as not verified.
R4 applied: C85 added; C38 text changed; X18, X19 added; links C66 to X19, C85 to X19; UK EMIR and SFTR added as not verified.
R5 applied: C86, C87, X17 added; link X17 to C47.
R6 applied: curated GROUP_EX in build_summary.py; strings for merged or moved groups adapted (Clients, ETF Primary, Private Fund Admin, Financial Crime, Integration, Enterprise Finance); fit measured with Inter proxy, 0 of 31 over two lines.
R7 applied: COMP_SHORT values changed as listed. The slide now renders GROUP_EX, so COMP_SHORT is kept only for reference and a coverage assert.
R8 modified: no rule marked verified; chip reads "Draft · analyst design · AI-reviewed, not practitioner-validated"; limitations bullet reworded as instructed; the "check before showing a client" line removed from board and notes.
R9 applied: X06 renamed Custodian, X16 added, link X16 to C82, X16 in RIGHT list at L4, summary strip split into Custodian and Depositary or trustee.
R10 applied: C39 external false and renamed Securities Lending Programme Oversight.
R11 applied: C57 renamed and tagged A,P; C61 tagged ALL (text now mentions LPA restrictions); C12 text; C17 note added to notes and assumption 11.
R12 applied: group renamed Portfolio Management; GROUP_LABEL key updated.
R13 applied: C43 A,P, new text, bian empty; C55 bian Financial Accounting; links C43 to C49 and C17 to C44.
R14 applied: C49 carries both fund BIAN names, C50 empty; C66 bian Regulatory Reporting (name from review); C61 Guideline Compliance; notes updated (Financial Market Research added; Trade and Price Reporting recorded as tried and dropped). BIAN count now 37 of 90.
R15 applied: auth moved to C66, C67 msg changed, acmt moved to C50, C09 FinDatEx msg, C48 GIPS msg, secl removed from standards row; FinDatEx and GIPS added as not verified.
R16 modified (option b): notes, assumption 6, legend note, CALM standards rows reworded: vocabulary only, not a CALM document, flows and controls not modelled.
R17 applied: C88 added to Trade Support and Settlement.
R18 applied: C89 added to Compliance and Surveillance; link C89 to C30.
R19 applied: C90 added; C34 renamed Basket (PCF) and iNAV Publication.
R20 applied: four links added; flows panel grouped under three headings; each link has a flow key (T, F, C). Second-guess: C21 to C23 (screened deal) sits under "Life of a capital call" and C67 to X14 and X05 to C33 under "Life of a fund deal" because no better heading exists.
R21 applied: layer label 19px/24px, padding 8px 6px.
R22 applied: no chip when a group is shared by all three; legend text "No letter: shared by all three".
R23 modified: notes claim reworded as instructed; no traceability.json built.
R24 applied: group moved to L6 and renamed Enterprise Finance; C55 text adds regulatory capital and ICARA. L4 now has 5 groups.
R25 applied: C09 merged into Client and Distributor Management; C77 merged into Integration, Access and APIs. C65 stays as Financial Crime. Rows now have 4, 6, 5, 5, 6, 5 groups.
R26 applied: CCI transition added; ILPA name updated with a note that the dates come from a secondary source; v2.0 not claimed for the CC&D template.
R27 applied: build.py writes both boards with the required geometry and titles (computed component count).
R28 applied: "and securities lending" removed from notes.
R29 skipped: FDC3 URL unchanged and unchecked (noted in notes.md).
R30 applied: Verified badge, flow numbers and assumption numbers now NAVY.
R31 modified: footer added to the detailed board; no other change.
R32 applied: TINT L border #8A5600.
R33 applied: Summary lang en-GB.
R34 applied: C45, C13, C04 text extended.
R35 skipped: nothing to fix.
Narrative: only the headline applied (Summary h1 and subtitle). Spine, thread overlays, 2027 callout and Level 0 not built.

## New risks
- Only layout is estimated: fit used Inter as a proxy for DM Sans and nothing was rendered in the canvas.
- Enterprise Finance now sits in the Platform row, whose slide label still reads "Platform: Data and Controls".
- Seven UK rules plus CASS, EMIR/SFTR, FinDatEx and GIPS are all unverified (11 of 26 standards).
- New components' wording (C81-C90) is taken from the review, which marks several statements as reviewer knowledge and unverified.
- Flow assignment to the three headings is a judgement for six links.
- Service providers strip on the slide is nearly full (about 406 of 436 px by the Inter proxy).
- The Active-only legend entry on the slide is not shown because no group is Active-only.
- Main board is now 6732 px tall; Key flows panel is long (32 rows).

## Follow-up: one-page grouping (owner instruction)
- Each Summary row is now ordered in work-flow order in two functional clusters, separated by a thin vertical divider (wider gap, no extra type). Boxes in a row have equal width and height; widths are computed per row. Grouping is defined by CLUSTERS in build_summary.py; the spec and detailed board are unchanged.
- Platform row label now reads "Platform: Data, Finance and Controls" (names finance, so the label is true).
- Legend left as one slim line. Re-checks: balanced markup, node --check, min font 18 px, no dashes, 0 of 31 boxes over two lines (Inter proxy).
- Residual risk: widths differ between rows (4, 6, 5, 5, 6, 5 boxes), so columns do not line up across rows; no sub-headings were added because the 1080 px height has no room.

## Follow-up 2: one-page left strips removed, four splits
- Summary: left stakeholder strips (clients and distributors, LPs and investors, regulators and auditors, and the trade repositories line) removed. X01, X02, X03, X14, X15, X19 therefore no longer appear on the one-pager; they remain on the detailed board. Layer labels start at x=24.
- Splits in spec.json (components moved, none added): Distribution Data and Platforms (C09), Fund Dealing and Register (C50, C83; Fund Accounting and Transfer Agency renamed Fund Accounting and NAV, C49 only), Compliance Monitoring (C61, C62, C89) vs Conduct and Promotions (C63, C64), Identity and Access (C77; Integration group renamed Integration and Interoperability). Groups now 35; components still 90. Detailed board rebuilt: height 6717, title "Detailed view (90 components)".
- Summary grid: one 7-slot grid (box width 208, gap 10) shared by all rows, two clusters per row with a divider in the gap, empty slots at row ends. Boxes per row 5, 6, 5, 6, 7, 6.
- Example for Compliance Monitoring dropped "insider lists" to stay at two lines.
