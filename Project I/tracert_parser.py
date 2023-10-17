def parse_tracert_output(output):
    delay_data = {}
    lines = output.splitlines()
    
    for line in lines:
        if "Request timed out" in line:
            # Handle cases where there's a timeout for a hop
            pass
        elif "ms" in line:
            # This line contains delay information
            parts = line.split()
            hop = int(parts[0])  # Hop number
            ip_address = parts[1]  # IP address or domain name
            try:
                delay = float(parts[-2].replace("ms", ""))  # Delay in milliseconds
            except ValueError:
                # Handle the case where the line contains a hostname instead of a delay
                delay = None  # Or any other appropriate value
            delay_data[hop] = {"ip_address": ip_address, "delay": delay}
    
    return delay_data
