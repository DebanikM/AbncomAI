"""
Simple test script to verify that imports are working correctly.
Run this script to test if the basic imports and dependencies are functioning.
"""

def test_imports():
    """Test that all required imports work correctly."""
    try:
        # Core dependencies
        import streamlit
        print("✅ Streamlit import successful")
        
        import textstat
        print("✅ Textstat import successful")
        
        import dotenv
        print("✅ Python-dotenv import successful")
        
        # Try to import google.generativeai, but don't fail if it's not available
        # since it requires an API key to fully function
        try:
            import google.generativeai
            print("✅ Google Generative AI import successful")
        except ImportError:
            print("⚠️ Google Generative AI import failed - may need to install")
        
        # Our custom modules
        from utils import gemini_utils, text_analysis, templates
        print("✅ Custom modules import successful")
        
        print("\nAll critical imports successful! The application should be able to start.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease run 'pip install -r requirements.txt' to install dependencies.")

if __name__ == "__main__":
    test_imports() 