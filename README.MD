stress-indicator/
│
├── app.py                  # Main Streamlit application
├── stress_model.pkl        # Trained ML model
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
│
├── assets/                 # Static files (images, icons, animations)
│   ├── logo.png
│   ├── heartbeat.json      # Lottie animation
│   └── quotes.txt          # Motivational quotes
│
├── css/                    # Custom CSS styles
│   └── style.css
│
├── data/                   # Dataset or sample CSVs
│   └── stress_dataset.csv
│
├── reports/                # Generated PDF reports
│   └── sample_report.pdf
│
├── utils/                  # Helper functions
│   ├── __init__.py
│   ├── prediction.py       # Model loading & prediction logic
│   ├── visualization.py    # Plotly charts, Graphviz tree
│   ├── pdf_generator.py    # ReportLab PDF generation
│   └── recommendations.py  # Personalized wellness tips
│
└── .gitignore              # Ignore unnecessary files
