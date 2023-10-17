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
            delay = float(parts[-2].replace("ms", ""))  # Delay in milliseconds
            delay_data[hop] = {"ip_address": ip_address, "delay": delay}
    
    return delay_data
