# Malaysia: wealth tax debate, sources and layers

Notes from the seed pass (R001, October 2026). Check that URLs still resolve before relying on them.

## Levels and the geography register

| Level (`level`) | Units | Notes |
|---|---|---|
| national | Parliament of Malaysia (Dewan Rakyat, Dewan Negara), Government of Malaysia | Direct and indirect taxation is exclusively a federal power under the Ninth Schedule of the Federal Constitution |
| region | 13 States and 3 Federal Territories | Codes: OCHA/DOSM P-codes (`MY01` to `MY17`), parent `G0001` |
| local | 144 administrative districts (*daerah*) | The map tier. Codes: official DOSM / OCHA P-codes (`MY0101` to `MY1709`), parented to their respective states |

**Map:** `data/my/boundaries.json` is generated from the Department of Statistics Malaysia (DOSM) boundaries republished under **CC BY-IGO** by OCHA via the Common Operational Datasets on HDX (`data.humdata.org/dataset/cod-ab-mys`). Districts carry official DOSM P-codes; states carry region codes. Converted with `topo_to_boundaries.py` and merged with `merge_boundaries.py`.

## What worked and what to watch

- **Dewan Rakyat debates:** The Parliament of Malaysia publishes official Hansard PDFs (*Penyata Rasmi*) on `parlimen.gov.my`. Budget debates on the annual Supply Bill (*Rang Undang-Undang Pembekalan*) provide formal parliamentary speeches:
  - Ahmad Saad Yahaya (PAS MP for Pokok Sena, DR 16.10.2025 p. 83) proposed an explicit 2.5% wealth tax on the ultra-rich based on zakat principles and Argentina's emergency wealth tax.
  - Hassan Abdul Karim (PKR MP for Pasir Gudang, DR 28.10.2025) argued for a wealth tax on multimillionaires and billionaires above US$1m.
  - Mohd Khairuddin Aman Razali (PAS MP for Kuala Nerus, DR 16.10.2019 p. 98) proposed a 2.5% wealth tax on stock holdings and corporate reserves.
- **Parties:** Parti Sosialis Malaysia (PSM) is the principal dedicated wealth-tax party in Malaysia, adopting wealth taxation at its 28th National Congress (August 2026) and in its alternative economic recovery budgets (July 2020) authored by Dr. Michael Jeyakumar Devaraj.
- **Think tanks and academics:**
  - Dr. Kua Kia Soong (former Petaling Jaya MP, sociologist, SUARAM co-founder) published detailed blueprints in Aliran (April and July 2026) with explicit designs (2% on top 100 or graduated 1%–1.5% above RM100m/RM500m).
  - Research for Social Advancement (REFSA) published policy briefs defending high-exemption wealth taxes against growth and innovation critiques.
  - Dr. Jomo Kwame Sundaram (Khazanah Research Institute, former UN Assistant Secretary-General) advocated for wealth and excess profit taxes to fund healthcare and public services.
- **Civil society:** Monitoring Sustainability of Globalisation (MSN) campaigned for a 2% wealth tax on Malaysia's top 50 billionaires to raise RM8.3 billion for free school meals and social housing.
- **Exclusions:**
  - Watch for *cukai harta pusaka* / *cukai pewarisan* (inheritance tax / estate duty), which was abolished in Malaysia in 1991 and is often proposed by consumer groups like CAP. Estate duty is excluded under the core definition.
  - Watch for *cukai durian runtuh* (windfall profit levy) and capital gains tax on unlisted shares, which are corporate or transactional taxes and excluded on their own (e.g. Syed Saddiq).
  - Both Lim Guan Eng (Finance Minister 2018–2020) and Anwar Ibrahim (Prime Minister & Finance Minister 2022–present) have formally rejected a net wealth tax, citing capital flight concerns and opting instead for dividend tax and targeted subsidy rationalisation.
