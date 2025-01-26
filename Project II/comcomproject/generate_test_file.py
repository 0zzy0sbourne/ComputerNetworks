def generate_test_file():
   # Generate 1000 lines of dummy text
   content = []
   for i in range(100):
       content.append(f"Test line {i}: This is a longer line of text with multiple words to increase the packet size substantially.")
   
   # Write to file
   with open('input.txt', 'w') as f:
       f.write('\n'.join(content))

generate_test_file()