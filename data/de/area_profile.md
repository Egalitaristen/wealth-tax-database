# Area profile — Germany

First written 2026-10-20 (run R001). Lines marked *[verify]* come from a search summary or a secondary page and were not checked against the primary document.

## 1. Scope
- Area: Germany (Bundesrepublik Deutschland); type: country, federal.
- Depth: **Seed** (SKILL.md 6.1). National level in every layer, the 16 Länder as a register, one Landtag sampled (Berlin). No municipalities loaded.
- Levels of government in scope: national (Bundestag, Bundesrat, Bundesregierung), supranational (German MEPs, not yet searched), regional (16 Länder; Landtage), local left out: municipalities cannot levy a wealth tax and were not sampled.
- Languages to search in: German (main), English.
- Date of first run: 2026-10-20.

## 2. Wealth tax history and live proposals (2010 onwards)
- The Vermögensteuer is **suspended, not repealed**. It has not been levied since 1997 after the Federal Constitutional Court's 1995 ruling on unequal valuation of property; the Kohl government did not pass a new valuation law ([Bundestag motion 21/4029, section I](https://dserver.bundestag.de/btd/21/040/2104029.pdf): "die Vermögensteuer 1997 ausgesetzt"; [Leipziger Zeitung](https://www.l-iz.de/politik/engagement/2025/07/tax-the-rich-startschuss-online-bundestagspetition-wiedereinfuhrung-vermogensteuer-628360)). The yield would go to the Länder (motion 21/4029).
- Bundestag record since 2010 (all read in the Drucksache, `harvest.csv` H0001–H0008):
  - 17th term: Left motion 17/2944 (2010-09-14, 5% above EUR 1m); Left motion 17/8792 (2012-02-29); Left motion 17/10778 (2012-09-25, EU-wide levy); **Greens bill 17/10770 (2012-09-25), a one-off levy of 15% of taxable wealth paid in ten instalments** (roll call on 2013-06-27 reportedly 66 yes, 318 no, 195 abstentions, SPD and Left abstaining *[verify]*).
  - 18th term (2013–2017): not searched.
  - 19th term: Left motions 19/94 (2017-11-22, 5% above EUR 1m) and 19/28908 (2021-04-22, one-off levy of at least EUR 300bn on the richest 0.7%).
  - 20th term: Left motion 20/4307 (2022-11-08, one-off levy), rejected 36 for, 649 against *[verify, per a search summary of the Bundestag text archive]*.
  - 21st term: Left motion 21/4029 (2026-02-06): 1% from EUR 1m rising to 5% at EUR 50m and 12% above EUR 1bn. First reading 2026-03-06 ([Bundestag](https://www.bundestag.de/dokumente/textarchiv/2026/kw10-de-vermoegensteuer-1150522)); the Finance Committee recommended rejection on 2026-10-07, with CDU/CSU, AfD, SPD and Greens voting against the Left ([Drucksache 21/8481](https://dserver.bundestag.de/btd/21/084/2108481.pdf)). The plenary vote is not yet recorded.
- Government: the CDU/CSU–SPD coalition (Chancellor Merz) has no wealth tax in its agreement; a Marvi (SPD) speech in the first reading says the SPD programme provides for it but "nicht diese Koalition". [ZDF](https://www.zdfheute.de/politik/deutschland/klingbeil-steuererhoehung-koalition-spd-100.html) reports the coalition agreement has no tax increases.
- Party positions found: Left (annual tax, plus one-off levies in 2021 and 2022), Greens (2016 congress resolution; 2021 programme 1% above EUR 2m; 2025 programme a global billionaire tax), SPD (2019 congress 1% above EUR 2m; 2025 programme "für sehr hohe Vermögen revitalisieren"). BSW position not read (site blocked). CDU/CSU, FDP and AfD oppose; not recorded.
- Civil society: alliance "Vermögen besteuern jetzt" (statement 2024-10-04, 22 organisations, later 27 plus 12 supporters); earlier alliance "Umfairteilen" (2012–2013); Attac's "Tax the Rich" Bundestag petition (2025); taxmenow and earlier millionaires' appeals (2011, 2021, 2022).
- Polls: Forsa for Stern, July 2024, 62% in favour of a levy on wealth above EUR 1m (34% against) — in `meta.json`.

## 3. Legislatures and where their records are
- **Bundestag.** Drucksachen as PDF: `https://dserver.bundestag.de/btd/<term>/<nnn>/<term><number>.pdf` (for example `21/040/2104029.pdf`). The text archive (`bundestag.de/dokumente/textarchiv/`) has the debate summaries; DIP (`dip.bundestag.de`) has procedures and roll-call votes. The member register with death dates is an open dataset: `https://www.bundestag.de/resource/blob/472878/MdB-Stammdaten.zip` (XML; name, party, birth and death date, constituency by term). Used to check every MP for the alive rule.
- **Bundesrat.** `bundesrat.de` — initiatives on a wealth tax not searched.
- **Landtage.** Each Land has its own portal; Berlin's is `parlament-berlin.de/adosservice/…`. The Left's motion database (`antragsdatenbank-laender.die-linke.de`) lists Landtag motions of the Left but serves a certificate that does not match its host name, so it was not used.
- **European Parliament.** German MEPs not searched.

## 4. Parties
- Bundestag 2025–: CDU/CSU, AfD, SPD, Greens, Die Linke (other seats not checked). BSW is not among the Bundestag groups in the documents read *[verify]*. Party names for the `party` column: `The Left`, `Alliance 90/The Greens`, `SPD`, `BSW`, `CDU/CSU`, `AfD`, `FDP`, `Independent`.
- Programmes read: SPD Regierungsprogramm 2025; Greens 2021 (PDF) and 2025 (web page); Left 2025 easy-read edition. Not read: Left 2025 full programme (die-linke.de answers 403 even to a headless browser), BSW 2025 (bsw-vg.de refuses connections), SPD and Greens older programmes before 2016.

## 5. Government below national level
- 16 Länder, each with a Landtag and government; municipalities below. Whether the Länder may legislate a wealth tax themselves is the question the Left's Berlin motion asks the Senate to have examined by a legal opinion (Drucksache 19/1952).
- The register `geo_units.csv` holds the 16 Länder under the country root, the Bundestag, Bundesrat, Bundesregierung and European Parliament. Official list: the 16 Länder are fixed; names are written in English (Bavaria, Lower Saxony, …).
- **Map:** `boundaries.json` is the Länder map from the Federal Agency for Cartography and Geodesy (VG250/NUTS 1:250,000, Data licence Germany – Attribution – Version 2.0) as redistributed by geoBoundaries gbOpen (CC BY 4.0), simplified. Attribution: © GeoBasis-DE / BKG.
- **Local decision:** no municipalities loaded; sampling not done. A Landtag-level sample (one of 16) found the Left's Berlin motion. Recommendation: do the Landtage next (Bundesrat initiatives and motions are where regional actors act), municipalities only if a sample of the largest cities finds council motions.

## 6. Search terms
| Term | Note |
|---|---|
| Vermögensteuer, Vermögenssteuer | Both spellings occur; the official law is *Vermögensteuergesetz* |
| Vermögensabgabe | One-off levy (Lastenausgleich model, Art. 106(1) no. 5 Basic Law) |
| Millionärsteuer, Millionärssteuer | Left's name for the 5% above EUR 1m design |
| Milliardärssteuer, Milliardärsteuer, Zucman-Steuer, Reichensteuer | Billionaire minimum tax (2% above EUR 100m); *Reichensteuer* is also the top **income** tax rate — read the context |
| Mindeststeuer für Superreiche, Überreichtum | Context terms |
| Erbschaftsteuer, Schenkungsteuer | **Excluded** on their own |
| Vermögensregister | A register is not a tax |
| Grundsteuer, Reichensteuer (Einkommensteuer), Soli | **Excluded** |
- Ambiguous: *Vermögensbesteuerung* can include inheritance tax; *Vermögensabgabe* is sometimes used for a levy on property alone (Lastenausgleich 1952).

## 7. Media
- Opinion pages found fetchable: taz, der Freitag, nd, Jacobin, IPG-Journal, Zeit-linked DIW blogs. Zeit itself answers 403; Süddeutsche, FR and Tagesschau are rejected by the web-search tool but can be fetched by URL. Handelsblatt, FAZ, Spiegel, Welt not tried.
- Commentators found: Ulrike Herrmann (taz) said by a search summary to back a Zucman-style tax *[verify]*; not recorded.

## 8. Registers
- Lobbyregister des Bundestages (`lobbyregister.bundestag.de`): taxmenow is entered as R005191, with 35 members (34 individuals, 1 organisation) as of 2025-09-30 *[verify, search summary]*.

## 9. Known networks
- Alliance "Vermögen besteuern jetzt" (recorded), Netzwerk Steuergerechtigkeit, Attac, Oxfam, DGB unions (ver.di, GEW, IG Metall), social associations (VdK, SoVD, AWO, Paritätischer), church development agencies (Misereor, Brot für die Welt), taxmenow, "Vermögende für eine Vermögensabgabe" (2011), Finanzwende (not recorded: no wealth-tax statement found), Campact (2013 member of Umfairteilen only), Heinrich-Böll-Stiftung and Friedrich-Ebert-Stiftung (not recorded).

## 10. Plan for the next runs
Ordered by expected yield per hour.
1. **Bundestag roll calls and debates (R002).** Roll-call lists (namentliche Abstimmungen), for example 2013-06-27 on 17/10770 (Greens and any SPD or Left members voting yes), plus plenary debates 2010–2026 on the Left motions: speakers who argue for the tax. Also the 18th term (2013–2017), which was not searched.
2. **SPD, Greens and Left individuals (R003).** Statements by leaders and finance spokespeople (Esken, Walter-Borjans, Türmer of the Jusos, Banaszak, Dröge, Reichinnek and van Aken beyond sponsorship), youth wings (Jusos congress decisions, Grüne Jugend, Linksjugend), and the BSW (needs a person with browser access to bsw-vg.de).
3. **Landtage (R004).** The Left's database of Landtag motions and each Landtag portal; then Bundesrat initiatives by Länder governments (Bremen, Hamburg, Berlin, Brandenburg, Thuringia).
4. **Unions and associations in full (R005).** IG Metall, the other DGB unions (IG BCE, NGG, EVG, IG BAU), Paritätischer, AWO, SoVD own statements; church bodies (KAB, Misereor, Brot für die Welt); economists' institutes (IMK, Hans-Böckler-Stiftung, FES).
5. **Economists and academics (R006).** Fratzscher is in; look for Dullien, Rietzler, Truger, Piketty and Zucman statements aimed at Germany, and Bach's own words; academic papers on the German wealth tax (Beckert, Bach, Thiemann). Roster: any open letter of economists.
6. **Media (R007).** Opinion pieces in Spiegel, Zeit, Süddeutsche, FR, nd, Jacobin, taz columnists (Herrmann), podcasts.
7. **Wealthy, business and culture (R008).** taxmenow members (taxmenow.eu answers a bot check), Patriotic Millionaires Germany, "wer hat der gibt", Initiative "Vermögende für eine Vermögensabgabe" members, and cultural figures from the 2011 appeal.
8. **QA (any time).** Second-person verification of the Bundestag sponsor rows and of the 25 roster-only rows; the profiles script needs Wikidata IDs (Wikidata was rate-limiting this environment).
- **Decisions that changed the default workflow:** the Bundestag sponsor lists were processed as bulk lists (SKILL 6.4) using the official member register for the alive check; the party programmes and union pages were read before any search of individuals; no municipal sweep, because municipalities cannot levy the tax.
- **Blocked or unreachable from this environment:** `die-linke.de`, `linksfraktion.de` (403), `bsw-vg.de` (connections refused), `taxmenow.eu` (bot check), `gew.de` and `der-paritaetische.de` (403 to plain clients), `zeit.de` (403), Wikidata and Wikipedia APIs (429).
