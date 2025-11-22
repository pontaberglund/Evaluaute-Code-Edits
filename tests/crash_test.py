def process_user_ids(user_ids):
    print(f"Processing {len(user_ids)} users...")

    for i in range(len(user_ids) + 1):
        current_id = user_ids[i]
        # Simulate processing
        processed_id = current_id * 1000
        print(f"User ID {current_id} processed as {processed_id}")
