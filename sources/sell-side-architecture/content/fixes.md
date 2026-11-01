# Fixes applied to review.md findings (v2)

Backup of v1: /home/claude/sell-arch-canvas/backup-v1/. Patch scripts: /home/claude/sell-arch-canvas/tools/apply_fixes.py and fix_xref.py (one-shot, already run).

R1 applied: C99 added to P7; links C83 to C99 and C41 to C99; EX P7 set; P7 now 3 columns (see R22).
R2 applied: C100 added to P6 with two links; EX P6 'Surveillance, control room, best ex, STORs'.
R3 applied: regs appended on C35, C37, C90, C62, C97, C78; one unverified standards row added.
R4 applied: EX G13 'MiFIR, EMIR, CFTC, public'; link C25 to C36 replaces C29 to C36; C31 to C36 added; C36 does updated.
R5 applied: C52 and C87 fields, notes sentence, Swift MT row relabelled, CBPR+ row added as verified (URL from review).
R6 applied: X17 to X21 added and placed in SIDES as specified; one-page external line rebuilt (see R21).
R7 modified: chip text as instructed by the owner; limitations reworded neutrally ("not checked against the source for this draft, validate before external use"); lims[7] and footer say AI-reviewed, not practitioner-validated. EU T+1 row renamed to Regulation 2025/2075 and verified (aoshearman URL); DORA row renamed and verified (natlawreview URL); UK T+1 source changed to gov.uk (already verified). No other row verified.
R8 applied: C101 added to G09 with BIAN "Commissions" (taken from review, not re-checked here); EX G09 'Capture, booking, fees'.
R9 applied: C46/C06 FIX fields, link 11 std, C41 iso20022, C43 and C48 regs, C48 does, UMR row renamed. Matrix counts recomputed.
R10 applied: C38 and C39 moved to P6, G14 deleted, P6 renamed in spec; slide label unchanged.
R11 applied: C69, C82, C88 deleted; link C80 to X14; EX G25, P3, P5 set (P3 text modified, see R22); notes external list updated. G25 is no longer dashed. G18 stays dashed (C49 and C50 are FMI touchpoints, 2 of 3).
R12 applied: C56 renamed, regs emptied; C94 does extended.
R13 applied: C79 renamed to XVA and Counterparty Exposure, ac ALL, Basel regs; FRTB row extended; EX P2 set.
R14 modified: C78 skipped (main session patched it to 'Market Risk; Economic Capital' and asked to keep it). C98 bian blanked, C81 set to Corporate Treasury, notes updated for C83 and C59.
R15 applied: C102 added to G11; C31 ac; G11 renamed; EX G11 set, slide label kept.
R16 modified: C103 added; C22 and C97 does updated; EX G04 'RFQ, streaming, online channels' (the review string 'e-channels' broke at the hyphen on the slide).
R17 applied: C37 renamed with SI regime; C14 regs; link C37 to X19; transparency row renamed.
R18 applied: all eight links added; flows now reach externals. Links sorted by thread, 50 in total.
R19 applied: S1 purpose updated; name Origination kept; footer clause added.
R20 modified: fixed 3-slot grid on every stage; 2-group stages (S0, S4, S5, S6, S7, S9) get a tinted hook box with a cost or fees label; S6 added because R22 left it with 2 groups; hooks reworded from spec value text; 3-group stages unchanged.
R21 modified: EX G05, G20, G10 applied; external line is four labelled runs with counts and short names, on two lines (full names stay on the detailed board).
R22 applied: G19 moved into P3 (renamed Collateral, Liquidity and Cash), P3 2 columns, P7 3 columns. Slide P3 label 'Collateral, Liquidity, Cash'.
R23 applied: C61, C27, C19, C40 changed; C42 GCM clause skipped (bank role not assumed).
R24 applied: C42 does updated; EMIR client clearing tag already present.
R25 applied: chevron text top-aligned; chevron height 88 and padding 8/6 so two-line names fit without clipping.
R26 applied: notes wording on vendor names.
R27 applied: recording tag on C39 and C97; unverified standards row added.
R28 applied: SHORT S9 already 'Market data'; aria-label and footer say stage 9 feeds every stage; S9 purpose starts 'Feeds every stage:'.
R29 skipped: no change requested; Swift MT row stays unverified.
R30 applied: C25 does updated.
R31 skipped: no fix needed; hygiene re-checked after rebuild.
R32 skipped: no fix needed; the one stale verified item was handled under R7.

Narrative suggestions: only the economics hook line (R20) and wording fixes were applied. No retitle, no T+1 tags, no thread markers, no mutualisation boundary, no asset-class strip, no Level 0 slide.

## New risks
- Detailed board grew from 3200 x 5096 to 3200 x 6334. S3 is now the tallest stage column (C101, C102 added), about 700 px below S0, so column bottoms are still uneven.
- Platform groups are drawn at the tallest group height (P6, 6 cards), so P1, P2 and P4 are about 40% blank.
- BIAN "Commissions" (C101) comes from the review and was not re-checked against v10 here.
- UK bond consolidated tape row is marked verified from the FCA URL named in the review; the 22 June 2026 date was not independently re-read.
- Moving cash and payments out of Settlement changes how a Settlement audience reads the stage; the flow C44 to C52 still links margin to payments.
- 19 of 41 standards remain unverified, including the new US broker-dealer, recording and MAR rows. Swift MT numbers remain analyst knowledge.
- The 18 px one-page external line is dense; full names are on the detailed board only.
