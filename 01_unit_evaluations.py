import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict

from utils.utils import POSSIBLE_DISEASES


def plot_test_results(results_file, bar_plot_file_name):
    # Read results
    df = pd.read_csv(results_file)

    # Get test columns (assuming they're boolean/True-False columns)
    test_columns = [
        "non_empty_response",
        "all_string_response",
        "valid_disease_name_response",
    ]

    # Calculate pass/fail counts for each test
    passed = [df[col].sum() for col in test_columns]
    failed = [len(df) - count for count in passed]

    # Create bar plot
    _, ax = plt.subplots(figsize=(10, 6))
    x = range(len(test_columns))
    width = 0.35

    # Plot bars
    ax.bar([i - width / 2 for i in x], passed, width, label="Passed", color="green")
    ax.bar([i + width / 2 for i in x], failed, width, label="Failed", color="red")

    # Customize plot
    ax.set_ylabel("Number of data samples")
    ax.set_title("Test Results Summary")
    ax.set_xticks(x)
    ax.set_xticklabels(test_columns)
    ax.grid()
    ax.legend()

    # Save plot
    plt.savefig(bar_plot_file_name)
    plt.close()


class TestSample:
    def __init__(self, data: Dict):
        self.data = data
        self.test_results = {}

    def run_tests(self):
        # Test 1: Non-Empty Response
        self.test_results["non_empty_response"] = (
            not pd.isna(self.data["response"]) and self.data["response"] != ""
        )

        # Test 2: String Type
        self.test_results["all_string_response"] = isinstance(
            self.data["response"], str
        )

        # Test 3: Valid Disease Name
        response_lower = self.data["response"].lower()
        diseases_lower = [disease.lower() for disease in POSSIBLE_DISEASES]
        try:
            if response_lower in diseases_lower or diseases_lower in response_lower:
                self.test_results["valid_disease_name_response"] = True
        except:
            self.test_results["valid_disease_name_response"] = False

        return self.test_results


def test_all_samples(file_name):
    # Read the responses from LLM that we want to apply unit evaluations on
    df = pd.read_csv("data/llm_responses.csv")

    # List to store results
    all_results = []

    # Test each sample
    for _, row in df.iterrows():
        sample = TestSample(row)
        test_results = sample.run_tests()

        # Combine original data with test results
        result_row = {**row.to_dict(), **test_results}
        all_results.append(result_row)

    # Create results DataFrame and save
    results_df = pd.DataFrame(all_results)
    results_df.to_csv(file_name, index=False)
    return results_df


if __name__ == "__main__":
    # Run tests and get results

    file_name = "evaluation_results/01_unit_evaluations_results.csv"
    bar_plot_file_name = "evaluation_results/01_unit_evaluations_plot.png"
    results = test_all_samples(file_name)

    # Print summary
    print("\nTest Results Summary:")
    print(f"Total samples tested: {len(results)}")
    for test in [
        "non_empty_response",
        "all_string_response",
        "valid_disease_name_response",
    ]:
        passed = len(results[results[test] == True])
        failed = len(results[results[test] == False])
        print(f"\n{test}:")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")

    print(f"\nResults saved to {file_name}")

    plot_test_results(file_name, bar_plot_file_name)

    print(f"\nResults bar plot saved to {bar_plot_file_name}")
