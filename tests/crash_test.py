def process_user_ids(user_ids):
    print(f"Processing {len(user_ids)} users...")

    # THE CRASH: range(len()) goes from 0 to length-1.
    # Adding +1 makes the loop try to access an index that doesn't exist.
    for i in range(len(user_ids) + 1):
        current_id = user_ids[i]
        # Simulate processing
        processed_id = current_id * 1000
        print(f"User ID {current_id} processed as {processed_id}")


# Example usage
ids = [1, 2, 3, 4, 5]
process_user_ids(ids)
