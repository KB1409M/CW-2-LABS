# Function to be used in main.py or a helper file

# NOTE: Requires pandas, connect_database, and DATA_DIR from imports
def load_csv_to_table(conn, csv_path, table_name):
    """Load a CSV file into a database table using pandas."""
    csv_file = Path(csv_path)

    if not csv_file.exists():
        print(f" CSV file not found: {csv_file}. Skipping {table_name}.")
        return 0

    try:
        df = pd.read_csv(csv_file)
        rows_loaded = df.to_sql(
            name=table_name,
            con=conn,
            if_exists='append',
            index=False
        )
        print(f" Loaded {rows_loaded} rows into {table_name} from {csv_file.name}.")
        return rows_loaded
    except Exception as e:
        print(f"Error loading CSV {csv_file.name} into {table_name}: {e}")
        return 0


def load_all_csv_data(conn):
    """Load data for all three main tables."""
    total_rows = 0
    total_rows += load_csv_to_table(conn, DATA_DIR / "cyber_incidents.csv", "cyber_incidents")
    total_rows += load_csv_to_table(conn, DATA_DIR / "datasets_metadata.csv", "datasets_metadata")
    total_rows += load_csv_to_table(conn, DATA_DIR / "it_tickets.csv", "it_tickets")
    return total_rows