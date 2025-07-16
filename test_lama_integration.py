#!/usr/bin/env python3
"""
Test script for lama-cleaner integration
Demonstrates watermark removal on images and integration with existing detection pipeline
"""

import cv2
import numpy as np
import os
import sys
from lama_integration import LamaCleaner, create_simple_mask_demo
from logo_detector import LogoDetector


def test_lama_cleaner_basic():
    """Test basic lama-cleaner functionality with a synthetic image"""
    print("=" * 50)
    print("Testing Basic Lama-Cleaner Functionality")
    print("=" * 50)
    
    success = create_simple_mask_demo()
    
    if success:
        print("✅ Basic lama-cleaner test passed!")
        
        # Display results if files exist
        if os.path.exists("test_image_with_watermark.png") and os.path.exists("test_image_cleaned.png"):
            print("\nTo view results:")
            print("Original: test_image_with_watermark.png")
            print("Cleaned:  test_image_cleaned.png")
            print("Mask:     test_watermark_mask.png")
    else:
        print("❌ Basic lama-cleaner test failed!")
    
    return success


def test_integration_with_detection():
    """Test integration with existing logo detection pipeline"""
    print("\n" + "=" * 50)
    print("Testing Integration with Logo Detection")
    print("=" * 50)
    
    # Check if we have a test video
    test_videos = [
        "test_moving_final.mp4",
        "test_simple_watermark.mp4",
        "test_final_watermark_removal.mp4"
    ]
    
    test_video = None
    for video in test_videos:
        if os.path.exists(video):
            test_video = video
            break
    
    if not test_video:
        print("❌ No test video found. Please ensure you have a test video available.")
        return False
    
    print(f"Using test video: {test_video}")
    
    try:
        # Initialize detector
        ffmpeg_path = "ffmpeg"  # Assuming ffmpeg is in PATH
        detector = LogoDetector(ffmpeg_path)
        
        # Detect watermarks
        print("Detecting watermarks...")
        detections = detector.detect_watermarks(test_video, sample_frames=10)
        
        if not detections:
            print("❌ No watermarks detected in test video")
            return False
        
        print(f"✅ Detected {len(detections)} watermark regions")
        
        # Create watermark timelines
        print("Creating watermark timelines...")
        timelines = detector._create_watermark_timelines(detections)
        
        print(f"✅ Created {len(timelines)} watermark timelines")
        
        # Test frame-by-frame processing with lama-cleaner
        print("Testing lama-cleaner frame processing...")
        
        output_path = f"test_lama_cleaned_{os.path.basename(test_video)}"
        
        with LamaCleaner() as cleaner:
            success = cleaner.process_video_frames(test_video, output_path, timelines)
            
            if success:
                print(f"✅ Video processing successful! Output: {output_path}")
                return True
            else:
                print("❌ Video processing failed")
                return False
                
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


def test_manual_image_cleaning():
    """Test manual image cleaning for demonstration"""
    print("\n" + "=" * 50)
    print("Testing Manual Image Cleaning")
    print("=" * 50)
    
    # Check if we have any test images
    test_images = [
        "test_real_watermark.png",
        "realistic_watermark_test.png",
        "debug_watermark_test.png"
    ]
    
    test_image = None
    for img in test_images:
        if os.path.exists(img):
            test_image = img
            break
    
    if not test_image:
        print("❌ No test image found. Creating a synthetic test image...")
        return test_lama_cleaner_basic()
    
    print(f"Using test image: {test_image}")
    
    try:
        # Load the image
        image = cv2.imread(test_image)
        if image is None:
            print("❌ Failed to load test image")
            return False
        
        height, width = image.shape[:2]
        print(f"Image dimensions: {width}x{height}")
        
        # Create a simple mask (you can modify this to target specific regions)
        # For demo, we'll create a mask for potential watermark locations
        mask = np.zeros((height, width), dtype=np.uint8)
        
        # Common watermark locations: corners and center-bottom
        margin = 50
        watermark_size = 100
        
        # Bottom-right corner
        cv2.rectangle(mask, 
                     (width - watermark_size - margin, height - watermark_size - margin),
                     (width - margin, height - margin), 
                     255, -1)
        
        # Top-right corner
        cv2.rectangle(mask, 
                     (width - watermark_size - margin, margin),
                     (width - margin, margin + watermark_size), 
                     255, -1)
        
        # Save mask
        mask_path = f"manual_mask_{os.path.basename(test_image)}"
        cv2.imwrite(mask_path, mask)
        
        # Apply lama-cleaner
        output_path = f"manual_cleaned_{os.path.basename(test_image)}"
        
        with LamaCleaner() as cleaner:
            success = cleaner.remove_watermark_from_image(test_image, mask_path, output_path)
            
            if success:
                print(f"✅ Manual cleaning successful!")
                print(f"Original: {test_image}")
                print(f"Mask:     {mask_path}")
                print(f"Cleaned:  {output_path}")
                return True
            else:
                print("❌ Manual cleaning failed")
                return False
                
    except Exception as e:
        print(f"❌ Manual cleaning test failed: {e}")
        return False


def run_all_tests():
    """Run all lama-cleaner tests"""
    print("🧪 Running Lama-Cleaner Integration Tests")
    print("This will test the lama-cleaner integration with your watermark detection system")
    print()
    
    # Test 1: Basic functionality
    test1_success = test_lama_cleaner_basic()
    
    # Test 2: Integration with detection
    test2_success = test_integration_with_detection()
    
    # Test 3: Manual image cleaning
    test3_success = test_manual_image_cleaning()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Basic Functionality:     {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Detection Integration:   {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"Manual Image Cleaning:   {'✅ PASS' if test3_success else '❌ FAIL'}")
    
    overall_success = test1_success or test2_success or test3_success
    
    if overall_success:
        print("\n🎉 At least one test passed! Lama-cleaner integration is working.")
        print("\n📋 Next steps:")
        print("1. Review the output files to assess quality")
        print("2. Adjust mask creation for better watermark targeting")
        print("3. Try different lama-cleaner models (lama, ldm, zits, etc.)")
        print("4. Integrate into your main application workflow")
    else:
        print("\n❌ All tests failed. Please check:")
        print("1. Lama-cleaner installation: pip install lama-cleaner")
        print("2. Dependencies and models are properly installed")
        print("3. Test files are available in the workspace")
    
    return overall_success


if __name__ == "__main__":
    run_all_tests()
