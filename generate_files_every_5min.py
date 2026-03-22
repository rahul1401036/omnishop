import os
import time
import random
import csv
from datetime import datetime , timedelta


def generate_row_with_nulls(row_id):
    # At least one of the first three fields will be null
    fields = [
        random.randint(1000, 9999),
        random.randint(10000, 99999),
        random.choice(["view", "cart", "purchase", "wishlist"])
    ]
    # Randomly pick one or more fields to set to None (at least one)
    null_indices = random.sample([0, 1, 2], random.randint(1, 3))
    for idx in null_indices:
        fields[idx] = None
    event_time = datetime.now().isoformat()
    return fields + [event_time]

def generate_row_no_nulls(row_id):
    user_id = random.randint(1000, 9999)
    product_id = random.randint(10000, 99999)
    event_type = random.choice(["view", "cart", "purchase", "wishlist"])
    event_time = datetime.now().isoformat()
    return [user_id, product_id, event_type, event_time]

def create_file_with_rows(directory, file_prefix="data",time_now=None , min_rows=1000, max_rows=1500):
    os.makedirs(directory, exist_ok=True)
    row_count = random.randint(min_rows, max_rows)
    timestamp = time_now.strftime("%Y%m%d_%H%M%S") if time_now else datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{file_prefix}_{timestamp}.csv"
    filepath = os.path.join(directory, filename)
    max_nulls = int(row_count * 0.1)
    nulls_used = 0
    with open(filepath, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "product_id", "event_type", "event_time"])  # header
        for i in range(1, row_count + 1):
            # Only allow up to max_nulls rows to have nulls
            if nulls_used < max_nulls:
                # 10% chance for this row to have nulls, but not exceeding max_nulls
                make_null = random.random() < 0.1
            else:
                make_null = False
            if make_null:
                nulls_used += 1
                writer.writerow(generate_row_with_nulls(i))
            else:
                writer.writerow(generate_row_no_nulls(i))
    print(f"Created {filepath} with {row_count} rows.")

def main():
    output_dir = "source_data"
    # Generate files for 12 hours without waiting between files
    start_time = datetime.now() + timedelta(hours=datetime.now().hour)  # Start at the beginning of the current hour
    print(f"Starting file generation at {start_time}")
    end_time = start_time + timedelta(hours=2)
    print(f"Ending file generation at {end_time}")
    duration = 2 * 60 * 60  # 12 hours in seconds
    delta_dur = 5 * 60  # 5 minutes in seconds
    file_count = 0
    time_now = start_time
    while time_now < end_time:
        create_file_with_rows(output_dir, time_now=time_now)
        file_count += 1
        print(f"Created file #{file_count}")
        time_now += timedelta(seconds=delta_dur)
    print(f"Finished creating {file_count} files in 2 hours.")

if __name__ == "__main__":
    main()
