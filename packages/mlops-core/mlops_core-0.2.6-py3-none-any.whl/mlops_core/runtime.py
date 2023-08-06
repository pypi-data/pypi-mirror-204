import os

# Create a function to see if the runtime is a databricks environment


def is_datbricks_runtime():
    return "DATABRICKS_RUNTIME_VERSION" in os.environ
