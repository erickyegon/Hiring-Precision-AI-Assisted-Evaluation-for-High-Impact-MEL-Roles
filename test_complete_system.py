"""
Test the complete CV analysis system with Euriai integration
"""

import asyncio
import os
from utils.euri_client import EuriClient
from utils.ai_analyzer_clean import ProfessionalCVAnalyzer
from utils.document_processor import DocumentProcessor

async def test_complete_system():
    """Test the complete system end-to-end"""
    print("🧪 Testing Complete CV Analysis System")
    print("=" * 50)
    
    # Test 1: Euriai Client
    print("1. Testing Euriai Client...")
    try:
        client = EuriClient()
        test_response = client.chat_completion([
            {"role": "user", "content": "Say 'Euriai is working!'"}
        ], max_tokens=10)
        print(f"✅ Euriai client works: {test_response}")
    except Exception as e:
        print(f"❌ Euriai client failed: {str(e)}")
        return False
    
    # Test 2: Document Processing
    print("\n2. Testing Document Processing...")
    try:
        processor = DocumentProcessor()
        
        # Check if CV directory exists
        cv_dir = "CVs"
        if not os.path.exists(cv_dir):
            print(f"❌ CV directory '{cv_dir}' not found")
            return False
        
        # Process a few sample files
        cv_files = []
        for file in os.listdir(cv_dir):
            if file.lower().endswith(('.pdf', '.docx', '.doc')):
                cv_files.append(os.path.join(cv_dir, file))
                if len(cv_files) >= 3:
                    break
        
        if not cv_files:
            print("❌ No CV files found for testing")
            return False
        
        print(f"Found {len(cv_files)} CV files for testing")
        
        # Process sample files
        sample_data = []
        for cv_file in cv_files:
            result = processor.process_single_file(cv_file)
            if not result.get('error') and result.get('text'):
                sample_data.append(result)
                print(f"✅ Processed: {result['filename']} ({result['word_count']} words)")
            else:
                print(f"❌ Failed: {cv_file}")
        
        if not sample_data:
            print("❌ No CV files processed successfully")
            return False
        
    except Exception as e:
        print(f"❌ Document processing failed: {str(e)}")
        return False
    
    # Test 3: Hybrid AI Analysis
    print(f"\n3. Testing Hybrid AI Analysis with {len(sample_data)} CVs...")
    try:
        # Get API key from environment
        euriai_key = os.getenv("EURI_API_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJlZDljYzlkYy0xZmQ2LTRiMGMtODcyZS1lYmJlMmRjNjZiNzQiLCJlbWFpbCI6ImtleWVnb25AZ21haWwuY29tIiwiaWF0IjoxNzQ3MDM0Nzc2LCJleHAiOjE3Nzg1NzA3NzZ9.6m2jzZ_A7eGmoBYjzP7lLazn1luxIFUIYOsbS6ttKS0"
        
        analyzer = ProfessionalCVAnalyzer(euriai_api_key=euriai_key)
        
        # Test single CV analysis
        first_cv = sample_data[0]
        print(f"Analyzing: {first_cv['filename']}")
        
        result = await analyzer.analyze_cv(
            first_cv['text'], 
            first_cv['filename']
        )
        
        if result:
            print("✅ Single CV analysis successful!")
            print(f"   Overall Score: {result.overall_score:.1f}")
            print(f"   Ranking Tier: {result.ranking_tier}")
            print(f"   Strengths: {len(result.strengths)}")
            print(f"   Provider: {result.strengths[0] if result.strengths else 'Unknown'}")
        else:
            print("❌ Single CV analysis failed")
            return False
        
        # Test batch analysis (small batch)
        print(f"\n4. Testing batch analysis with {len(sample_data)} CVs...")
        
        batch_results = await analyzer.analyze_batch(sample_data[:2])  # Test with 2 CVs
        
        if batch_results:
            print(f"✅ Batch analysis successful! {len(batch_results)} CVs analyzed")
            
            for i, result in enumerate(batch_results, 1):
                provider = "Unknown"
                if result.strengths and "[" in result.strengths[0]:
                    provider = result.strengths[0].split("]")[0].replace("[", "")
                
                print(f"   {i}. {result.filename}: {result.overall_score:.1f} ({result.ranking_tier}) - {provider}")
        else:
            print("❌ Batch analysis failed")
            return False
        
    except Exception as e:
        print(f"❌ AI analysis failed: {str(e)}")
        return False
    
    # Test Summary
    print("\n" + "=" * 50)
    print("🎉 Complete System Test Results")
    print("=" * 50)
    print("✅ Euriai Client: Working")
    print("✅ Document Processing: Working")
    print("✅ AI Analysis: Working")
    print("✅ Batch Processing: Working")
    
    print(f"\n📊 Test Results:")
    print(f"- CVs Processed: {len(sample_data)}")
    print(f"- CVs Analyzed: {len(batch_results)}")
    print(f"- Success Rate: {len(batch_results)/len(sample_data)*100:.1f}%")
    
    print(f"\n🚀 System Status: FULLY OPERATIONAL")
    print(f"Your MEL Manager CV Analysis System is ready for production use!")
    
    return True

def main():
    """Main test function"""
    try:
        success = asyncio.run(test_complete_system())
        
        if success:
            print("\n🎯 Next Steps:")
            print("1. Launch the hybrid batch processor: streamlit run hybrid_batch_processor.py --server.port 8506")
            print("2. Process your 374 CVs with Euriai as the primary provider")
            print("3. View results with detailed rankings and justifications")
            print("4. Export comprehensive reports for your recruitment team")
        else:
            print("\n❌ System test failed. Please check the errors above.")
            
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
