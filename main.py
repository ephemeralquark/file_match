import os

def find_duplicates(path):
  """Finds all duplicate files in a directory and its subdirectories.

  Args:
    path: The path to the directory to search.

  Returns:
    A dictionary of hash to tuples, where each tuple contains all duplicate files for a given file.
  """

  duplicates = {}
  file_hashes = {}
  for root, _, files in os.walk(path):
    for file in files:
      file_path = os.path.join(root, file)
      file_hash = hash(open(file_path, "rb").read())
      if file_hash in file_hashes:
        if file_hash in duplicates:
          duplicates[file_hash].append(file_path)
        else:
          duplicates[file_hash] = [file_hashes[file_hash], file_path]
      else:
        file_hashes[file_hash] = file_path
  return duplicates

def find_original(file_paths):
    oldest_file_index = 0
    oldest_file_time = os.path.getmtime(file_paths[0])
    for i in range(1, len(file_paths)):
      file_time = os.path.getmtime(file_paths[i])
      if file_time < oldest_file_time:
        oldest_file_index = i
        oldest_file_time = file_time

    return oldest_file_index

def remove_duplicates(duplicates):
  """Removes all duplicate files, keeping the original file, with user verification before delete.

  Args:
    duplicates: A list of all duplicate files found.
  """
  for key in duplicates:
    file_paths = duplicates[key]
    index = find_original(file_paths)

    for i in range(0, len(file_paths)):
      if i != index:
        delete_file = file_paths[i]
        with open("deleted_files.txt", "a") as f:
          f.write(f"{delete_file}\n")
        # os.remove(delete_file)
        # print(f"Delete duplicate file: {delete_file}?")
        # user_input = input("y/n: ")
        # if user_input == "y":
        #   os.remove(delete_file)

if __name__ == "__main__":
  path = input("Enter the path to the directory to search: ")
  duplicates = find_duplicates(path)
  remove_duplicates(duplicates)
