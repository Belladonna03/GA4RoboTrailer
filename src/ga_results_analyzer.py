import json
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def analyze_json_files(file_paths):
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                data = [json.loads(line) for line in file]

            # Extract relevant information and handle NaN/infinity values
            fitness_values = [entry['best_fitness'] for entry in data if np.isfinite(entry['best_fitness'])]
            run_times = [entry['run_time'] for entry in data if np.isfinite(entry['run_time'])]
            individual_lengths = [len(entry['best_individual']) for entry in data if np.isfinite(len(entry['best_individual']))]

            if not fitness_values or not run_times or not individual_lengths:
                print(f"File: {file_path} contains invalid data.")
                continue

            # Calculate statistics
            average_fitness = np.mean(fitness_values)
            deviation_count_1 = sum(1 for value in fitness_values if abs(value - average_fitness) < 1000)
            deviation_count_2 = sum(1 for value in fitness_values if abs(value - average_fitness) > 1000)
            deviation_count_3 = sum(1 for value in fitness_values if abs(value - average_fitness) > 6000)
            average_run_time = np.mean(run_times)
            average_individual_length = np.mean(individual_lengths)

            # Calculate additional statistics for deviation analysis
            std_dev_fitness = np.std(fitness_values)
            median_fitness = np.median(fitness_values)
            q1 = np.percentile(fitness_values, 25)
            q3 = np.percentile(fitness_values, 75)
            iqr_fitness = q3 - q1

            # Print statistics
            print(f"File: {file_path}")
            print(f"Average Fitness Value: {average_fitness}")
            print(f"Number of Deviations < 1000: {deviation_count_1}")
            print(f"Number of Deviations 1000 << 6000: {deviation_count_2 - deviation_count_3}")
            print(f"Number of Deviations > 6000: {deviation_count_3}")
            print(f"Average Run Time: {average_run_time} seconds")
            print(f"Average Individual Length: {average_individual_length}")
            print(f"Standard Deviation of Fitness Values: {std_dev_fitness}")
            print(f"Median Fitness Value: {median_fitness}")
            print(f"Interquartile Range of Fitness Values: {iqr_fitness}")
            print()

            # Sort the data by the fitness values in ascending order
            sorted_data = sorted(data, key=lambda x: x['best_fitness'] if np.isfinite(x['best_fitness']) else float('inf'))
            sorted_run_numbers = [data.index(entry) + 1 for entry in sorted_data if np.isfinite(entry['best_fitness'])]
            sorted_fitness_runs = [(run_number, entry['best_fitness']) for run_number, entry in zip(sorted_run_numbers, sorted_data) if np.isfinite(entry['best_fitness'])]

            # Create a DataFrame for better visualization
            df_sorted_fitness_runs = pd.DataFrame(sorted_fitness_runs, columns=['Run Number', 'Fitness Value'])
            pd.set_option('display.max_rows', None)
            print(df_sorted_fitness_runs)

        except FileNotFoundError:
            print(f"Error: File not found - {file_path}")
        except json.JSONDecodeError:
            print(f"Error: Failed to parse JSON from file - {file_path}")
        except KeyError as e:
            print(f"Error: Missing key {e} in file - {file_path}")
        except Exception as e:
            print(f"Unexpected error occurred while processing file {file_path}: {e}")

# List of JSON file paths
file_paths = [
    'C:/Python 3.8.2/Thesis/Результаты/Statistics/ga_statistics_(5,5)_(5,95)_310.json',
    'C:/Python 3.8.2/Thesis/Результаты/Statistics/ga_statistics_(95,5)_(40,95)_255.json',
    'C:/Python 3.8.2/Thesis/Результаты/Statistics/ga_statistics_(95,95)_(5,95)_235.json'
]

analyze_json_files(file_paths)