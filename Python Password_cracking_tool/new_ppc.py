import zipfile
import threading
from termcolor import colored

def extract_zip(zip_path, wordlist_file):
    """
    Tries to crack the password of a ZIP file using a wordlist.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as file:
                
                # Iterate through the wordlist and attempt extraction
                for line in file:
                    password = line.strip()
                    print(f"DEBUG: Trying password: '{password}'")
                    
                    try:
                        zip_file.extractall(pwd=password.encode('utf-8'))
                        print(colored(f"[+] Password cracked for {zip_path}: {password}", 'green', attrs=['bold']))
                        return password
                    
                    except (RuntimeError, zipfile.BadZipFile):
                        continue
            
            # If password is not found in wordlist
            print(colored(f"[-] Brute-force attack failed for {zip_path}. Password not found.", 'red', attrs=['bold']))
            return None
    
    except FileNotFoundError:
        print(f"[!] Error: '{zip_path}' or '{wordlist_file}' not found.")
        return None
    
    except Exception as e:
        print(f"[!] Error: {e}")
        return None

def crack_multiple_zips(zip_paths, wordlist_file):
    """
    Cracks multiple ZIP files using the same wordlist.
    """
    threads = []
    
    for zip_path in zip_paths:
        thread = threading.Thread(target=extract_zip, args=(zip_path, wordlist_file))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

def main():
    """
    Main function to handle user input and initiate the cracking process.
    """
    print("=" * 50)
    print("🔥 Advanced ZIP Password Cracker by Namita Shrestha 🔥")
    print("=" * 50)
    
    # User inputs
    zip_paths = input("[!] Enter paths to the ZIP files (comma-separated): ").strip().split(',')
    wordlist_file = input("[!] Enter path to the wordlist file: ").strip()
    
    # Validate inputs
    if not zip_paths or not wordlist_file:
        print("[!] Error: Please provide valid file paths.")
        return
    
    # Start cracking process
    crack_multiple_zips(zip_paths, wordlist_file)

if __name__ == "__main__":
    """
    Entry point of the script. Ensures 'termcolor' is installed before execution.
    """
    try:
        from termcolor import colored
    except ImportError:
        print("[!] 'termcolor' not found. Installing...")
        import os
        os.system("pip install termcolor")
        from termcolor import colored
    
    # Run main function
    main()
