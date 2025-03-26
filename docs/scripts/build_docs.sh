#!/bin/bash
# Documentation Build Script for Hephaestus
# This script provides an easy way to run the various documentation scripts

set -e  # Exit on error

# Function to display the menu
show_menu() {
  echo ""
  echo "Hephaestus Documentation Tools"
  echo "------------------------------"
  echo ""
  echo "Please select an option:"
  echo "1. Set up documentation structure"
  echo "2. Migrate existing documentation"
  echo "3. Generate component documentation"
  echo "4. Run MkDocs server (preview)"
  echo "5. Build documentation site"
  echo "6. Run complete documentation pipeline"
  echo "7. Exit"
  echo ""
}

# Function to run the setup script
run_setup() {
  echo ""
  echo "Running documentation setup script..."
  python3 docs/scripts/setup_docs.py
  echo ""
  read -p "Press Enter to continue..."
}

# Function to run the migration script
run_migrate() {
  echo ""
  echo "Running documentation migration script..."
  python3 docs/scripts/migrate_docs.py
  echo ""
  read -p "Press Enter to continue..."
}

# Function to run the component documentation generator
run_generate() {
  echo ""
  echo "Running component documentation generator..."
  python3 docs/scripts/generate_component_docs.py
  echo ""
  read -p "Press Enter to continue..."
}

# Function to start the MkDocs server
run_serve() {
  echo ""
  echo "Starting MkDocs server for preview..."
  echo "The documentation will be available at http://127.0.0.1:8000/"
  echo "Press Ctrl+C to stop the server."
  echo ""
  mkdocs serve
}

# Function to build the documentation site
run_build() {
  echo ""
  echo "Building documentation site..."
  mkdocs build --clean
  echo ""
  echo "Documentation site built in the 'site' directory."
  read -p "Press Enter to continue..."
}

# Function to run the complete pipeline
run_pipeline() {
  echo ""
  echo "Running complete documentation pipeline..."
  echo ""
  echo "Step 1: Setting up documentation structure..."
  python3 docs/scripts/setup_docs.py
  echo ""
  echo "Step 2: Migrating existing documentation..."
  python3 docs/scripts/migrate_docs.py
  echo ""
  echo "Step 3: Generating component documentation..."
  python3 docs/scripts/generate_component_docs.py
  echo ""
  echo "Step 4: Building documentation site..."
  mkdocs build --clean
  echo ""
  echo "Documentation pipeline completed."
  echo "The built site is available in the 'site' directory."
  read -p "Press Enter to continue..."
}

# Main loop
while true; do
  show_menu
  read -p "Enter your choice (1-7): " choice
  
  case $choice in
    1) run_setup ;;
    2) run_migrate ;;
    3) run_generate ;;
    4) run_serve ;;
    5) run_build ;;
    6) run_pipeline ;;
    7) 
      echo ""
      echo "Exiting documentation tools."
      exit 0
      ;;
    *)
      echo "Invalid choice. Please try again."
      ;;
  esac
done 