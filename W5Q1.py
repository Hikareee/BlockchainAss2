#!/usr/bin/env python3

import hashlib

def find_hash_with_leading_zeros(base_string, leading_zeros=3, hash_algorithm='md5'):
	target_prefix = '0' * leading_zeros
	iteration_count = 0
	
	while True:
		iteration_count += 1
		# The number to append
		combined_string = f"{base_string}{iteration_count}"
		
		# Calculate the hash based on the selected algorithm
		if hash_algorithm == 'md5':
			hash_result = hashlib.md5(combined_string.encode()).hexdigest()
		elif hash_algorithm == 'sha256':
			hash_result = hashlib.sha256(combined_string.encode()).hexdigest()
		elif hash_algorithm == 'sha512':
			hash_result = hashlib.sha512(combined_string.encode()).hexdigest()
		else:
			raise ValueError("Invalid hash algorithm selected.")
			
		# Check if the hash starts with the required number of leading zeros
		if hash_result.startswith(target_prefix):
			return iteration_count, combined_string, hash_result
		
# Get input from the user
base_string = input("Enter the base string: ")
leading_zeros = int(input("Enter the number of leading zeros: "))

# Select the hash algorithm
print("Choose the hash algorithm:")
print("1. MD5")
print("2. SHA-256")
print("3. SHA-512")
algorithm_choice = input("Enter the number corresponding to your choice: ")

# Map the user's choice to the hash algorithm
if algorithm_choice == '1':
	hash_algorithm = 'md5'
elif algorithm_choice == '2':
	hash_algorithm = 'sha256'
elif algorithm_choice == '3':
	hash_algorithm = 'sha512'
else:
	raise ValueError("Invalid choice. Please select 1, 2, or 3.")
	
# Run the function to find the correct hash
iterations, correct_string, found_hash = find_hash_with_leading_zeros(base_string, leading_zeros, hash_algorithm)

# Output the results
print(f"\nNumber of iterations: {iterations}")
print(f"Correct string: {correct_string}")
print(f"{hash_algorithm.upper()} hash: {found_hash}")
