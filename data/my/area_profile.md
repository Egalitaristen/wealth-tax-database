# Area profile — Malaysia

Updated: 2026-10-23 (R001 seed pass).

## 1. Scope
- **Area**: Malaysia (`MY`); sovereign federation in Southeast Asia consisting of 13 States and 3 Federal Territories.
- **Depth**: Seed pass with wide sweeps across all layers.
- **Levels in scope**:
  - National: Federal Parliament (Dewan Rakyat, Dewan Negara), political parties, central trade unions, think tanks, academic economists, and civil society organisations.
  - Regional: 13 States (*Negeri*) and 3 Federal Territories (*Wilayah Persekutuan*) loaded in `geo_units.csv` (`G0005` to `G0020`).
  - Local: 144 administrative districts (*Daerah*) loaded in `geo_units.csv` (`G0021` to `G0164`), matched directly to official Department of Statistics Malaysia (DOSM) codes via OCHA Common Operational Datasets (cod-ab-mys).
- **Languages searched**: Malay (Bahasa Melayu), English.
- **Date of first run**: 2026-10-23 (R001).

## 2. Wealth tax history and live proposals (2010 onwards)
- **Tax structure context**: Malaysia has never had an annual recurring tax on net wealth. Estate duty (inheritance tax) was abolished in 1991 under the Estate Duty (Repeal) Act 1991. The Goods and Services Tax (GST) introduced at 6% in April 2015 was repealed in September 2018 under the Pakatan Harapan government and replaced with the Sales and Services Tax (SST).
- **The Wealth Tax Debate**:
  - The debate over a wealth tax (*cukai kekayaan*) in Malaysia is driven by stark wealth inequality: according to Forbes 2024–2026 reports, Malaysia's top 50 richest tycoons hold over RM400 billion in collective assets, equivalent to the federal budget.
  - Successive governments (Pakatan Harapan under Mahathir Mohamad/Lim Guan Eng 2018–2020, Perikatan Nasional under Muhyiddin Yassin 2020–2021, Ismail Sabri Yaakob 2021–2022, and the Madani government under Anwar Ibrahim 2022–present) have formally resisted a net wealth tax, citing concerns over capital flight, asset valuation of illiquid family businesses, and the goal of positioning Malaysia as a regional wealth hub. Instead, the government introduced targeted proxy taxes: a 2% dividend tax on annual dividend income exceeding RM100,000 (introduced in Budget 2025/2024), capital gains tax on unlisted shares (effective March 2024), and high-value goods tax proposals.
  - **Proposals**:
    - **Parti Sosialis Malaysia (PSM)**: Longest-standing advocate. Authored a detailed graduated wealth tax proposal in its post-COVID recovery framework (July 2020) proposing a 2% rate on assets between RM1bn and RM2bn, graduating up to 10% on assets over RM30bn. Reaffirmed in party congress resolutions (August 2026).
    - **Dewan Rakyat parliamentary speeches**: Backbench and opposition MPs have formally proposed wealth taxes during budget debates. In October 2025 (Supply Bill 2026), Ahmad Saad Yahaya (PAS MP for Pokok Sena) proposed an explicit 2.5% wealth tax on the ultra-rich based on zakat principles and Argentina's wealth tax experience. Hassan Abdul Karim (PKR MP for Pasir Gudang) called during the same budget debate for a wealth tax on multimillionaires and billionaires possessing assets above US$1m. Earlier in October 2019, Mohd Khairuddin Aman Razali (PAS MP for Kuala Nerus) called for a 2.5% tax on stock wealth and corporate reserves.
    - **Civil society & NGOs**: Monitoring Sustainability of Globalisation (MSN, led by V. Aishwarya) campaigned for a 2% wealth tax on the top 50 richest Malaysians to raise RM8.3 billion to fund school meals and green social housing. Former MP Charles Santiago repeatedly campaigned for a 2%–2.5% wealth tax on the 50 richest tycoons to raise RM10 billion for public healthcare. Dr. Kua Kia Soong published detailed proposals in Aliran for a 2% wealth tax on the top 100 or a graduated 1%–1.5% tax on net wealth over RM100m/RM500m.
    - **Economists**: Dr. Jomo Kwame Sundaram (Khazanah Research Institute) and Ng Sze Fung (REFSA) have published analyses advocating wealth taxes as necessary to cure structural wealth concentration and expand fiscal space for public goods.

