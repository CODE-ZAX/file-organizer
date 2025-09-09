#!/usr/bin/env python3
"""
Test script for TidyDesk rules functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_organizer.core.config import Config, OrganizationRule

def test_rules():
    """Test rules creation and management"""
    print("🧪 Testing TidyDesk Rules Functionality")
    print("=" * 40)
    
    # Create config
    config = Config()
    print(f"✅ Config loaded with {len(config.config.organization_rules)} default rules")
    
    # Test adding a new rule
    test_rule = OrganizationRule(
        name="Test Rule",
        file_extensions=[".test", ".tmp"],
        target_folder="Test Files",
        enabled=True
    )
    
    print(f"✅ Created test rule: {test_rule.name}")
    
    # Add rule to config
    config.add_organization_rule(test_rule)
    print(f"✅ Added rule to config. Total rules: {len(config.config.organization_rules)}")
    
    # Test getting rule
    retrieved_rule = config.get_organization_rule("Test Rule")
    if retrieved_rule:
        print(f"✅ Retrieved rule: {retrieved_rule.name}")
        print(f"   Extensions: {retrieved_rule.file_extensions}")
        print(f"   Target: {retrieved_rule.target_folder}")
        print(f"   Enabled: {retrieved_rule.enabled}")
    else:
        print("❌ Failed to retrieve rule")
    
    # Test rule validation
    print("\n🔍 Testing rule validation...")
    
    # Test valid rule
    valid_rule = OrganizationRule(
        name="Valid Rule",
        file_extensions=[".pdf", ".doc"],
        target_folder="Documents",
        enabled=True
    )
    print(f"✅ Valid rule created: {valid_rule.name}")
    
    # Test invalid rule (empty name)
    try:
        invalid_rule = OrganizationRule(
            name="",
            file_extensions=[".pdf"],
            target_folder="Documents",
            enabled=True
        )
        print("❌ Invalid rule was created (should have failed)")
    except Exception as e:
        print(f"✅ Invalid rule properly rejected: {e}")
    
    # Test rule removal
    print(f"\n🗑️  Testing rule removal...")
    initial_count = len(config.config.organization_rules)
    config.remove_organization_rule("Test Rule")
    final_count = len(config.config.organization_rules)
    
    if final_count == initial_count - 1:
        print("✅ Rule removed successfully")
    else:
        print(f"❌ Rule removal failed. Count: {initial_count} -> {final_count}")
    
    # Test rule update
    print(f"\n🔄 Testing rule update...")
    update_rule = OrganizationRule(
        name="Updated Rule",
        file_extensions=[".txt", ".md"],
        target_folder="Text Files",
        enabled=False
    )
    
    config.add_organization_rule(update_rule)
    print(f"✅ Added update rule: {update_rule.name}")
    
    # Update the rule
    updated_rule = OrganizationRule(
        name="Updated Rule",
        file_extensions=[".txt", ".md", ".rtf"],
        target_folder="Text Documents",
        enabled=True
    )
    
    config.remove_organization_rule("Updated Rule")
    config.add_organization_rule(updated_rule)
    print(f"✅ Updated rule: {updated_rule.name}")
    
    # Final verification
    final_rule = config.get_organization_rule("Updated Rule")
    if final_rule and final_rule.target_folder == "Text Documents":
        print(f"✅ Rule update verified: {final_rule.target_folder}")
    else:
        print("❌ Rule update verification failed")
    
    print(f"\n📊 Final rule count: {len(config.config.organization_rules)}")
    print("🎉 Rules functionality test completed!")

if __name__ == "__main__":
    test_rules()
