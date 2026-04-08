import streamlit as st
import anthropic
import json
import re
from datetime import datetime

st.set_page_config(page_title="PhytoRx Africa", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
:root {
    --green-deep:#0d3b2e; --green-mid:#1a5c45; --green-soft:#2d7a5f;
    --gold:#c8a84b; --gold-light:#e8cc80; --cream:#f5f0e8; --cream-dark:#ede7d9;
    --text-dark:#1a1a18; --text-mid:#3d3d38; --text-light:#6b6b60;
    --red:#c0392b; --orange:#d35400; --amber:#d4a017; --emerald:#1e8449;
    --grey:#808080; --card-bg:#ffffff; --border:#ddd8cc; --blue:#1a6ea8;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background:var(--cream);color:var(--text-dark);}
.phytorx-header{background:linear-gradient(135deg,var(--green-deep) 0%,var(--green-mid) 60%,var(--green-soft) 100%);border-radius:16px;padding:2.5rem 3rem;margin-bottom:2rem;}
.phytorx-header h1{font-family:'DM Serif Display',serif;font-size:2.8rem;color:var(--cream);margin:0;}
.phytorx-header h1 span{color:var(--gold);}
.phytorx-header p{color:rgba(245,240,232,0.75);font-size:1rem;margin:.5rem 0 0 0;font-weight:300;}
.header-badge{display:inline-block;background:rgba(200,168,75,0.2);border:1px solid var(--gold);color:var(--gold-light);font-size:.7rem;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;padding:3px 10px;border-radius:20px;margin-bottom:.8rem;}
.query-panel{background:var(--card-bg);border:1px solid var(--border);border-radius:12px;padding:1.8rem;margin-bottom:1.5rem;box-shadow:0 2px 12px rgba(13,59,46,.06);}
.brand-card{background:#eaf4ff;border:1px solid #b3d4f0;border-left:4px solid var(--blue);border-radius:10px;padding:1.2rem 1.5rem;margin-bottom:1.2rem;}
.brand-card h4{color:var(--blue);font-family:'DM Serif Display',serif;font-size:1.1rem;margin:0 0 .5rem 0;}
.herb-chip{display:inline-block;background:var(--green-mid);color:var(--cream);font-size:.75rem;padding:3px 10px;border-radius:20px;margin:3px 3px 3px 0;font-family:'DM Mono',monospace;}
.comp-warn{background:#fff8e6;border:1px solid var(--amber);border-radius:6px;padding:.6rem 1rem;font-size:.82rem;color:#7a5a00;margin-top:.5rem;}
.multi-warn{background:#fff3f0;border:1px solid var(--orange);border-radius:6px;padding:.6rem 1rem;font-size:.85rem;color:var(--orange);margin-top:.5rem;font-weight:500;}
.sev-badge{display:inline-flex;align-items:center;gap:6px;padding:6px 16px;border-radius:20px;font-weight:600;font-size:.85rem;letter-spacing:.5px;}
.sev-severe{background:#fdecea;color:var(--red);border:1.5px solid var(--red);}
.sev-moderate{background:#fef3e2;color:var(--orange);border:1.5px solid var(--orange);}
.sev-mild{background:#fefbe6;color:var(--amber);border:1.5px solid var(--amber);}
.sev-none{background:#eafaf1;color:var(--emerald);border:1.5px solid var(--emerald);}
.sev-unknown{background:#f2f2f2;color:var(--grey);border:1.5px solid var(--grey);}
.icard{background:var(--card-bg);border:1px solid var(--border);border-radius:12px;padding:2rem;margin-bottom:1.2rem;box-shadow:0 2px 16px rgba(13,59,46,.07);border-left:4px solid var(--green-mid);}
.icard.severe{border-left-color:var(--red);} .icard.moderate{border-left-color:var(--orange);}
.icard.mild{border-left-color:var(--amber);} .icard.none{border-left-color:var(--emerald);}
.icard-title{font-family:'DM Serif Display',serif;font-size:1.4rem;color:var(--green-deep);margin-bottom:1rem;}
.icard-title .herb{color:var(--gold);font-style:italic;}
.icard-title .btag{font-family:'DM Sans',sans-serif;font-size:.75rem;background:var(--cream-dark);border:1px solid var(--border);color:var(--text-light);padding:2px 8px;border-radius:4px;vertical-align:middle;margin-left:8px;}
.fl{margin-bottom:1rem;} .fl-label{font-size:.68rem;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:var(--text-light);margin-bottom:.3rem;}
.fl-val{font-size:.95rem;color:var(--text-dark);line-height:1.6;}
.epill{display:inline-block;background:var(--cream-dark);border:1px solid var(--border);color:var(--text-mid);font-size:.75rem;font-family:'DM Mono',monospace;padding:3px 10px;border-radius:4px;}
.refitem{font-size:.82rem;color:var(--text-light);font-family:'DM Mono',monospace;padding:4px 0;border-bottom:1px dotted var(--border);}
.refitem:last-child{border-bottom:none;}
.clwarn{background:#fdecea;border:1px solid var(--red);border-radius:8px;padding:1rem 1.2rem;margin:1rem 0;font-size:.9rem;color:var(--red);}
.clwarn strong{display:block;margin-bottom:.3rem;}
.disc{background:var(--cream-dark);border:1px solid var(--border);border-radius:8px;padding:1rem 1.2rem;font-size:.8rem;color:var(--text-light);margin-top:2rem;line-height:1.6;}
.hist-item{background:var(--card-bg);border:1px solid var(--border);border-radius:8px;padding:.8rem 1rem;margin-bottom:.5rem;font-size:.85rem;}
.stButton>button{background:var(--green-mid)!important;color:var(--cream)!important;border:none!important;border-radius:8px!important;font-weight:600!important;padding:.6rem 2rem!important;}
.stButton>button:hover{background:var(--green-deep)!important;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════

HERBALS = {
    "Cryptolepis sanguinolenta (Nibima / Ghana quinine)": "Cryptolepis sanguinolenta",
    "Morinda lucida (Brimstone tree / Konkroma)":         "Morinda lucida",
    "Xylopia aethiopica (Grains of Selim / Hwentia)":     "Xylopia aethiopica",
    "Azadirachta indica (Neem / Dongoyaro)":              "Azadirachta indica",
    "Annona muricata (Soursop / Graviola)":               "Annona muricata",
    "Khaya senegalensis (African mahogany)":              "Khaya senegalensis",
    "Momordica charantia (Bitter melon)":                 "Momordica charantia",
    "Ocimum gratissimum (African basil / Scent leaf)":    "Ocimum gratissimum",
    "Carica papaya (Pawpaw leaf)":                        "Carica papaya",
    "Vernonia amygdalina (Bitter leaf / Ewuro)":          "Vernonia amygdalina",
    "Phyllanthus amarus (Stonebreaker)":                  "Phyllanthus amarus",
    "Lippia multiflora (Gambian tea bush)":               "Lippia multiflora",
    "Senna alata (Emperor's candlestick)":                "Senna alata",
    "Alstonia boonei (Pattern wood / Sinuro)":            "Alstonia boonei",
    "Griffonia simplicifolia (5-HTP plant)":              "Griffonia simplicifolia",
    "Securidaca longipedunculata (Violet tree)":          "Securidaca longipedunculata",
    "Cassia sieberiana (African laburnum)":               "Cassia sieberiana",
    "Blighia sapida (Akee apple)":                        "Blighia sapida",
    "Tetrapleura tetraptera (Prekese / Aidan fruit)":     "Tetrapleura tetraptera",
    "Kalanchoe pinnata (Leaf of life)":                   "Kalanchoe pinnata",
    "Other / Not listed":                                 "OTHER",
}

BRAND_DB = {
    "Nibima": {
        "active_herbals": ["Cryptolepis sanguinolenta"],
        "manufacturer": "Centre for Plant Medicine Research (CPMR), Mampong-Akuapem",
        "form": "Liquid decoction / Capsules",
        "marketed_use": "Uncomplicated malaria",
        "fda_ghana": True, "fda_reg": "FDA/HD1.20-02086 (APPROXIMATE)",
        "risk": "HIGH", "comp_confidence": "HIGH — single-herb confirmed",
        "sources": ["Nortey et al. 2023 PMC10460277", "PMC10890966"],
        "notes": "CPMR gold-standard Cryptolepis product. 72.7% parasite clearance Day 7.",
    },
    "MIBIMA": {
        "active_herbals": ["Cryptolepis sanguinolenta"],
        "manufacturer": "Centre for Plant Medicine Research (CPMR), Mampong-Akuapem",
        "form": "Liquid decoction", "marketed_use": "Malaria treatment",
        "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — single-herb",
        "sources": ["Kumatia et al. 2021 PMC8633853"],
        "notes": "30 mL three times daily after meals. Standardised batch.",
    },
    "Masada Mixture": {
        "active_herbals": ["Cryptolepis sanguinolenta"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Antimalarial", "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — label survey confirmed",
        "sources": ["Nortey et al. 2023 PMC10460277"], "notes": "Greater Accra pharmacy survey.",
    },
    "Lepiquin": {
        "active_herbals": ["Cryptolepis sanguinolenta"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Antimalarial", "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — label survey",
        "sources": ["Nortey et al. 2023 PMC10460277"], "notes": "",
    },
    "Nolico Mixture": {
        "active_herbals": ["Cryptolepis sanguinolenta"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Antimalarial", "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — label survey",
        "sources": ["Nortey et al. 2023 PMC10460277"], "notes": "",
    },
    "Herbaquin": {
        "active_herbals": ["Cryptolepis sanguinolenta","Xylopia aethiopica","Alstonia boonei","Azadirachta indica"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Antimalarial", "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — product label in peer-reviewed survey",
        "sources": ["Nortey et al. 2023 PMC10460277"],
        "notes": "4 priority herbs. Run all pairs against any co-medication.",
    },
    "Krobo Fever Eduro": {
        "active_herbals": ["Cryptolepis sanguinolenta","Vernonia amygdalina","Momordica charantia"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Malaria / fever", "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — label survey",
        "sources": ["Nortey et al. 2023 PMC10460277"],
        "notes": "Antimalarial + 2 glucose-lowering herbs. Critical risk in diabetic patients on ACTs.",
    },
    "Alive Diabelex Mixture": {
        "active_herbals": ["Vernonia amygdalina","Momordica charantia"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Diabetes", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — antidiabetic herbal study",
        "sources": ["2024 Ghana antidiabetic herbal safety study"],
        "notes": "Two highest-priority antidiabetic herbs together. Critical risk with sulfonylureas and insulin.",
    },
    "COA Mixture": {
        "active_herbals": ["Ocimum gratissimum","Vernonia amygdalina","Carica papaya"],
        "manufacturer": "COA Research and Manufacturing Co. Ltd, Ghana",
        "form": "Liquid", "marketed_use": "Immune support / general wellbeing",
        "fda_ghana": True, "fda_reg": "FDA/Hl 21-12502 (APPROXIMATE)",
        "risk": "HIGH", "comp_confidence": "MEDIUM — composition from manufacturer + FDA notice; also contains Persea americana",
        "sources": ["coamixture.com","Ghana FDA Public Notices 2020/2021"],
        "notes": "On Ghana Essential Medicines List — dispensed in mainstream facilities.",
    },
    "Crystal Herbal Mixture": {
        "active_herbals": ["Azadirachta indica","Ocimum gratissimum","Carica papaya"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Antimalarial", "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — label survey",
        "sources": ["Nortey et al. 2023 PMC10460277"],
        "notes": "3 priority herbs with overlapping CYP3A4, 2C9, 2C19 inhibition.",
    },
    "Immunim": {
        "active_herbals": ["Azadirachta indica"],
        "manufacturer": "Centre for Plant Medicine Research (CPMR), Mampong-Akuapem",
        "form": "Hydroethanolic tincture 120 mL",
        "marketed_use": "Immune system support",
        "fda_ghana": True, "fda_reg": "FDA/HD.20-11485 (APPROXIMATE)",
        "risk": "HIGH", "comp_confidence": "HIGH — CPMR single-herb",
        "sources": ["PMC10890966 NIH table"],
        "notes": "CYP3A4/2C8/2C9 inhibition risk. CPMR registered neem product.",
    },
    "Typhofa-202": {
        "active_herbals": ["Vernonia amygdalina","Morinda lucida","Alstonia boonei","Carica papaya"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Typhoid / fever", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "MEDIUM — single survey source",
        "sources": ["Nortey et al. 2023 PMC10460277"],
        "notes": "4 priority herbs. Broad multi-CYP inhibition profile.",
    },
    "Ebenezer Favare Mixture": {
        "active_herbals": ["Alstonia boonei","Morinda lucida","Tetrapleura tetraptera"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Malaria", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "MEDIUM — single survey source",
        "sources": ["Nortey et al. 2023 PMC10460277"],
        "notes": "Also contains Rauwolfia vomitoria — additional cardiovascular concern.",
    },
    "Fosuaa Herbal Mixture": {
        "active_herbals": ["Morinda lucida","Senna alata","Carica papaya"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Malaria", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "MEDIUM — single survey source",
        "sources": ["Nortey et al. 2023 PMC10460277"], "notes": "",
    },
    "Danaq Herbal Mixture": {
        "active_herbals": ["Alstonia boonei","Vernonia amygdalina","Xylopia aethiopica"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Malaria", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "MEDIUM — single survey source",
        "sources": ["Nortey et al. 2023 PMC10460277"],
        "notes": "CYP inhibition + CYP induction herbs in same product.",
    },
    "Ebetoda Bitters": {
        "active_herbals": ["Azadirachta indica","Khaya senegalensis"],
        "manufacturer": "UNCERTAIN", "form": "Liquid bitters",
        "marketed_use": "Antimalarial / general tonic", "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "MEDIUM", "comp_confidence": "HIGH — label survey",
        "sources": ["Nortey et al. 2023 PMC10460277"],
        "notes": "Bitters — commonly under-disclosed at medication history.",
    },
    "Taabea Herbal Mixture": {
        "active_herbals": ["Azadirachta indica","Tetrapleura tetraptera"],
        "manufacturer": "UNCERTAIN", "form": "Liquid / Capsule",
        "marketed_use": "Antimalarial", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "MEDIUM", "comp_confidence": "HIGH — label survey (some variation noted)",
        "sources": ["Nortey et al. 2023 PMC10460277"], "notes": "",
    },
    "M-Sons Bitters": {
        "active_herbals": ["Khaya senegalensis","Ocimum gratissimum","Tetrapleura tetraptera"],
        "manufacturer": "UNCERTAIN", "form": "Bitters",
        "marketed_use": "Malaria / general tonic", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "MEDIUM", "comp_confidence": "MEDIUM — single survey",
        "sources": ["Nortey et al. 2023 PMC10460277"],
        "notes": "Bitters commonly under-reported by patients.",
    },
    "Adom Mala Mixture": {
        "active_herbals": ["Cryptolepis sanguinolenta","Azadirachta indica"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Antimalarial", "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "MEDIUM", "comp_confidence": "MEDIUM — survey documented",
        "sources": ["Nortey et al. 2023 PMC10460277"], "notes": "",
    },
    "Dietes Control": {
        "active_herbals": ["Morinda lucida"],
        "manufacturer": "UNCERTAIN", "form": "Liquid mixture",
        "marketed_use": "Diabetes", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "MEDIUM", "comp_confidence": "MEDIUM — antidiabetic study",
        "sources": ["2024 Ghana antidiabetic herbal safety study"],
        "notes": "Patients on this for diabetes may also take ACTs for malaria — double interaction risk.",
    },
    "Osompa D.P.": {
        "active_herbals": ["Carica papaya","Vernonia amygdalina"],
        "manufacturer": "Dr. Afari James, Ghana", "form": "Liquid food supplement",
        "marketed_use": "Diabetes / hypertension", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "MEDIUM — single study source",
        "sources": ["2024 Ghana antidiabetic herbal safety study"],
        "notes": "Marketed directly for diabetes — high co-medication probability.",
    },
    "DBT-57A": {
        "active_herbals": ["Khaya senegalensis"],
        "manufacturer": "UNCERTAIN", "form": "Polyherbal formulation",
        "marketed_use": "Type 2 diabetes", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "MEDIUM", "comp_confidence": "MEDIUM — 3 decades of community use; academic study",
        "sources": ["medRxiv 2025 observational study"],
        "notes": "49.8% mean FBS reduction in 25-patient study. Also contains Solanum torvum, Allium cepa.",
    },
    "MCP-1": {
        "active_herbals": ["Momordica charantia"],
        "manufacturer": "UNCERTAIN", "form": "UNCERTAIN",
        "marketed_use": "Hyperlipidaemia / infections", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — used in peer-reviewed Ghanaian RCT",
        "sources": ["ScienceDirect 2021 RCT"],
        "notes": "Only Ghanaian Momordica product with RCT evidence.",
    },
    "CHARDICA Powder": {
        "active_herbals": ["Momordica charantia"],
        "manufacturer": "Centre for Plant Medicine Research (CPMR), Mampong-Akuapem",
        "form": "Powder", "marketed_use": "Detoxification",
        "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "HIGH — CPMR product",
        "sources": ["CPMR product page"],
        "notes": "Marketed for detox but Momordica has significant antidiabetic activity — patient may not associate with blood sugar risk.",
    },
    "Lippia Tea": {
        "active_herbals": ["Lippia multiflora"],
        "manufacturer": "Centre for Plant Medicine Research (CPMR), Mampong-Akuapem",
        "form": "Tea", "marketed_use": "Stress relief",
        "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "LOW", "comp_confidence": "HIGH — CPMR product",
        "sources": ["CPMR product page","Ghanaian Times"],
        "notes": "CYP2C19 inhibition extrapolated from related Lippia scaberrima — limited direct evidence.",
    },
    "Blighia Powder": {
        "active_herbals": ["Blighia sapida"],
        "manufacturer": "Centre for Plant Medicine Research (CPMR), Mampong-Akuapem",
        "form": "Powder", "marketed_use": "Diarrhoea and bleeding piles",
        "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "MEDIUM", "comp_confidence": "HIGH — CPMR product",
        "sources": ["CPMR product page"],
        "notes": "Hypoglycin A toxicological concern. Flag for patients on hypoglycaemics.",
    },
    "Prekese Syrup": {
        "active_herbals": ["Tetrapleura tetraptera"],
        "manufacturer": "Various (CSIR-FRI Kumasi; Tiku Herbal; Ena Herbals)",
        "form": "Liquid syrup / Tea bags", "marketed_use": "Hypertension / postpartum recovery",
        "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "LOW", "comp_confidence": "HIGH",
        "sources": ["Graphic Online 2023","Market surveys Accra"],
        "notes": "Multiple brand variants. Theoretical additive hypotension with antihypertensives.",
    },
    "CSIR Prekese Syrup": {
        "active_herbals": ["Tetrapleura tetraptera"],
        "manufacturer": "CSIR-Forestry Research Institute (FRI), Kumasi, Ghana",
        "form": "Syrup", "marketed_use": "Hypertension",
        "fda_ghana": True, "fda_reg": "On label — number not published",
        "risk": "LOW", "comp_confidence": "HIGH",
        "sources": ["Graphic Online 2023 PAC testimony"], "notes": "",
    },
    "African SourSop Bitters": {
        "active_herbals": ["Annona muricata","Azadirachta indica"],
        "manufacturer": "Manufactured in Ghana; distributed African Imports USA",
        "form": "Liquid bitters 16 oz (21 herbs total)",
        "marketed_use": "Asthma, coughs, hypertension, colon cleanse",
        "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "MEDIUM — partial composition; 21 total herbs",
        "sources": ["African Imports USA product listing"],
        "notes": "Contains alcohol. Compound CYP inhibition from multiple herbs.",
    },
    "Ena Soursop Tea": {
        "active_herbals": ["Annona muricata"],
        "manufacturer": "Ena Herbals, Ghana", "form": "Tea bags",
        "marketed_use": "Antioxidant / hypertension / cancer support",
        "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "MEDIUM", "comp_confidence": "HIGH — 100% Annona muricata leaves",
        "sources": ["Retail presence Shoprite/Melcom Ghana"],
        "notes": "Additive hypotensive risk with amlodipine, lisinopril.",
    },
    "Serene Science 5-HTP": {
        "active_herbals": ["Griffonia simplicifolia"],
        "manufacturer": "Source Naturals (international); available Ghana via iHerb",
        "form": "Capsule 100 mg", "marketed_use": "Mood / sleep / serotonin support",
        "fda_ghana": False, "fda_reg": "Not applicable — imported supplement",
        "risk": "HIGH", "comp_confidence": "HIGH — standardised 5-HTP",
        "sources": ["iHerb Ghana product listing"],
        "notes": "⚠️ SEROTONIN SYNDROME RISK with SSRIs, MAOIs, tramadol.",
    },
    "Alomo Bitters": {
        "active_herbals": ["COMPOSITION UNKNOWN — proprietary"],
        "manufacturer": "Kasapreko PLC, Ghana",
        "form": "Liquid bitters (750 mL / 200 mL / 30 mL sachet)",
        "marketed_use": "Revitalising herbal drink",
        "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "UNCERTAIN — composition proprietary",
        "comp_confidence": "LOW — ingredient list not publicly disclosed",
        "sources": ["Kasapreko PLC manufacturer website"],
        "notes": "Very widely consumed. Cannot assess interaction risk without composition.",
    },
    "Top Fever Syrup": {
        "active_herbals": ["Azadirachta indica","Alstonia boonei"],
        "manufacturer": "Top Herbal, Ghana", "form": "Liquid syrup",
        "marketed_use": "Fever / malaria fever", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "MEDIUM — single source",
        "sources": ["Ghanaian retail listing; antimalarial market survey"], "notes": "",
    },
    "Time Herbal Mixture": {
        "active_herbals": ["Vernonia amygdalina"],
        "manufacturer": "Kenoga Company Limited, Ghana", "form": "Liquid mixture",
        "marketed_use": "Malaria", "fda_ghana": "UNCERTAIN", "fda_reg": "UNCERTAIN",
        "risk": "MEDIUM", "comp_confidence": "MEDIUM — composition varies across sources",
        "sources": ["Clinical evaluation studies; market surveys"],
        "notes": "Composition inconsistency is itself a clinical concern.",
    },
    "Hepatone": {
        "active_herbals": ["Phyllanthus amarus"],
        "manufacturer": "Medi-Moses Herbal Clinic, Accra", "form": "Liquid",
        "marketed_use": "Hepatitis / liver disorders",
        "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "LOW — single source, manufacturer not cross-verified",
        "sources": ["Medi-Moses product listings Accra"],
        "notes": "If confirmed: CYP3A4 MBI — critical for patients on ARVs or statins.",
    },
    "Tina Bitters": {
        "active_herbals": ["Momordica charantia","Vernonia amygdalina"],
        "manufacturer": "Tina Herbal Medicine and Spiritual Centre, Ghana",
        "form": "Liquid", "marketed_use": "Diabetes / appetite loss",
        "fda_ghana": True, "fda_reg": "UNCERTAIN",
        "risk": "HIGH", "comp_confidence": "LOW — single source, not cross-verified",
        "sources": ["Local media adverts; GHAFTRAM listings"],
        "notes": "Two hypoglycaemic herbs — high additive risk with metformin, glibenclamide.",
    },
}

ALIASES = {
    "nibima":"Nibima","mibima":"MIBIMA","masada":"Masada Mixture",
    "masada mixture":"Masada Mixture","lepiquin":"Lepiquin",
    "nolico":"Nolico Mixture","nolico mixture":"Nolico Mixture",
    "herbaquin":"Herbaquin","krobo":"Krobo Fever Eduro",
    "krobo fever":"Krobo Fever Eduro","alive diabelex":"Alive Diabelex Mixture",
    "diabelex":"Alive Diabelex Mixture","coa":"COA Mixture","coa mixture":"COA Mixture",
    "crystal":"Crystal Herbal Mixture","immunim":"Immunim",
    "typhofa":"Typhofa-202","typhofa-202":"Typhofa-202",
    "ebenezer favare":"Ebenezer Favare Mixture","fosuaa":"Fosuaa Herbal Mixture",
    "danaq":"Danaq Herbal Mixture","ebetoda":"Ebetoda Bitters",
    "taabea":"Taabea Herbal Mixture","m-sons":"M-Sons Bitters","msons":"M-Sons Bitters",
    "adom mala":"Adom Mala Mixture","dietes":"Dietes Control","dietes control":"Dietes Control",
    "osompa":"Osompa D.P.","dbt-57a":"DBT-57A","dbt57a":"DBT-57A",
    "mcp-1":"MCP-1","mcp1":"MCP-1","chardica":"CHARDICA Powder",
    "lippia tea":"Lippia Tea","blighia powder":"Blighia Powder",
    "prekese syrup":"Prekese Syrup","prekese":"Prekese Syrup",
    "csir prekese":"CSIR Prekese Syrup","soursop bitters":"African SourSop Bitters",
    "african soursop":"African SourSop Bitters","ena soursop":"Ena Soursop Tea",
    "soursop tea":"Ena Soursop Tea","5-htp":"Serene Science 5-HTP",
    "griffonia":"Serene Science 5-HTP","serene science":"Serene Science 5-HTP",
    "alomo":"Alomo Bitters","alomo bitters":"Alomo Bitters",
    "top fever":"Top Fever Syrup","time herbal":"Time Herbal Mixture",
    "hepatone":"Hepatone","tina bitters":"Tina Bitters","tina":"Tina Bitters",
}

DRUG_CATEGORIES = {
    "Antimalarials":["Artesunate","Artemether","Lumefantrine","Artemether-Lumefantrine (Coartem)","Amodiaquine","Chloroquine","Quinine"],
    "Antiretrovirals":["Efavirenz","Nevirapine","Lopinavir/Ritonavir","Dolutegravir","Tenofovir","Zidovudine","Lamivudine"],
    "Antidiabetics":["Metformin","Glibenclamide","Glimepiride","Glipizide","Insulin","Repaglinide","Pioglitazone","Sitagliptin"],
    "Antihypertensives":["Amlodipine","Nifedipine","Lisinopril","Enalapril","Hydrochlorothiazide","Atenolol","Methyldopa","Losartan"],
    "Anticoagulants / Antiplatelets":["Warfarin","Clopidogrel","Aspirin (low-dose)"],
    "Antibiotics / Antimicrobials":["Erythromycin","Azithromycin","Ciprofloxacin","Metronidazole","Cotrimoxazole","Fluconazole","Isoniazid","Rifampicin"],
    "CNS / Psychiatric":["Amitriptyline","Fluoxetine","Sertraline","Phenytoin","Carbamazepine","Phenobarbitone","Tramadol","Haloperidol"],
    "Cardiovascular":["Amiodarone","Digoxin","Simvastatin","Atorvastatin","Spironolactone"],
}

SYSTEM_PROMPT = """You are PhytoRx Africa, a clinical pharmacology expert specialising in 
West African herb-drug interactions. Return ONLY valid JSON — no preamble, no markdown.
Base your response ONLY on published evidence. State INSUFFICIENT EVIDENCE rather than guess.
Severity: "Severe"|"Moderate"|"Mild"|"None"|"Unknown"
mechanism_type: "Pharmacokinetic"|"Pharmacodynamic"|"Both"|"Unknown"|"None"
evidence_quality: "Clinical_Study"|"Animal_Study"|"In_vitro_only"|"Case_Report"|"Theoretical"|"Insufficient_Evidence"
clinical_warning: urgent warning string OR "" if none.
References: real sources only — prefix UNCERTAIN citations with "APPROXIMATE:"

Return:
{"drug":"","herbal":"","severity":"","mechanism_type":"","mechanism_detail":"",
"clinical_consequence":"","management_recommendation":"","evidence_quality":"",
"evidence_summary":"","references":[],"clinical_warning":"","data_gaps":"","confidence_note":""}"""

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def sev_html(s):
    m={"Severe":("🔴","sev-severe"),"Moderate":("🟠","sev-moderate"),
       "Mild":("🟡","sev-mild"),"None":("🟢","sev-none"),"Unknown":("⚪","sev-unknown")}
    i,c=m.get(s,("⚪","sev-unknown"))
    return f'<span class="sev-badge {c}">{i} {s}</span>'

def card_cls(s):
    return {"Severe":"severe","Moderate":"moderate","Mild":"mild","None":"none"}.get(s,"")

def lookup(q):
    k=q.strip().lower()
    c=ALIASES.get(k)
    if not c:
        for a,cn in ALIASES.items():
            if k in a or a in k: c=cn; break
    return (c, BRAND_DB[c]) if c and c in BRAND_DB else (None,None)

def api_call(drug, herbal, key):
    client=anthropic.Anthropic(api_key=key)
    msg=client.messages.create(
        model="claude-opus-4-5", max_tokens=1500, system=SYSTEM_PROMPT,
        messages=[{"role":"user","content":f"DRUG: {drug}\nHERBAL: {herbal}\nReturn JSON interaction card."}])
    raw=msg.content[0].text.strip()
    raw=re.sub(r"^```(?:json)?\s*","",raw); raw=re.sub(r"\s*```$","",raw)
    return json.loads(raw)

def render_brand_card(canonical, bd):
    herbals=bd["active_herbals"]
    chips="".join(f'<span class="herb-chip">{h}</span>' for h in herbals)
    fda="✅ Yes" if bd["fda_ghana"] is True else "❌ No" if bd["fda_ghana"] is False else "⚠️ UNCERTAIN"
    uncertain=""
    if any(x in bd.get("comp_confidence","").upper() for x in ["LOW","MEDIUM","UNCERTAIN"]):
        uncertain=f'<div class="comp-warn">⚠️ Composition confidence: {bd["comp_confidence"]}</div>'
    multi=""
    if len(herbals)>1 and "UNKNOWN" not in herbals[0].upper():
        multi=f'<div class="multi-warn">🔁 Multi-herb — {len(herbals)} interaction checks will run</div>'
    notes_html=f'<div style="font-size:.8rem;margin-top:.5rem;color:#555">📝 {bd["notes"]}</div>' if bd.get("notes") else ""
    st.markdown(f"""
    <div class="brand-card">
        <h4>🌿 {canonical}</h4>
        <div style="margin-bottom:.8rem">{chips}</div>
        <div style="font-size:.82rem;color:#444;line-height:1.8">
            <b>Manufacturer:</b> {bd['manufacturer']}<br>
            <b>Form:</b> {bd['form']} &nbsp;|&nbsp; <b>Use:</b> {bd['marketed_use']}<br>
            <b>FDA Ghana:</b> {fda} &nbsp;|&nbsp; <b>Reg No:</b> {bd['fda_reg']}<br>
            <b>Interaction risk:</b> {bd['risk']}
        </div>
        {uncertain}{multi}
        <div style="font-size:.78rem;color:#777;margin-top:.6rem;font-style:italic">
            📄 {"; ".join(bd['sources'])}
        </div>
        {notes_html}
    </div>""", unsafe_allow_html=True)

def render_icard(result, brand=""):
    sev=result.get("severity","Unknown")
    cls=card_cls(sev)
    btag=f'<span class="btag">via {brand}</span>' if brand else ""
    st.markdown(f"""
    <div class="icard {cls}">
        <div class="icard-title">
            <span class="drug">{result.get('drug','')}</span>
            <span style="color:var(--text-light);margin:0 8px">+</span>
            <span class="herb">{result.get('herbal','')}</span>{btag}
        </div>
        {sev_html(sev)}
    </div>""", unsafe_allow_html=True)
    if result.get("clinical_warning"):
        st.markdown(f'<div class="clwarn"><strong>⚠️ Clinical Warning</strong>{result["clinical_warning"]}</div>', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        for label,key in [("Mechanism Type","mechanism_type"),("Mechanism Detail","mechanism_detail"),("Clinical Consequence","clinical_consequence")]:
            st.markdown(f'<div class="fl"><div class="fl-label">{label}</div><div class="fl-val">{result.get(key,"—")}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="fl"><div class="fl-label">Management</div><div class="fl-val">{result.get("management_recommendation","Monitor")}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fl"><div class="fl-label">Evidence Quality</div><div class="fl-val"><span class="epill">{result.get("evidence_quality","—")}</span></div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fl"><div class="fl-label">Confidence</div><div class="fl-val">{result.get("confidence_note","—")}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="fl"><div class="fl-label">Evidence Summary</div><div class="fl-val">{result.get("evidence_summary","")}</div></div>', unsafe_allow_html=True)
    refs=result.get("references",[])
    if refs:
        st.markdown(f'<div class="fl"><div class="fl-label">References</div>{"".join(f"""<div class="refitem">📄 {r}</div>""" for r in refs)}</div>', unsafe_allow_html=True)
    if result.get("data_gaps"):
        st.markdown(f'<div class="fl"><div class="fl-label">Data Gaps</div><div class="fl-val" style="color:var(--text-light);font-style:italic">{result["data_gaps"]}</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION
# ══════════════════════════════════════════════════════════════════════════════
if "history" not in st.session_state: st.session_state.history=[]
if "results" not in st.session_state: st.session_state.results=[]

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="phytorx-header">
    <div class="header-badge">West African Herbal Intelligence</div>
    <h1>Phyto<span>Rx</span> Africa</h1>
    <p>Herb–Drug Interaction Intelligence · Brand name lookup · Ghana &amp; West Africa</p>
</div>""", unsafe_allow_html=True)

with st.expander("🔑 API Configuration", expanded=False):
    api_key=st.text_input("Anthropic API Key", type="password")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2 = st.tabs(["🔍 Search by Botanical Name", "🏷️ Search by Brand Name"])

# ── TAB 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="query-panel">', unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        mode=st.radio("DRUG INPUT",["Select from list","Type drug name"],horizontal=True,key="t1_drug_mode")
        if mode=="Select from list":
            cat=st.selectbox("CATEGORY",list(DRUG_CATEGORIES.keys()),key="t1_cat")
            drug=st.selectbox("DRUG",DRUG_CATEGORIES[cat],key="t1_drug")
        else:
            drug=st.text_input("DRUG NAME",placeholder="e.g. Warfarin",key="t1_drug_txt")
    with c2:
        hd=st.selectbox("HERBAL",list(HERBALS.keys()),key="t1_herb")
        if HERBALS[hd]=="OTHER":
            herb=st.text_input("SPECIFY HERBAL",key="t1_herb_custom")
        else:
            herb=hd
    b1,b2=st.columns([1,4])
    with b1: go=st.button("🌿 Check",key="t1_go",use_container_width=True)
    with b2:
        if st.button("Clear",key="t1_clr"):
            st.session_state.history=[]; st.session_state.results=[]; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    if go:
        if not api_key: st.error("Enter API key.")
        elif not drug: st.error("Enter a drug.")
        elif not herb or herb=="OTHER": st.error("Specify herbal.")
        else:
            with st.spinner("Synthesising interaction data..."):
                try:
                    r=api_call(drug,herb,api_key)
                    st.session_state.results.insert(0,{"result":r,"brand":""})
                    st.session_state.history.insert(0,{"drug":drug,"herb":herb,"severity":r.get("severity","Unknown"),"time":datetime.now().strftime("%H:%M"),"brand":""})
                except Exception as e: st.error(f"Error: {e}")

# ── TAB 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="query-panel">', unsafe_allow_html=True)
    bmode=st.radio("BRAND INPUT",["Select known brand","Type brand name"],horizontal=True,key="t2_bmode")
    if bmode=="Select known brand":
        bq=st.selectbox("BRAND",sorted(BRAND_DB.keys()),key="t2_bsel")
    else:
        bq=st.text_input("BRAND NAME",placeholder="e.g. Nibima, Alive Diabelex, Alomo Bitters...",key="t2_btxt")
    c1,c2=st.columns(2)
    with c1:
        dmode=st.radio("DRUG INPUT",["Select from list","Type drug name"],horizontal=True,key="t2_dmode")
    with c2:
        if dmode=="Select from list":
            dcat=st.selectbox("CATEGORY",list(DRUG_CATEGORIES.keys()),key="t2_dcat")
            bdrug=st.selectbox("DRUG",DRUG_CATEGORIES[dcat],key="t2_dsel")
        else:
            bdrug=st.text_input("DRUG NAME",placeholder="e.g. Metformin",key="t2_dtxt")
    b1,b2=st.columns([1,4])
    with b1: bgo=st.button("🏷️ Check Brand",key="t2_go",use_container_width=True)
    with b2:
        if st.button("Clear",key="t2_clr"):
            st.session_state.history=[]; st.session_state.results=[]; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if bgo:
        if not api_key: st.error("Enter API key.")
        elif not bq: st.error("Enter brand name.")
        elif not bdrug: st.error("Enter drug.")
        else:
            canonical,bd=lookup(bq)
            if not canonical:
                st.warning(f"**'{bq}'** not in brand database. Try the Botanical Name tab, or check spelling.")
            else:
                render_brand_card(canonical,bd)
                herbals=bd["active_herbals"]
                if "UNKNOWN" in herbals[0].upper() or "UNCERTAIN" in herbals[0].upper():
                    st.warning(f"Composition of **{canonical}** is proprietary — cannot run interaction check. Advise patient to disclose full ingredient list.")
                else:
                    if len(herbals)>1:
                        st.info(f"Running {len(herbals)} checks ({len(herbals)} botanicals × 1 drug)...")
                    for h in herbals:
                        with st.spinner(f"Checking {h}..."):
                            try:
                                r=api_call(bdrug,h,api_key)
                                st.session_state.results.insert(0,{"result":r,"brand":canonical})
                                st.session_state.history.insert(0,{"drug":bdrug,"herb":h,"severity":r.get("severity","Unknown"),"time":datetime.now().strftime("%H:%M"),"brand":canonical})
                            except Exception as e: st.error(f"Error for {h}: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.results:
    st.markdown("## Interaction Reports")
    sev_icons={"Severe":"🔴","Moderate":"🟠","Mild":"🟡","None":"🟢","Unknown":"⚪"}
    if len(st.session_state.history)>1:
        with st.expander(f"📋 Session History ({len(st.session_state.history)} queries)"):
            for item in st.session_state.history:
                icon=sev_icons.get(item["severity"],"⚪")
                btag=f' <em>({item["brand"]})</em>' if item.get("brand") else ""
                st.markdown(f'<div class="hist-item">{icon} <b>{item["drug"]}</b> + <em>{item["herb"]}</em>{btag}<span style="float:right;font-size:.7rem;color:var(--text-light)">{item["time"]}</span></div>', unsafe_allow_html=True)
    for entry in st.session_state.results:
        render_icard(entry["result"], brand=entry.get("brand",""))
        st.markdown("---")

st.markdown("""
<div class="disc">
    <strong>⚕️ Clinical Disclaimer</strong><br>
    PhytoRx Africa synthesises published pharmacological literature to support clinical decision-making.
    This tool does not replace professional clinical judgement. Evidence quality is explicitly stated in 
    every report. Brand name composition data is sourced from peer-reviewed pharmacy surveys, CPMR/CSIR 
    product lists, and published clinical studies. Where composition is proprietary or unconfirmed, this 
    is explicitly stated. FDA Ghana registration status reflects cited sources and may not reflect current 
    regulatory status.
</div>""", unsafe_allow_html=True)
