#!/usr/bin/env python3
"""
Simple demo of TidyDesk rules functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from file_organizer.core.config import Config, OrganizationRule

def main():
    """Simple rules demo"""
    print("🎯 TidyDesk Rules Demo")
    print("=" * 30)
    
    # Create config
    config = Config()
    print(f"📋 Loaded {len(config.config.organization_rules)} default rules")
    
    # Show existing rules
    print("\n📝 Existing Rules:")
    for i, rule in enumerate(config.config.organization_rules, 1):
        print(f"  {i}. {rule.name}")
        print(f"     Extensions: {', '.join(rule.file_extensions)}")
        print(f"     Target: {rule.target_folder}")
        print(f"     Enabled: {rule.enabled}")
        print()
    
    # Create a custom rule
    print("➕ Creating custom rule...")
    custom_rule = OrganizationRule(
        name="My Custom Files",
        file_extensions=[".myfile", ".custom"],
        target_folder="Custom Files",
        enabled=True
    )
    
    config.add_organization_rule(custom_rule)
    print(f"✅ Created rule: {custom_rule.name}")
    
    # Show updated rules
    print(f"\n📋 Updated rules count: {len(config.config.organization_rules)}")
    
    # Test rule retrieval
    retrieved = config.get_organization_rule("My Custom Files")
    if retrieved:
        print(f"✅ Retrieved rule: {retrieved.name}")
        print(f"   Extensions: {retrieved.file_extensions}")
        print(f"   Target: {retrieved.target_folder}")
    
    # Test rule removal
    print(f"\n🗑️  Removing rule...")
    config.remove_organization_rule("My Custom Files")
    print(f"✅ Removed rule. New count: {len(config.config.organization_rules)}")
    
    print("\n🎉 Demo completed successfully!")
    print("\n💡 To use the GUI:")
    print("   python3 -m file_organizer --gui")
    print("   Then click 'Custom Rules' to manage rules")

if __name__ == "__main__":
    main()