## 3. Legislatures and where their records are
- **Parliament of Malaysia (Parlimen Malaysia)**:
  - Dewan Rakyat (House of Representatives) and Dewan Negara (Senate).
  - Hansards / Official Reports (*Penyata Rasmi*): Published as searchable PDFs on [parlimen.gov.my](https://www.parlimen.gov.my/hansard-dewan-rakyat.html).
  - Written Answers (*Jawapan Bertulis*): Published on [parlimen.gov.my/jawapan-lisan-dewan-rakyat.html](https://www.parlimen.gov.my).
  - Parliamentary Repository: [repositori.parlimen.gov.my](https://repositori.parlimen.gov.my).
- **State Legislative Assemblies (Dewan Undangan Negeri - DUN)**:
  - 13 state assemblies. While states do not have constitutional jurisdiction over income or direct wealth taxes (Federal List under the Ninth Schedule of the Federal Constitution), state politicians and ADUNs debate national economic policies and cost of living.

## 4. Parties
- **Parti Sosialis Malaysia (PSM)**: Core supporter. Formal policy adoption in the 28th National Congress Resolutions (August 2026) and alternative budget proposals.
- **Pakatan Harapan (PH)**: Coalition includes PKR, DAP, and Amanah. Party backbenchers (Hassan Abdul Karim of PKR, former MP Charles Santiago of DAP) have strongly pushed for a wealth tax, though the coalition leadership in government (Anwar Ibrahim, Lim Guan Eng, Liew Chin Tong) has opted for targeted dividend and capital gains taxes rather than a net wealth tax.
- **Perikatan Nasional (PN)**: Coalition includes PAS and Bersatu. MPs like Ahmad Saad Yahaya (PAS) have advocated for a 2.5% wealth tax on Islamic zakat-aligned principles during budget debates.
- **MUDA (Malaysian United Democratic Alliance)**: Pushed for windfall taxes on glove manufacturers and inheritance/capital gains taxes, but has not formally proposed a recurring net wealth tax (`exclusions.csv`).

## 5. Government below national level
- **Structure**:
  - Federal level -> 13 States (*Negeri*) + 3 Federal Territories (*Wilayah Persekutuan*).
  - Local level -> 144 administrative districts (*Daerah*), functioning as administrative divisions under district offices (*Pejabat Daerah*) and local authorities (*Pihak Berkuasa Tempatan* - City Councils / Municipal Councils / District Councils).
- **Taxation powers**: Under the Ninth Schedule of the Federal Constitution of Malaysia, direct and indirect taxation (income tax, company tax, customs, excise) is strictly federal. States only collect land tax (*cukai tanah*), quit rent, and forest revenues; local authorities collect local assessment rates (*cukai pintu* / *cukai taksiran*). Therefore, any wealth tax is strictly a federal legislative matter, explaining why subnational advocates always lobby the federal Ministry of Finance and Parliament.
- **Geography register & Boundaries**:
  - Register generated down to the 144 administrative districts with official P-codes from Department of Statistics Malaysia (DOSM) via OCHA Common Operational Datasets (`cod-ab-mys`), under CC BY-IGO.
  - Map built with `topo_to_boundaries.py` and `merge_boundaries.py` yielding 144 district units and 16 state/territory outlines.

## 6. Search terms
- **Malay**:
  - Included: `cukai kekayaan`, `cukai aset bersih`, `cukai maha kaya`, `cukai bilionair`, `cukai harta kekayaan`.
  - Ambiguous / Excluded: `cukai harta pusaka` (estate duty / inheritance tax), `cukai keuntungan modal` (capital gains tax), `cukai taksiran` / `cukai pintu` (local property assessment rates), `cukai tanah` (quit rent), `cukai durian runtuh` (windfall profit levy).
- **English**:
  - Included: `wealth tax`, `net wealth tax`, `billionaire tax`, `tax on the super-rich`, `taxing wealth`.
  - Excluded: `inheritance tax`, `estate duty`, `capital gains tax`, `luxury goods tax`, `windfall tax`.

## 7. Media
- **News Portals**:
  - *Malaysiakini* (bilingual: English, Malay): In-depth reporting on progressive taxation, parliamentary debates, and civil society statements.
  - *Free Malaysia Today (FMT)*: Extensive coverage of political statements (Hassan Karim, Charles Santiago) and economic analyses.
  - *The Edge Malaysia*: Deep financial and policy analysis of government budgets, tax reform committees, and Ministry of Finance stances.
  - *Scoop.my* / *The Vibes*: Independent coverage of public policy podcasts and commentaries.
  - *Aliran Kesedaran Negara*: Progressive reform civil society portal publishing in-depth articles by Dr. Kua Kia Soong and Raveen Jeyakumar.
  - *Sosialis.net*: Official publication portal of PSM containing full text of alternative budgets and congress resolutions.
  - *Astro Awani*, *Berita Harian*, *Utusan Malaysia*, *Sinar Harian*: Mainstream Malay-language dailies covering ministerial replies and parliamentary sessions.

## 8. Registers
- Parliament of Malaysia: [parlimen.gov.my](https://www.parlimen.gov.my)
- Registry of Societies (ROS): [ros.gov.my](https://www.ros.gov.my)
- Companies Commission of Malaysia (SSM): [ssm.com.my](https://www.ssm.com.my)

## 9. Known networks
- **Tax justice / economic justice coalitions**:
  - Monitoring Sustainability of Globalisation (MSN)
  - Aliran Kesedaran Negara
  - Gabungan Bertindak Malaysia (GBM)
  - Bersih
  - Suaram (Suara Rakyat Malaysia)
  - MTUC (Malaysian Trades Union Congress)
  - Research for Social Advancement (REFSA)
  - Khazanah Research Institute (KRI)

## 10. Plan for the next runs
- **Run R001 delivered**:
  - Complete 164-unit geography register (1 country root, 3 national institutions, 16 states/federal territories, 144 districts) with CC BY-IGO boundaries map.
  - 15 supporters (12 persons, 3 organisations) across politicians (PAS, PKR, DAP, PSM), think tanks (REFSA), NGOs (MSN), academics (Dr. Kua Kia Soong, Dr. Jomo Kwame Sundaram, Ng Sze Fung), and columnists/campaigners.
  - 19 verified evidence items (9 Grade A, 6 Grade B) with 100% of checkable web quotes confirmed verbatim.
  - 9 exclusions documented (ministers, economists proposing alternate taxes, inheritance tax advocates).
- **Next runs (R002+)**:
  1. *Dewan Rakyat & Dewan Negara Hansard sweep*: Full-text keyword searches across 2018–2024 Hansard PDF repositories for additional MPs who raised wealth tax queries or budget amendments.
  2. *Trade Unions*: MTUC, CUEPACS, and affiliate unions' budget memorandums submitted to the Ministry of Finance.
  3. *State Assemblies (DUN)*: Sample motions and questions in the Selangor and Penang state legislative assemblies.
  4. *Civil Society Coalitions*: Follow up on signers of NGO memoranda on Budget 2024/2025/2026.
