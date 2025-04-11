#!/usr/bin/env python3
"""
System Test Script

This script tests all components of the Business Finder & Website Generator system.
"""

import os
import sys
import json
import sqlite3
import subprocess
import time
from datetime import datetime

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80 + "\n")

def print_result(test_name, success, message=""):
    """Print a test result."""
    if success:
        print(f"✅ {test_name}: PASSED")
    else:
        print(f"❌ {test_name}: FAILED - {message}")

def test_directory_structure():
    """Test that all required directories exist."""
    print_header("Testing Directory Structure")
    
    required_dirs = [
        "analytics",
        "data",
        "docs",
        "integrations",
        "outreach",
        "pageandbrand",
        "tools",
        "ui",
        "website_generator",
        "setup"
    ]
    
    all_exist = True
    for directory in required_dirs:
        exists = os.path.isdir(directory)
        print(f"Directory '{directory}': {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_exist = False
    
    print_result("Directory Structure", all_exist)
    return all_exist

def test_documentation():
    """Test that all documentation files exist."""
    print_header("Testing Documentation")
    
    required_docs = [
        "docs/user_manual.md",
        "docs/technical_setup_guide.md",
        "docs/api_key_reference.md",
        "docs/quick_start_guide.md",
        "README.md"
    ]
    
    all_exist = True
    for doc in required_docs:
        exists = os.path.isfile(doc)
        print(f"Documentation '{doc}': {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_exist = False
    
    print_result("Documentation", all_exist)
    return all_exist

def test_business_finder():
    """Test the business finder tool."""
    print_header("Testing Business Finder Tool")
    
    # Check if files exist
    files_to_check = [
        "tools/business_finder.py",
        "tools/business_finder_cli.py"
    ]
    
    all_files_exist = True
    for file in files_to_check:
        exists = os.path.isfile(file)
        print(f"File '{file}': {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_files_exist = False
    
    # Check if files are executable
    all_files_executable = True
    for file in files_to_check:
        if os.path.isfile(file):
            is_executable = os.access(file, os.X_OK)
            print(f"File '{file}': {'✅ Executable' if is_executable else '❌ Not executable'}")
            if not is_executable:
                all_files_executable = False
    
    # Test import
    try:
        sys.path.append(os.getcwd())
        from tools.business_finder import BusinessFinder
        print("✅ BusinessFinder class can be imported")
        import_success = True
    except ImportError as e:
        print(f"❌ Failed to import BusinessFinder: {str(e)}")
        import_success = False
    
    # Overall result
    success = all_files_exist and all_files_executable and import_success
    print_result("Business Finder Tool", success)
    return success

def test_outreach_system():
    """Test the outreach system."""
    print_header("Testing Outreach System")
    
    # Check if files exist
    files_to_check = [
        "outreach/outreach_generator.py",
        "outreach/outreach_cli.py",
        "outreach/outreach_automation.py"
    ]
    
    all_files_exist = True
    for file in files_to_check:
        exists = os.path.isfile(file)
        print(f"File '{file}': {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_files_exist = False
    
    # Check if files are executable
    all_files_executable = True
    for file in files_to_check:
        if os.path.isfile(file):
            is_executable = os.access(file, os.X_OK)
            print(f"File '{file}': {'✅ Executable' if is_executable else '❌ Not executable'}")
            if not is_executable:
                all_files_executable = False
    
    # Overall result
    success = all_files_exist and all_files_executable
    print_result("Outreach System", success)
    return success

def test_website_generator():
    """Test the website generator."""
    print_header("Testing Website Generator")
    
    # Check if files exist
    files_to_check = [
        "website_generator/website_generator.py",
        "website_generator/website_generator_cli.py",
        "website_generator/website_generator_integration.py"
    ]
    
    all_files_exist = True
    for file in files_to_check:
        exists = os.path.isfile(file)
        print(f"File '{file}': {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_files_exist = False
    
    # Check if files are executable
    all_files_executable = True
    for file in files_to_check:
        if os.path.isfile(file):
            is_executable = os.access(file, os.X_OK)
            print(f"File '{file}': {'✅ Executable' if is_executable else '❌ Not executable'}")
            if not is_executable:
                all_files_executable = False
    
    # Test import
    try:
        sys.path.append(os.getcwd())
        from website_generator.website_generator import WebsiteGenerator
        print("✅ WebsiteGenerator class can be imported")
        import_success = True
    except ImportError as e:
        print(f"❌ Failed to import WebsiteGenerator: {str(e)}")
        import_success = False
    
    # Overall result
    success = all_files_exist and all_files_executable and import_success
    print_result("Website Generator", success)
    return success

def test_calendly_integration():
    """Test the Calendly integration."""
    print_header("Testing Calendly Integration")
    
    # Check if files exist
    files_to_check = [
        "integrations/calendly_integration.py"
    ]
    
    all_files_exist = True
    for file in files_to_check:
        exists = os.path.isfile(file)
        print(f"File '{file}': {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_files_exist = False
    
    # Check if files are executable
    all_files_executable = True
    for file in files_to_check:
        if os.path.isfile(file):
            is_executable = os.access(file, os.X_OK)
            print(f"File '{file}': {'✅ Executable' if is_executable else '❌ Not executable'}")
            if not is_executable:
                all_files_executable = False
    
    # Test import
    try:
        sys.path.append(os.getcwd())
        from integrations.calendly_integration import CalendlyIntegration
        print("✅ CalendlyIntegration class can be imported")
        import_success = True
    except ImportError as e:
        print(f"❌ Failed to import CalendlyIntegration: {str(e)}")
        import_success = False
    
    # Overall result
    success = all_files_exist and all_files_executable and import_success
    print_result("Calendly Integration", success)
    return success

def test_analytics_system():
    """Test the analytics system."""
    print_header("Testing Analytics System")
    
    # Check if files exist
    files_to_check = [
        "analytics/message_analytics.py",
        "analytics/analytics_integration.py"
    ]
    
    all_files_exist = True
    for file in files_to_check:
        exists = os.path.isfile(file)
        print(f"File '{file}': {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_files_exist = False
    
    # Check if files are executable
    all_files_executable = True
    for file in files_to_check:
        if os.path.isfile(file):
            is_executable = os.access(file, os.X_OK)
            print(f"File '{file}': {'✅ Executable' if is_executable else '❌ Not executable'}")
            if not is_executable:
                all_files_executable = False
    
    # Test import
    try:
        sys.path.append(os.getcwd())
        from analytics.message_analytics import MessageAnalytics
        print("✅ MessageAnalytics class can be imported")
        import_success = True
    except ImportError as e:
        print(f"❌ Failed to import MessageAnalytics: {str(e)}")
        import_success = False
    
    # Overall result
    success = all_files_exist and all_files_executable and import_success
    print_result("Analytics System", success)
    return success

def test_pageandbrand_website():
    """Test the PageAndBrand website."""
    print_header("Testing PageAndBrand Website")
    
    # Check if files exist
    files_to_check = [
        "pageandbrand/index.html",
        "pageandbrand/styles.css",
        "pageandbrand/scripts.js"
    ]
    
    all_files_exist = True
    for file in files_to_check:
        exists = os.path.isfile(file)
        print(f"File '{file}': {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_files_exist = False
    
    # Check if images directory exists and has content
    images_dir = "pageandbrand/images"
    if os.path.isdir(images_dir):
        images = os.listdir(images_dir)
        if images:
            print(f"✅ Images directory exists and contains {len(images)} files")
            images_exist = True
        else:
            print("❌ Images directory exists but is empty")
            images_exist = False
    else:
        print("❌ Images directory does not exist")
        images_exist = False
    
    # Overall result
    success = all_files_exist and images_exist
    print_result("PageAndBrand Website", success)
    return success

def test_ui_components():
    """Test the UI components."""
    print_header("Testing UI Components")
    
    # Check if files exist
    files_to_check = [
        "ui/app.py",
        "ui/templates/index.html",
        "ui/templates/leads.html",
        "ui/templates/website_generator.html"
    ]
    
    all_files_exist = True
    for file in files_to_check:
        exists = os.path.isfile(file)
        print(f"File '{file}': {'✅ Exists' if exists else '❌ Missing'}")
        if not exists:
            all_files_exist = False
    
    # Overall result
    success = all_files_exist
    print_result("UI Components", success)
    return success

def create_test_summary(results):
    """Create a summary of test results."""
    print_header("Test Summary")
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(passed_tests / total_tests) * 100:.1f}%")
    
    if failed_tests == 0:
        print("\n✅ All tests passed! The system is ready for delivery.")
    else:
        print("\n❌ Some tests failed. Please fix the issues before delivery.")
    
    # Create a test report file
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "success_rate": (passed_tests / total_tests) * 100,
        "results": results
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\nTest report saved to data/test_report.json")

def main():
    """Run all tests."""
    print_header("Business Finder & Website Generator System Test")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    results = {
        "Directory Structure": test_directory_structure(),
        "Documentation": test_documentation(),
        "Business Finder": test_business_finder(),
        "Outreach System": test_outreach_system(),
        "Website Generator": test_website_generator(),
        "Calendly Integration": test_calendly_integration(),
        "Analytics System": test_analytics_system(),
        "PageAndBrand Website": test_pageandbrand_website(),
        "UI Components": test_ui_components()
    }
    
    # Create summary
    create_test_summary(results)

if __name__ == "__main__":
    main()
