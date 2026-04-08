# PhytoRx Africa 🌿

**West African Herbal–Drug Interaction Intelligence Platform**

A clinical decision-support prototype that synthesises published ethnopharmacology and pharmacology literature to generate structured herb–drug interaction reports for pharmacists and clinicians in Ghana and West Africa.

---

## 🌐 Live Application

🔗 https://phytorx-africa.streamlit.app/

---

## 🚀 Key Features

* 🔍 **Herb–Drug Interaction Checker** (20 priority West African herbals)
* ⚠️ **Risk Classification** (Severe / Moderate / Mild / None / Unknown)
* 🧠 **Mechanism-Aware Output** (CYP450, pharmacodynamic, transporter effects)
* 📊 **Evidence Transparency** (explicit quality grading + references)
* 🛡️ **Anti-Hallucination Engine**

  * Forces **INSUFFICIENT EVIDENCE** when data is lacking
  * Uses **APPROXIMATE flag** for uncertain citations

---

## 🛠️ Setup

```bash
# 1. Clone repository
git clone <your-repo-link>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run app
streamlit run app.py
```

---

## 🧪 Usage

1. Enter your Anthropic API key in the **API Configuration** panel
2. Select or input a **drug name**
3. Select a **herbal preparation** (from curated West African list)
4. Click **Check Interaction**
5. Review structured output:

   * Severity
   * Mechanism
   * Clinical management
   * Evidence quality
   * References

---

## 🌿 Coverage

### Herbals (20)

Cryptolepis sanguinolenta · Morinda lucida · Xylopia aethiopica ·
Azadirachta indica · Annona muricata · Khaya senegalensis ·
Momordica charantia · Ocimum gratissimum · Carica papaya ·
Vernonia amygdalina · Phyllanthus amarus · Lippia multiflora ·
Senna alata · Alstonia boonei · Griffonia simplicifolia ·
Securidaca longipedunculata · Cassia sieberiana · Blighia sapida ·
Tetrapleura tetraptera · Kalanchoe pinnata

---

### Drug Categories (8)

Antimalarials · Antiretrovirals · Antidiabetics ·
Antihypertensives · Anticoagulants/Antiplatelets ·
Antibiotics · CNS/Psychiatric · Cardiovascular

---

## 🧠 Architecture

* **Frontend:** Streamlit (custom CSS: DM Serif Display + DM Sans)
* **LLM Engine:** Claude (claude-opus-4-5)
* **Output Format:** Structured JSON interaction cards
* **Core Design Principle:**

  > *Never fabricate evidence — explicitly declare uncertainty*

---

## 📊 Evidence Tiers

| Colour | Severity | Example                                        |
| ------ | -------- | ---------------------------------------------- |
| 🔴     | Severe   | Griffonia + MAOIs (serotonin syndrome)         |
| 🟠     | Moderate | Phyllanthus + ARVs (CYP3A4 interaction)        |
| 🟡     | Mild     | Momordica + metformin (additive hypoglycaemia) |
| 🟢     | None     | No documented interaction                      |
| ⚪      | Unknown  | Insufficient evidence                          |

---

## ⚠️ Clinical Disclaimer

This tool synthesises published literature to support clinical decision-making.
It does **not replace professional judgement**.

* Evidence quality is explicitly stated
* Outputs should be interpreted within clinical context
* Always verify high-risk interactions independently

---

## 🚧 Future Development

* Multi-herb product interaction engine (bitters/tonics)
* Patient medication profile input (polypharmacy analysis)
* Ghana FDA herbal product integration
* SHAP-style explainability for interaction risk
* Offline clinical deployment version

---

## 👨‍⚕️ Target Users

* Pharmacists
* Clinicians
* Public health researchers
* Regulatory bodies (FDA Ghana context)

---

## 🌍 Vision

To build the **first clinically reliable herb–drug interaction intelligence system for African traditional medicine**.
