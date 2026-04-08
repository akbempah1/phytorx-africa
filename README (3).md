# PhytoRx Africa 🌿
**West African Herbal–Drug Interaction Intelligence**

A Streamlit prototype that synthesises published ethnopharmacology literature 
to deliver structured herb-drug interaction reports for pharmacists and clinicians 
in Ghana and West Africa.

---

## Setup

```bash
# 1. Clone / copy files into a folder
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
streamlit run app.py
```

## Usage

1. Enter your Anthropic API key in the **API Configuration** expander
2. Select or type a **drug name**
3. Select the **herbal preparation** from the dropdown (20 priority West African herbals)
4. Click **Check Interaction**
5. Review the structured interaction card — severity, mechanism, management, evidence quality, references

## Coverage

**Herbals (20):** Cryptolepis sanguinolenta, Morinda lucida, Xylopia aethiopica, 
Azadirachta indica, Annona muricata, Khaya senegalensis, Momordica charantia, 
Ocimum gratissimum, Carica papaya, Vernonia amygdalina, Phyllanthus amarus, 
Lippia multiflora, Senna alata, Alstonia boonei, Griffonia simplicifolia, 
Securidaca longipedunculata, Cassia sieberiana, Blighia sapida, 
Tetrapleura tetraptera, Kalanchoe pinnata

**Drug categories (8):** Antimalarials · Antiretrovirals · Antidiabetics · 
Antihypertensives · Anticoagulants/Antiplatelets · Antibiotics · CNS/Psychiatric · 
Cardiovascular

## Architecture

- **Frontend:** Streamlit with custom CSS (DM Serif Display + DM Sans)
- **Engine:** Claude claude-opus-4-5 with structured anti-hallucination prompt
- **Output:** JSON interaction cards with severity, mechanism, evidence quality, references
- **Anti-hallucination:** LLM instructed to state INSUFFICIENT EVIDENCE rather than fabricate; 
  APPROXIMATE flag required for uncertain citations

## Evidence Tiers

| Colour | Severity | Example |
|--------|----------|---------|
| 🔴 | Severe | Griffonia + MAOIs (serotonin syndrome) |
| 🟠 | Moderate | Phyllanthus + ARVs (CYP3A4 MBI) |
| 🟡 | Mild | Momordica + metformin (additive effect) |
| 🟢 | None | No documented interaction |
| ⚪ | Unknown | Insufficient evidence |

## Disclaimer

This tool synthesises published literature to support clinical decision-making. 
It does not replace professional judgement. Evidence quality is explicitly stated 
in every report.
