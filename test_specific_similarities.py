#!/usr/bin/env python3
"""
Test specific text similarity cases
"""

import sys
import os
sys.path.append('/Users/sunnengsen/Documents/Code/script_mmo')

from logo_detector import LogoDetector

def test_specific_similarities():
    detector = LogoDetector('/opt/homebrew/bin/ffmpeg')
    
    # Test specific cases that should be grouped
    test_cases = [
        ("MOVING V", "-RMARK"),
        ("MOVING V", "G WATERMAR"),
        ("MOVING V", "NIC WATERKAAR"),
        ("MOVING V", "TEPKAARKO"),
        ("-RMARK", "G WATERMAR"),
        ("-RMARK", "NIC WATERKAAR"),
        ("G WATERMAR", "NIC WATERKAAR"),
        ("TEPKAARKO", "NIC WATERKAAR"),
        ("ATE", "G WATERMAR"),
        ("VII", "MOVING V"),
    ]
    
    print("Testing specific text similarity cases:")
    for text1, text2 in test_cases:
        similar = detector._texts_are_similar(text1, text2)
        print(f"'{text1}' vs '{text2}': {'Similar' if similar else 'Different'}")

if __name__ == "__main__":
    test_specific_similarities()
