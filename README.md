# COG (CSV–OWL Bridge): A Spreadsheet-Based Ontology Editor for Bidirectional CSV ↔ OWL Transformation

COG is a lightweight framework that enables users to create, inspect, and maintain OWL ontologies using spreadsheets by supporting **bidirectional conversion between CSV/XLSX files and OWL**. The tool lowers the barrier to ontology authoring by allowing ontology construction without writing OWL syntax.

## 🎯 What This Repository Contains

This repository serves as the **landing page** for the COG project.  
All source code is organized inside subfolders, and each folder contains its own README describing its contents.

## 🎥 Demo Video

▶️ Tool Demo: <https://youtu.be/R1brWymSiQM>

## 📌 Key Capabilities

- CSV/XLSX → OWL conversion  
- OWL → CSV/XLSX conversion  
- Support for:
  - Classes  
  - SubClassOf axioms  
  - Property restrictions (some / all)  
  - Intersection classes  
  - Object properties  
  - Domain & Range  
  - Individuals  
  - Subproperties and property chains  
- Automatic prefix extraction and reuse  
- Generation of consolidated OWL output  

## 🗂️ Repository Structure
```
cog-csv-owl-bridge/
│
├── src/
│   ├── csv_to_owl/
│   │   ├── csv_owl_code.py
│   │   └── README.md
│   │
│   ├── owl_to_csv/
│   │   ├── owl_csv_code.py
│   │   ├── owl_csv_code_new.py
│   │   └── README.md
│   │
│   ├── start.py
│   └── README.md
│
├── build_tool/
│   └── README.md
│
├── testing_output/
│   └── README.md
│
├── comparison/
│   └── README.md
│
├── LICENSE
└── README.md
```

## ⚙️ Installation

```bash
git clone <repo-url>
cd cog-csv-owl-bridge
python -m venv env
source env/bin/activate        # Linux/Mac
env\Scripts\activate           # Windows
pip install pandas rdflib owlready2 numpy
```

## 🚀 Usage
1. OWL → CSV/XLSX

```bash
python src/start.py owl_to_csv "path/to/input.owl"
```
- Output: output.xlsx with sheets:
  - owlclass
  - subclass
  - domain
  - range
  - instances
  - subproperty
  - prefixiri

2. CSV/XLSX → OWL

```bash
python src/start.py csv_to_owl "path/to/input.xlsx"
```
- Output:
  - classes.owl
  - subclass.owl
  - domain.owl
  - range.owl
  - instances.owl
  - subproperty.owl
  - combined.owl
    
## 🔁 Typical Workflow
- Create CSV/XLSX → Generate OWL → View in Protégé
- OWL → CSV/XLSX → Edit Spreadsheet → Rebuild OWL

## 📁 Folder Descriptions
- src/: Contains all executable code for conversion pipelines.
- src/csv_to_owl/: Implementation of CSV/XLSX → OWL conversion.
- src/owl_to_csv/: Implementation of OWL → CSV/XLSX extraction.
- build_tool/: Helper scripts and dependency installers.
- testing_output/: Sample inputs and generated outputs.
- comparison/: Scripts and files used to compare generated OWL artifacts.

## 🛠 Technologies
- Python
- RDFlib
- Owlready2
- Pandas
- NumPy

## 📊 Use Cases
- Spreadsheet-based ontology authoring
- Teaching OWL concepts
- Rapid ontology prototyping
- Ontology debugging and inspection

## 🤝 Contributing
- Fork the repository
- Create a new branch
- Commit your changes
- Open a Pull Request

## 📜 License
- Apache 2.0 License
