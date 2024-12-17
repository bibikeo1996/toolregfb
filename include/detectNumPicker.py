import subprocess
import time
import re

def swipe_element(adb_path, start, end, duration=300):
    """Swipe the element based on given coordinates."""
    command = [
        adb_path, "shell", "input", "swipe", str(start[0]), str(start[1]), str(end[0]), str(end[1]), str(duration)
    ]
    subprocess.run(command, capture_output=True, text=True)
    print(f"Swiped from {start} to {end}")

def get_number_picker_values(adb_path, resource_id):
    """Get all number picker values with the same resource ID."""
    # Dump UI XML
    subprocess.run([adb_path, "shell", "uiautomator", "dump", "/sdcard/window_dump.xml"], capture_output=True, text=True)
    subprocess.run([adb_path, "pull", "/sdcard/window_dump.xml", "./window_dump.xml"], capture_output=True, text=True)
    
    # Read and parse the dumped XML
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        content = file.read()
    
    # Find all values with the specified resource_id
    matches = re.findall(rf'resource-id="{resource_id}".*?text="([^"]+)"', content)
    return matches if matches else []

def format_picker_values(values):
    """Format picker values into Month, Day, and Year."""
    if len(values) >= 3:
        return {"Month": values[0], "Day": values[1], "Year": values[2]}
    return {"Month": "N/A", "Day": "N/A", "Year": "N/A"}

def swipe_field_until_target(adb_path, resource_id, target_value, swipe_coords):
    """Swipe a single field until the target value is reached."""
    while True:
        # Get the current values of the number picker fields
        current_values = get_number_picker_values(adb_path, resource_id)
        if not current_values:
            print("Error: Could not retrieve current values.")
            return

        current_value = current_values[0]  # First field value
        print(f"Current value: {current_value}, Target: {target_value}")

        if current_value == target_value:
            print(f"Field reached target value: {current_value}")
            break

        # Perform the swipe
        swipe_element(adb_path, swipe_coords[0], swipe_coords[1])
        time.sleep(1)  # Wait for swipe and UI update

def swipe_all_fields(adb_path, resource_id, target_values, swipe_coords_list):
    """
    Swipe each field individually (Month, Day, Year) until target values are reached.
    - swipe_coords_list: List of start/end coordinates for each field swipe.
    """
    print("Starting to swipe fields...")
    for i, target_value in enumerate(target_values):
        print(f"\nSwiping field {i + 1}: Target Value = {target_value}")
        swipe_field_until_target(adb_path, resource_id, target_value, swipe_coords_list[i])

    # Final check after swiping all fields
    final_values = get_number_picker_values(adb_path, resource_id)
    formatted_values = format_picker_values(final_values)
    print("\nFinal values:")
    print(f"Month: {formatted_values['Month']}, Day: {formatted_values['Day']}, Year: {formatted_values['Year']}")
    print("Swiping complete!")
