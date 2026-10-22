# Area profile — China

Saved in `data/cn/area_profile.md`. Date: 2026-10-22.

## 1. Scope
- **Area:** China (People's Republic of China); ISO 3166-1 alpha-2: `CN`
- **Type:** Country / sovereign state
- **Depth:** Seed pass (prominent national supporters across legislature, academic economists, think tanks, Party/State Council policy debates, and business figures, with a plan for later runs)
- **Levels in scope:** National, plus 34 province-level regional units (23 provinces, 4 direct-administered municipalities, 5 autonomous regions, 2 special administrative regions), plus 361 prefecture-level units loaded into the geography register and mapped
- **Languages searched in:** Simplified Chinese (zh-CN), Traditional Chinese (zh-HK / zh-TW), English
- **Date of first run:** 2026-10-22 (Run R001)

## 2. Wealth tax history and live proposals (2010 onwards)
China does not have a general recurring net wealth tax (`annual_net_wealth`). Its tax structure is historically reliant on indirect turnover taxes (VAT, consumption tax, corporate income tax). Individual income tax (IIT) accounts for a relatively small share of revenue (~7-8%), and property taxation is predominantly transactional (deed tax, land appreciation tax).

Post-2010 wealth taxation debates in China have centered around three main axes:
1. **The Common Prosperity (共同富裕) and Tertiary Distribution (三次分配) drive (2020-present):** The Central Financial and Economic Affairs Commission (August 2021) and the 20th CPC National Congress (October 2022) emphasized "standardizing the mechanism of wealth accumulation" (规范财富积累机制) and adjusting excessive incomes. While this spurred widespread academic and policy discussion on property and wealth taxes, official government policy has prioritized direct regulation of high-net-worth individuals, cracking down on offshore trusts and cross-border tax avoidance via CRS and individual CFC rules, rather than an immediate standalone domestic net wealth tax.
2. **Exit Tax / Expatriation Tax (弃籍税 / 离境清税):** In 2018, Article 13 of the amended Individual Income Tax Law introduced a requirement that individuals canceling Chinese household registration (户籍) due to overseas emigration must clear taxes beforehand. At the March 2022 National People's Congress (NPC), deputy Chen Jingying formally proposed establishing a full-fledged "exit tax" (弃籍税) on wealthy emigrants, targeting unrealized capital gains and accumulated domestic assets to stop capital flight.
3. **Global Minimum Wealth Tax on Billionaires (2023-2026):** With the EU Tax Observatory's 2024 Global Tax Evasion Report and the G20 2024 Brazilian presidency proposing a 2% coordinated minimum wealth tax on billionaires, Chinese public finance scholars (notably Bai Yanfeng and Yuan Guibo at CUFE and RUC, and Wang Jie and Li Yilin on *The Paper*) have analyzed and advocated for China's engagement in wealth tax valuation methodologies, international coordination, and accumulation of wealth tax collection management experience.

## 3. Legislatures and where their records are
- **National People's Congress (NPC, 全国人民代表大会):** `http://www.npc.gov.cn`. Proposals (建议 / 议案) submitted by deputies during the annual March session ("Two Sessions" / 两会). Full texts of proposals are often summarized by official news agencies (Xinhua, China News Service) or published in ministerial responses on ministry portals (`mof.gov.cn`).
- **Chinese People's Political Consultative Conference (CPPCC, 中国人民政治协商会议):** `http://www.cppcc.gov.cn`. Proposals (提案) by members; texts selectively published on CPPCC and ministry websites.

## 4. Parties
- **Communist Party of China (CPC, 中国共产党):** Governing party.
- **Eight legally recognized democratic parties:**
  - Chinese Peasants' and Workers' Democratic Party (中国农工民主党)
  - China National Democratic Construction Association (中国民主建国会)
  - China Democratic League (中国民主同盟)
  - China Association for Promoting Democracy (中国民主促进会)
  - Jiusan Society (九三学社)
  - Revolutionary Committee of the Chinese Kuomintang (中国国民党革命委员会)
  - China Zhi Gong Party (中国致公党)
  - Taiwan Democratic Self-Government League (台湾民主自治同盟)

## 5. Government below national level
- **Structure:** 34 province-level divisions (regions: provinces, municipalities, autonomous regions, SARs) -> 361 prefecture-level divisions (prefectural-level cities, autonomous prefectures, prefectures, leagues) -> ~2,840 county-level divisions.
- **Taxing powers:** Highly centralized since the 1994 tax-sharing reform (分税制). Local governments receive designated shares of national taxes (VAT, corporate income tax) and specific local taxes, but cannot independently create new tax categories or set wealth tax rates without State Council authorization or NPC legislation.
- **Local decision:** Prefectures are loaded in `geo_units.csv` to ensure comparability and mapped in `boundaries.json`. In the seed pass, local units remain `pending`; sub-national actors are placed at their province or municipality.

## 6. Search terms
- **Primary terms (zh):** `财富税` (wealth tax), `净财富税` (net wealth tax), `资本税` (capital tax), `资本存量税` (capital stock tax), `弃籍税` (exit / expatriation tax), `资产离境税` (asset exit tax), `富豪税` (billionaires / rich tax), `全球最低财富税` (global minimum wealth tax).
- **Ambiguous terms to watch:**
  - `房产税` / `房地产税` (real estate property tax): Excluded on its own under Section 2 unless explicitly framed as or bundled with an overall net wealth/assets tax (`财产税` / `财富税`).
  - `遗产税` / `赠与税` (estate and gift tax): Excluded on its own under Section 2.
  - `共同富裕` (common prosperity) / `三次分配` (tertiary distribution): Broad political concepts; only counts when tied to an included wealth tax design.

## 7. Media
- *The Paper* (澎湃新闻, `thepaper.cn`): Major opinion and think-tank columns.
- *Caixin* (财新网, `caixin.com`): Authoritative financial and macroeconomic coverage.
- *Yicai* (第一财经, `yicai.com`): Business reporting and policy commentary.
- *Study Times* (学习时报): Central Party School theoretical newspaper.
- *Fiscal Science* (《财政科学》) and *Taxation Research* (《税务研究》): Academic journals of CAFS and State Taxation Administration.
- *Aisixiang* (爱思想, `aisixiang.com`): Academic commentary archive.
- *Red Culture Net* (红色文化网, `hswh.org.cn`): Heterodox/Marxist economic publications.

## 8. Registers
- National Enterprise Credit Information Publicity System (`gsxt.gov.cn`)
- Ministry of Civil Affairs Charity in China register (`cishan.chinanpo.gov.cn`)
- Ministry of Finance NPC/CPPCC response disclosure (`mof.gov.cn`)

## 9. Known networks
- Central University of Finance and Economics (CUFE) School of Public Finance and Taxation
- Renmin University of China (RUC) Institute of Public Finance and Taxation
- Chinese Academy of Social Sciences (CASS) Institute of Economics and Institute of Finance and Banking
- World Association for Political Economy (WAPE)
- East China University of Political Science and Law (ECUPL) International Tax Law Center

## 10. Plan for the next runs
- **R002 (NPC/CPPCC Proposals & Ministry Responses):** Systematic sweep of Ministry of Finance published responses to NPC/CPPCC proposals from 2018-2025 touching `财产税` / `弃籍税` / `财富调节`.
- **R003 (Academic Economists & CASS/Universities):** Deepen coverage of academic economists in Peking University, Tsinghua University, Zhejiang University (Center for Research on Shared Prosperity), and SWUFE.
- **R004 (Hong Kong SAR & Macao SAR):** Investigate Legislative Council debates in Hong Kong on capital taxation and family office / wealth management regulatory regimes.
