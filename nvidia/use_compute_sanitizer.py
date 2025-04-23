import subprocess
import os
import json
from datetime import datetime

# Configuration
cuda_execution = ["gaussjordan","-a","-m","100","-r","5"]  
output_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"sanitizer_results"
os.makedirs(output_dir, exist_ok=True)
subtools = [["compute-sanitizer","--tool","memcheck","--leak-check=full"],
            ["compute-sanitizer","--tool","racecheck"],
            ["compute-sanitizer","--tool","initcheck"],
            ["compute-sanitizer","--tool","synccheck"]
            ]

def run_baseline():
    stats_file_path = f"/tmp/baseline_{output_timestamp}.json"
    result = subprocess.run(cuda_execution + ["--stats-file",stats_file_path], capture_output=True)
    with open(stats_file_path) as f:
        return result, json.load(f)


def run_compute_sanitizer(subtool_w_options):
    stats_file_path = f"/tmp/{subtool_w_options[2]}_{output_timestamp}.json"
    result = subprocess.run(subtool_w_options + cuda_execution + ["--stats-file",stats_file_path], capture_output=True)
    with open(stats_file_path) as f:
        return result,json.load(f)

def compute_mean_overheads(baseline_stats, sanitizer_stats):
    overheads = {}
    for tool_name, tool_data in sanitizer_stats.items():
        total_ratio = 0
        count = 0
        for key in baseline_stats:
            base_elapsed = baseline_stats[key]["e_stats"]["elapsed"]
            tool_elapsed = tool_data.get(key, {}).get("e_stats", {}).get("elapsed")

            if tool_elapsed is not None and base_elapsed > 0:
                ratio = tool_elapsed / base_elapsed
                total_ratio += ratio
                count += 1

        mean_overhead = total_ratio / count if count > 0 else None
        overheads[tool_name] = mean_overhead

    return overheads

def compute_kernel_overheads_vs_bs(baseline_stats):
    bs_elapsed = baseline_stats["BS"]["e_stats"]["elapsed"]
    overheads = {}

    for kernel, data in baseline_stats.items():
        elapsed = data["e_stats"]["elapsed"]
        if kernel == "BS":
            overheads[kernel] = 0.0
        else:
            overhead_percent = ((elapsed - bs_elapsed) / bs_elapsed) * 100
            overheads[kernel] = overhead_percent

    return overheads


def main():
    print("Running baseline...",flush=True)
    result,baseline_stats = run_baseline()
    print("Baseline complete.",flush=True)

    sanitizer_results = {}
    failing = []#Fix failing
    for subtool in subtools:
        print(f"Running sanitizer: {subtool[2]}...",flush=True)
        result,stats = run_compute_sanitizer(subtool)
        sanitizer_results[subtool[2]] = stats
        print(f"{subtool[2]} complete.",flush=True)
        #if result.returncode!=0 : FIX
        failing.append({subtool[2]:str(result.stdout)})

    mean_overheads = compute_mean_overheads(baseline_stats, sanitizer_results)

    print("\nMean overheads per tool:",flush=True)
    for tool, overhead in mean_overheads.items():
        if overhead is not None:
            print(f"{tool}: {overhead:.2f}x",flush=True)
        else:
            print(f"{tool}: No data",flush=True)
    
    overheads_vs_bs = compute_kernel_overheads_vs_bs(baseline_stats)

    print("Overhead relative to BS (in %,flush=True):")
    for kernel, overhead in overheads_vs_bs.items():
        print(f"{kernel}: {overhead:.2f}%",flush=True)


    combined_results_path = os.path.join(output_dir, f"combined_results_{output_timestamp}.json")
    with open(combined_results_path, "w") as f:
        json.dump({"mean_tool_overhead":mean_overheads,
                   "overhead_of_error":overheads_vs_bs,
                   "failing":failing,
            "baseline": baseline_stats,
            "sanitizers": sanitizer_results
        }, f, indent=4)

    print(f"\nAll results saved to {combined_results_path}",flush=True)


if __name__ == "__main__":
    print("Script started",flush=True)
    main()