import os

# Define the structure relative to the current directory (timeglance/)
structure = [
    "pyproject.toml",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "src/timeglance/__init__.py",
    "src/timeglance/forecast.py",
    "src/timeglance/profiler.py",
    "src/timeglance/predictor.py",
    "src/timeglance/reporter.py",
    "src/timeglance/decorators.py",
    "src/timeglance/context.py",
    "src/timeglance/exceptions.py",
    "src/timeglance/config.py",
    "src/timeglance/models/metrics.py",
    "src/timeglance/models/forecast.py",
    "src/timeglance/models/report.py",
    "src/timeglance/integrations/pandas.py",
    "src/timeglance/integrations/numpy.py",
    "src/timeglance/integrations/dask.py",
    "src/timeglance/integrations/asyncio.py",
    "src/timeglance/exporters/json_exporter.py",
    "src/timeglance/exporters/csv_exporter.py",
    "src/timeglance/exporters/html_exporter.py",
    "src/timeglance/display/rich_output.py",
    "src/timeglance/display/terminal.py",
    "src/timeglance/display/progress.py",
    "src/timeglance/utils/memory.py",
    "src/timeglance/utils/timing.py",
    "src/timeglance/utils/statistics.py",
    "src/timeglance/utils/confidence.py",
    "tests/test_forecast.py",
    "tests/test_memory.py",
    "tests/test_async.py",
    "tests/test_confidence.py",
    "examples/basic.py",
    "examples/pandas.py",
    "examples/numpy.py",
    "examples/async_example.py",
]

for path in structure:
    # Extract directory path
    dirname = os.path.dirname(path)
    
    # Create directories if they don't exist
    if dirname:
        os.makedirs(dirname, exist_ok=True)
        
    # Create empty file
    with open(path, "w") as f:
        pass

print("File structure created successfully!")