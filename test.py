from src.processor import DDRProcessor

# Simulated data since we don't have the PDFs yet
sample_inspection = "Area: Roof. Observation: Water pooling near the AC unit. Tiles appear cracked."
sample_thermal = "Area: Roof. Finding: Temperature spike of 45°C detected under AC unit, suggesting moisture retention."

processor = DDRProcessor()
report = processor.analyze_data(sample_inspection, sample_thermal)

print("\n--- GENERATED DDR PREVIEW ---")
print(report)