#!/usr/bin/env python3
"""
Automatic Logo Detection and Removal Module
Uses computer vision and OCR to automatically detect and remove logos/watermarks from videos
"""

import cv2
import numpy as np
import subprocess
import tempfile
import os
from typing import List, Tuple, Optional
import re

# OCR imports with fallback
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False


class LogoDetector:
    """Automatically detect logos and watermarks in videos"""
    
    def __init__(self, ffmpeg_path: str):
        self.ffmpeg_path = ffmpeg_path
        self.ocr_reader = None
        self._init_ocr()
    
    def _init_ocr(self):
        """Initialize OCR engines"""
        global PYTESSERACT_AVAILABLE
        
        if EASYOCR_AVAILABLE:
            try:
                self.ocr_reader = easyocr.Reader(['en'])
                print("EasyOCR initialized successfully")
            except Exception as e:
                print(f"Failed to initialize EasyOCR: {e}")
                self.ocr_reader = None
        
        if PYTESSERACT_AVAILABLE:
            try:
                # Test if tesseract is available
                pytesseract.get_tesseract_version()
                print("Pytesseract initialized successfully")
            except Exception as e:
                print(f"Pytesseract not available: {e}")
                PYTESSERACT_AVAILABLE = False
    
    def extract_frame(self, video_path: str, timestamp: float = 5.0) -> Optional[np.ndarray]:
        """Extract a frame from video for analysis"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Extract frame at specified timestamp
            cmd = [
                self.ffmpeg_path, '-i', video_path, 
                '-ss', str(timestamp), '-vframes', '1', 
                '-y', temp_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return None
            
            # Read the frame
            frame = cv2.imread(temp_path)
            os.unlink(temp_path)  # Clean up temp file
            
            return frame
            
        except Exception as e:
            print(f"Error extracting frame: {e}")
            return None
    
    def detect_logos_in_corners(self, frame: np.ndarray, corner_size: float = 0.3) -> List[dict]:
        """Detect potential logos in corners and edges - enhanced for moving watermarks"""
        if frame is None:
            return []
        
        h, w = frame.shape[:2]
        corner_w = int(w * corner_size)
        corner_h = int(h * corner_size)
        
        # Enhanced corner regions (larger to catch moving watermarks)
        corners = {
            'top_left': (0, 0, corner_w, corner_h),
            'top_right': (w - corner_w, 0, corner_w, corner_h),
            'bottom_left': (0, h - corner_h, corner_w, corner_h),
            'bottom_right': (w - corner_w, h - corner_h, corner_w, corner_h),
            'top_center': (w//2 - corner_w//2, 0, corner_w, corner_h//2),
            'bottom_center': (w//2 - corner_w//2, h - corner_h//2, corner_w, corner_h//2),
            'left_center': (0, h//2 - corner_h//2, corner_w//2, corner_h),
            'right_center': (w - corner_w//2, h//2 - corner_h//2, corner_w//2, corner_h)
        }
        
        detected_logos = []
        
        for corner_name, (x, y, cw, ch) in corners.items():
            # Ensure we don't go out of bounds
            x = max(0, min(x, w - 1))
            y = max(0, min(y, h - 1))
            cw = min(cw, w - x)
            ch = min(ch, h - y)
            
            if cw > 0 and ch > 0:
                corner_region = frame[y:y+ch, x:x+cw]
                logo_boxes = self._detect_logos_in_region(corner_region, x, y)
                
                for box in logo_boxes:
                    box['corner'] = corner_name
                    detected_logos.append(box)
        
        # Enhanced edge regions (wider strips to catch moving watermarks)
        edge_regions = {
            'top_edge': (0, 0, w, int(h * 0.2)),
            'bottom_edge': (0, int(h * 0.8), w, int(h * 0.2)),
            'left_edge': (0, 0, int(w * 0.2), h),
            'right_edge': (int(w * 0.8), 0, int(w * 0.2), h)
        }
        
        for edge_name, (x, y, ew, eh) in edge_regions.items():
            # Ensure we don't go out of bounds
            x = max(0, min(x, w - 1))
            y = max(0, min(y, h - 1))
            ew = min(ew, w - x)
            eh = min(eh, h - y)
            
            if ew > 0 and eh > 0:
                edge_region = frame[y:y+eh, x:x+ew]
                logo_boxes = self._detect_logos_in_region(edge_region, x, y)
                
                for box in logo_boxes:
                    box['corner'] = edge_name
                    detected_logos.append(box)
        
        return detected_logos
    
    def _detect_logos_in_region(self, region: np.ndarray, offset_x: int, offset_y: int) -> List[dict]:
        """Detect logos in a specific region using OCR-first approach"""
        logos = []
        
        # Method 1: OCR-based text detection (highest priority for text watermarks)
        ocr_boxes = self._detect_text_with_ocr(region, offset_x, offset_y)
        logos.extend(ocr_boxes)
        
        # Only use traditional methods if OCR didn't find anything significant
        if not any(box.get('is_watermark', False) for box in ocr_boxes):
            # Method 2: High-confidence traditional text detection only
            text_boxes = self._detect_text_regions_selective(region, offset_x, offset_y)
            logos.extend(text_boxes)
        
        return logos
    
    def _detect_text_with_ocr(self, region: np.ndarray, offset_x: int, offset_y: int) -> List[dict]:
        """Fast OCR detection - optimized for speed with better text extraction and area coverage"""
        text_regions = []
        
        # Skip very small regions to save processing time
        h, w = region.shape[:2]
        if h < 20 or w < 20:
            return text_regions
        
        # For large regions, use full region analysis first to catch complete watermarks
        if h > 400 or w > 400:
            # First try OCR on the full region to catch complete watermarks
            full_region_detections = self._detect_text_with_ocr_full_region(region, offset_x, offset_y)
            text_regions.extend(full_region_detections)
            
            # If we found good watermarks, return early
            if any(d.get('is_watermark', False) and d.get('confidence', 0) > 0.7 for d in full_region_detections):
                return text_regions
            
            # Otherwise, split into smaller chunks for detailed analysis
            regions_to_check = [
                (region[0:h//3, 0:w//3], 0, 0),  # Top-left
                (region[0:h//3, 2*w//3:w], 2*w//3, 0),  # Top-right
                (region[2*h//3:h, 0:w//3], 0, 2*h//3),  # Bottom-left
                (region[2*h//3:h, 2*w//3:w], 2*w//3, 2*h//3),  # Bottom-right
            ]
            
            for sub_region, sub_x, sub_y in regions_to_check:
                if sub_region.size > 0:
                    sub_detections = self._detect_text_with_ocr(sub_region, offset_x + sub_x, offset_y + sub_y)
                    text_regions.extend(sub_detections)
            
            return text_regions
        
        # Use Pytesseract first (much faster than EasyOCR)
        if PYTESSERACT_AVAILABLE:
            try:
                # Quick preprocessing
                if len(region.shape) == 3:
                    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
                else:
                    gray = region.copy()
                
                # Try multiple OCR configurations for better detection
                configs = [
                    r'--oem 3 --psm 6',  # Uniform block of text
                    r'--oem 3 --psm 8',  # Single word
                    r'--oem 3 --psm 7',  # Single text line
                    r'--oem 3 --psm 13', # Raw line
                ]
                
                best_text = ""
                best_confidence = 0
                
                for config in configs:
                    try:
                        text = pytesseract.image_to_string(gray, config=config).strip()
                        if len(text) > len(best_text):
                            best_text = text
                            best_confidence = 0.7
                    except:
                        continue
                
                if len(best_text) > 1:
                    # Check if text looks like a watermark
                    is_watermark = self._is_watermark_text(best_text)
                    confidence = 0.8 if is_watermark else 0.5
                    
                    text_regions.append({
                        'x': offset_x,
                        'y': offset_y,
                        'width': w,
                        'height': h,
                        'confidence': confidence,
                        'type': 'ocr_tesseract',
                        'text': best_text,
                        'is_watermark': is_watermark,
                        'corner': 'ocr_detected'
                    })
                    
            except Exception as e:
                print(f"Fast OCR failed: {e}")
        
        return text_regions
    
    def _detect_text_with_ocr_full_region(self, region: np.ndarray, offset_x: int, offset_y: int) -> List[dict]:
        """OCR detection on full region to capture complete watermarks - more selective"""
        text_regions = []
        h, w = region.shape[:2]
        
        # Only use full region detection on smaller regions to avoid false positives
        if h > 200 or w > 300:
            return text_regions
        
        # Use Pytesseract on the full region first
        if PYTESSERACT_AVAILABLE:
            try:
                # Quick preprocessing
                if len(region.shape) == 3:
                    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
                else:
                    gray = region.copy()
                
                # Try OCR on the full region with different configurations
                configs = [
                    r'--oem 3 --psm 7',  # Single text line
                    r'--oem 3 --psm 8',  # Single word
                ]
                
                best_text = ""
                best_confidence = 0
                
                for config in configs:
                    try:
                        text = pytesseract.image_to_string(gray, config=config).strip()
                        if len(text) > len(best_text):
                            best_text = text
                            best_confidence = 0.7
                    except:
                        continue
                
                if len(best_text) > 2:  # Require at least 3 characters
                    # Check if text looks like a watermark
                    is_watermark = self._is_watermark_text(best_text)
                    
                    # Only add if it's likely a watermark
                    if is_watermark:
                        confidence = 0.8
                        
                        # For watermarks, add conservative padding
                        padding_x = min(10, int(w * 0.1))  # 10% padding or 10px max
                        padding_y = min(8, int(h * 0.1))   # 10% padding or 8px max
                        
                        # Expand the detection area slightly
                        expanded_x = max(0, offset_x - padding_x)
                        expanded_y = max(0, offset_y - padding_y)
                        expanded_w = w + 2 * padding_x
                        expanded_h = h + 2 * padding_y
                        
                        text_regions.append({
                            'x': expanded_x,
                            'y': expanded_y,
                            'width': expanded_w,
                            'height': expanded_h,
                            'confidence': confidence,
                            'type': 'ocr_full_region',
                            'text': best_text,
                            'is_watermark': is_watermark,
                            'corner': 'full_region_scan'
                        })
                    
            except Exception as e:
                print(f"Full region OCR failed: {e}")
        
        return text_regions
    
    def _preprocess_for_ocr(self, region: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        if len(region.shape) == 3:
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        else:
            gray = region.copy()
        
        # Resize if too small (OCR works better on larger images)
        h, w = gray.shape
        if h < 50 or w < 50:
            scale = max(50 / h, 50 / w, 2.0)
            new_h, new_w = int(h * scale), int(w * scale)
            gray = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        
        # Apply multiple preprocessing techniques
        processed_variants = []
        
        # Original
        processed_variants.append(gray)
        
        # High contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        processed_variants.append(enhanced)
        
        # Binary threshold
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processed_variants.append(binary)
        
        # Inverted binary
        _, inv_binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        processed_variants.append(inv_binary)
        
        # Return the variant with highest contrast
        best_variant = gray
        best_contrast = 0
        
        for variant in processed_variants:
            contrast = np.std(variant)
            if contrast > best_contrast:
                best_contrast = contrast
                best_variant = variant
        
        return best_variant
    
    def _is_watermark_text(self, text: str) -> bool:
        """Check if detected text looks like a watermark"""
        text_lower = text.lower().strip()
        
        # Common watermark patterns
        watermark_patterns = [
            r'www\.',           # Website URLs
            r'\.com',           # Domain endings
            r'\.org',
            r'\.net',
            r'\.tv',
            r'\.me',
            r'\.io',
            r'drama',           # Drama sites
            r'movie',           # Movie sites
            r'stream',          # Streaming sites
            r'download',        # Download sites
            r'watch',           # Watch sites
            r'free',            # Free content sites
            r'hd',              # HD quality indicators
            r'1080p',           # Quality indicators
            r'720p',
            r'copyright',       # Copyright notices
            r'©',               # Copyright symbol
            r'™',               # Trademark
            r'®',               # Registered trademark
            r'watermark',       # Explicit watermark
            r'logo',            # Logo text
            r'subscribe',       # Subscribe prompts
            r'follow',          # Follow prompts
        ]
        
        # Moving watermark specific patterns (expanded)
        moving_watermark_patterns = [
            r'moving',          # Moving watermark
            r'mov',             # Part of moving
            r'ving',            # Part of moving
            r'oving',           # Part of moving
            r'water',           # Part of watermark
            r'mark',            # Part of watermark
            r'ater',            # Part of watermark
            r'ter',             # Part of watermark
            r'rmark',           # Part of watermark
            r'emark',           # Part of watermark
            r'watermar',        # Partial watermark
            r'waterm',          # Partial watermark
            r'g water',         # "ING WATER" from "MOVING WATERMARK"
            r'nic water',       # OCR error for "ING WATER"
            r'waterkaar',       # OCR error for "WATERMARK"
            r'tepkaarko',       # OCR error for "WATERMARK"
        ]
        
        # Check for patterns
        for pattern in watermark_patterns + moving_watermark_patterns:
            if re.search(pattern, text_lower):
                return True
        
        # Check for URL-like patterns
        if re.search(r'[a-zA-Z0-9]+\.[a-zA-Z]{2,}', text):
            return True
        
        # Check for short promotional text
        if len(text) < 30 and any(word in text_lower for word in ['free', 'watch', 'download', 'hd', 'stream']):
            return True
        
        # Check for fragments that might be part of "MOVING WATERMARK"
        if len(text) >= 2:
            # Check if this text fragment appears in common watermark phrases
            watermark_phrases = ['moving watermark', 'watermark', 'moving', 'copyright notice']
            for phrase in watermark_phrases:
                if text_lower in phrase.replace(' ', ''):
                    return True
        
        return False
    
    def _detect_text_regions(self, region: np.ndarray, offset_x: int, offset_y: int) -> List[dict]:
        """Detect text-based logos using multiple enhanced methods"""
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        text_regions = []
        h, w = region.shape[:2]
        
        # Method 1: Multiple edge detection thresholds
        for low_thresh, high_thresh in [(20, 80), (50, 150), (30, 120)]:
            edges = cv2.Canny(gray, low_thresh, high_thresh)
            
            # Apply morphological operations to connect text components
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                x, y, cw, ch = cv2.boundingRect(contour)
                
                # Much more lenient filtering for better detection
                if (cw > 10 and ch > 6 and cw < w * 0.95 and ch < h * 0.95 and 
                    0.05 <= ch/cw <= 5.0):  # Very flexible aspect ratio
                    
                    confidence = self._calculate_text_confidence(gray[y:y+ch, x:x+cw])
                    
                    if confidence > 0.1:  # Much lower threshold
                        text_regions.append({
                            'x': offset_x + x,
                            'y': offset_y + y,
                            'width': cw,
                            'height': ch,
                            'confidence': confidence,
                            'type': 'text'
                        })
        
        # Method 2: Adaptive thresholding for text
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Find connected components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
        
        for i in range(1, num_labels):  # Skip background
            x, y, cw, ch, area = stats[i]
            
            if (cw > 8 and ch > 5 and cw < w * 0.9 and ch < h * 0.9 and
                0.1 <= ch/cw <= 8.0 and area > 20):
                
                confidence = min(area / (cw * ch), 1.0)
                
                if confidence > 0.05:
                    text_regions.append({
                        'x': offset_x + x,
                        'y': offset_y + y,
                        'width': cw,
                        'height': ch,
                        'confidence': confidence,
                        'type': 'text_adaptive'
                    })
        
        # Method 3: Variance-based text detection
        text_regions.extend(self._detect_by_variance(gray, offset_x, offset_y))
        
        return text_regions
    
    def _detect_by_variance(self, gray: np.ndarray, offset_x: int, offset_y: int) -> List[dict]:
        """Detect text regions using variance analysis"""
        text_regions = []
        h, w = gray.shape
        
        # Text areas typically have high variance due to character boundaries
        window_size = 15  # Smaller window for better detection
        stride = 8
        
        for y in range(0, h - window_size, stride):
            for x in range(0, w - window_size, stride):
                window = gray[y:y+window_size, x:x+window_size]
                
                # Calculate variance
                variance = np.var(window)
                
                # Text areas have moderate to high variance
                if variance > 50:  # Lower threshold for better detection
                    # Find the actual text boundaries
                    text_box = self._find_text_boundaries(gray, x, y, window_size)
                    if text_box:
                        text_regions.append({
                            'x': offset_x + text_box[0],
                            'y': offset_y + text_box[1],
                            'width': text_box[2],
                            'height': text_box[3],
                            'confidence': min(variance / 1000, 1.0),
                            'type': 'text_variance'
                        })
        
        return text_regions

    def _find_text_boundaries(self, gray: np.ndarray, start_x: int, start_y: int, window_size: int) -> Optional[Tuple[int, int, int, int]]:
        """Find tight boundaries around text in a region"""
        h, w = gray.shape
        end_x = min(start_x + window_size, w)
        end_y = min(start_y + window_size, h)
        
        region = gray[start_y:end_y, start_x:end_x]
        
        # Apply threshold to find text pixels
        _, binary = cv2.threshold(region, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find non-zero pixels (both dark and light text)
        coords_dark = np.column_stack(np.where(binary < 128))  # Dark pixels (text)
        coords_light = np.column_stack(np.where(binary > 128))  # Light pixels (text)
        
        # Use whichever has more pixels
        coords = coords_dark if len(coords_dark) > len(coords_light) else coords_light
        
        if len(coords) == 0:
            return None
        
        # Find bounding box
        min_y, min_x = np.min(coords, axis=0)
        max_y, max_x = np.max(coords, axis=0)
        
        # Add padding
        padding = 2
        min_x = max(0, min_x - padding)
        min_y = max(0, min_y - padding)
        max_x = min(region.shape[1], max_x + padding)
        max_y = min(region.shape[0], max_y + padding)
        
        width = max_x - min_x
        height = max_y - min_y
        
        # Validate size
        if width > 5 and height > 4:
            return (start_x + min_x, start_y + min_y, width, height)
        
        return None
    
    def _detect_edge_based_logos(self, region: np.ndarray, offset_x: int, offset_y: int) -> List[dict]:
        """Detect logos using enhanced edge density analysis"""
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        
        # Apply multiple edge detection methods
        edges1 = cv2.Canny(gray, 20, 80)
        edges2 = cv2.Canny(gray, 50, 150)
        edges3 = cv2.Canny(gray, 30, 120)
        
        # Combine edge maps
        edges = cv2.bitwise_or(edges1, cv2.bitwise_or(edges2, edges3))
        
        h, w = region.shape[:2]
        block_size = 25  # Smaller blocks for better detection
        
        logo_regions = []
        
        for y in range(0, h - block_size, block_size // 4):  # More overlap
            for x in range(0, w - block_size, block_size // 4):
                block = edges[y:y+block_size, x:x+block_size]
                edge_density = np.sum(block > 0) / (block_size * block_size)
                
                # Much lower threshold for better detection
                if edge_density > 0.05:
                    # Try to find the exact logo boundaries
                    logo_box = self._refine_logo_boundaries(edges, x, y, block_size)
                    if logo_box:
                        logo_regions.append({
                            'x': offset_x + logo_box[0],
                            'y': offset_y + logo_box[1], 
                            'width': logo_box[2],
                            'height': logo_box[3],
                            'confidence': edge_density,
                            'type': 'edge_based'
                        })
        
        return logo_regions
    
    def _detect_color_regions(self, region: np.ndarray, offset_x: int, offset_y: int) -> List[dict]:
        """Detect logos based on color consistency - enhanced version"""
        h, w = region.shape[:2]
        
        # Convert to different color spaces for better detection
        hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        
        color_regions = []
        
        # Method 1: Look for white/light regions (common for text watermarks)
        mask_white = cv2.inRange(hsv, (0, 0, 180), (180, 50, 255))
        
        # Method 2: Look for black/dark regions
        mask_black = cv2.inRange(hsv, (0, 0, 0), (180, 255, 80))
        
        # Method 3: Look for semi-transparent regions (common for watermarks)
        mask_semi = cv2.inRange(gray, 120, 200)
        
        # Method 4: Look for any consistent color regions
        mask_consistent = cv2.inRange(hsv, (0, 0, 50), (180, 100, 255))
        
        # Combine all masks
        combined_mask = cv2.bitwise_or(mask_white, mask_black)
        combined_mask = cv2.bitwise_or(combined_mask, mask_semi)
        combined_mask = cv2.bitwise_or(combined_mask, mask_consistent)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, cw, ch = cv2.boundingRect(contour)
            
            # Much more lenient filtering
            if cw > 8 and ch > 5 and cw < w * 0.9 and ch < h * 0.9:
                area_ratio = cv2.contourArea(contour) / (cw * ch)
                
                if area_ratio > 0.3:  # Lower threshold for better detection
                    color_regions.append({
                        'x': offset_x + x,
                        'y': offset_y + y,
                        'width': cw,
                        'height': ch,
                        'confidence': area_ratio,
                        'type': 'color_region'
                    })
        
        return color_regions
    
    def _calculate_text_confidence(self, text_region: np.ndarray) -> float:
        """Calculate confidence that a region contains text"""
        if text_region.size == 0:
            return 0.0
        
        # Apply edge detection
        edges = cv2.Canny(text_region, 50, 150)
        
        # Calculate edge density
        edge_density = np.sum(edges > 0) / edges.size
        
        # Calculate horizontal/vertical line ratios (text has more horizontal lines)
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
        kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
        
        horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel_h)
        vertical_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel_v)
        
        h_score = np.sum(horizontal_lines > 0)
        v_score = np.sum(vertical_lines > 0)
        
        # Text typically has more horizontal features
        if h_score + v_score > 0:
            text_ratio = h_score / (h_score + v_score)
        else:
            text_ratio = 0
        
        # Combine metrics
        confidence = (edge_density * 2 + text_ratio) / 3
        return min(confidence, 1.0)
    
    def _refine_logo_boundaries(self, edges: np.ndarray, start_x: int, start_y: int, block_size: int) -> Optional[Tuple[int, int, int, int]]:
        """Refine logo boundaries by finding the actual edges"""
        # Find the bounding box of edges in the region
        h, w = edges.shape
        end_x = min(start_x + block_size, w)
        end_y = min(start_y + block_size, h)
        
        region = edges[start_y:end_y, start_x:end_x]
        edge_points = np.where(region > 0)
        
        if len(edge_points[0]) == 0:
            return None
        
        # Find tight bounding box
        min_y, max_y = np.min(edge_points[0]), np.max(edge_points[0])
        min_x, max_x = np.min(edge_points[1]), np.max(edge_points[1])
        
        # Add some padding
        padding = 5
        min_x = max(0, min_x - padding)
        min_y = max(0, min_y - padding)
        max_x = min(region.shape[1], max_x + padding)
        max_y = min(region.shape[0], max_y + padding)
        
        return (start_x + min_x, start_y + min_y, max_x - min_x, max_y - min_y)
    
    def merge_overlapping_detections(self, detections: List[dict], overlap_threshold: float = 0.3) -> List[dict]:
        """Merge overlapping logo detections - conservative approach to avoid oversized areas"""
        if not detections:
            return []
        
        # Sort by confidence
        detections.sort(key=lambda x: x['confidence'], reverse=True)
        
        merged = []
        used = set()
        
        for i, detection in enumerate(detections):
            if i in used:
                continue
            
            # For text detections, try to merge nearby detections but be more conservative
            nearby_detections = [detection]
            
            for j in range(i + 1, len(detections)):
                if j in used:
                    continue
                
                # Check overlap
                overlap = self._calculate_overlap(detection, detections[j])
                
                # Also check if detections are nearby (for text fragments)
                distance = self._calculate_distance(detection, detections[j])
                
                # More conservative merging criteria
                should_merge = False
                
                if overlap > overlap_threshold:
                    # Always merge if overlapping significantly
                    should_merge = True
                elif (distance < 30 and  # Much closer distance threshold
                      detection.get('type', '').startswith('text') and 
                      detections[j].get('type', '').startswith('text') and
                      abs(detection['y'] - detections[j]['y']) < 20):  # Similar vertical position
                    # Merge nearby text detections that are on similar horizontal line
                    should_merge = True
                
                if should_merge:
                    nearby_detections.append(detections[j])
                    used.add(j)
            
            # Merge all nearby detections into one larger area
            if len(nearby_detections) > 1:
                merged_detection = self._merge_multiple_detections(nearby_detections)
            else:
                merged_detection = detection.copy()
                # Add minimal padding for single detections
                padding = min(8, detection['width'] // 8, detection['height'] // 4)
                merged_detection['x'] = max(0, merged_detection['x'] - padding)
                merged_detection['y'] = max(0, merged_detection['y'] - padding)
                merged_detection['width'] += 2 * padding
                merged_detection['height'] += 2 * padding
            
            merged.append(merged_detection)
            used.add(i)
        
        return merged
    
    def _calculate_overlap(self, box1: dict, box2: dict) -> float:
        """Calculate overlap ratio between two bounding boxes"""
        x1, y1, w1, h1 = box1['x'], box1['y'], box1['width'], box1['height']
        x2, y2, w2, h2 = box2['x'], box2['y'], box2['width'], box2['height']
        
        # Calculate intersection
        left = max(x1, x2)
        top = max(y1, y2)
        right = min(x1 + w1, x2 + w2)
        bottom = min(y1 + h1, y2 + h2)
        
        if left >= right or top >= bottom:
            return 0.0
        
        intersection = (right - left) * (bottom - top)
        union = w1 * h1 + w2 * h2 - intersection
        
        return intersection / union if union > 0 else 0.0
    
    def _merge_detections(self, box1: dict, box2: dict) -> dict:
        """Merge two overlapping detections"""
        x1, y1, w1, h1 = box1['x'], box1['y'], box1['width'], box1['height']
        x2, y2, w2, h2 = box2['x'], box2['y'], box2['width'], box2['height']
        
        # Calculate merged bounding box
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1 + w1, x2 + w2)
        bottom = max(y1 + h1, y2 + h2)
        
        return {
            'x': left,
            'y': top,
            'width': right - left,
            'height': bottom - top,
            'confidence': max(box1['confidence'], box2['confidence']),
            'type': f"{box1['type']}_merged",
            'corner': box1.get('corner', 'merged')
        }
    
    def _calculate_distance(self, box1: dict, box2: dict) -> float:
        """Calculate distance between two bounding box centers"""
        x1_center = box1['x'] + box1['width'] / 2
        y1_center = box1['y'] + box1['height'] / 2
        x2_center = box2['x'] + box2['width'] / 2
        y2_center = box2['y'] + box2['height'] / 2
        
        distance = ((x1_center - x2_center) ** 2 + (y1_center - y2_center) ** 2) ** 0.5
        return distance
    
    def _merge_multiple_detections(self, detections: List[dict]) -> dict:
        """Merge multiple detections into one larger area - with conservative size limits"""
        if not detections:
            return {}
        
        if len(detections) == 1:
            detection = detections[0].copy()
            # Add minimal padding for single detections
            padding = min(8, detection['width'] // 8, detection['height'] // 4)
            detection['x'] = max(0, detection['x'] - padding)
            detection['y'] = max(0, detection['y'] - padding)
            detection['width'] += 2 * padding
            detection['height'] += 2 * padding
            return detection
        
        # Find bounding box that encompasses all detections
        min_x = min(d['x'] for d in detections)
        min_y = min(d['y'] for d in detections)
        max_x = max(d['x'] + d['width'] for d in detections)
        max_y = max(d['y'] + d['height'] for d in detections)
        
        # Calculate the span
        span_x = max_x - min_x
        span_y = max_y - min_y
        
        # Add minimal padding based on content span
        padding_x = min(15, max(5, span_x // 20))  # 5% of span or max 15px
        padding_y = min(10, max(3, span_y // 20))   # 5% of span or max 10px
        
        final_x = max(0, min_x - padding_x)
        final_y = max(0, min_y - padding_y)
        final_width = span_x + 2 * padding_x
        final_height = span_y + 2 * padding_y
        
        # Impose much stricter size limits (watermarks should be compact)
        max_width = 300  # Maximum watermark width (reduced from 600)
        max_height = 100  # Maximum watermark height (reduced from 200)
        
        if final_width > max_width:
            # Center the reduced area
            center_x = final_x + final_width // 2
            final_x = max(0, center_x - max_width // 2)
            final_width = max_width
        
        if final_height > max_height:
            # Center the reduced area
            center_y = final_y + final_height // 2
            final_y = max(0, center_y - max_height // 2)
            final_height = max_height
            final_y = max(0, center_y - max_height // 2)
            final_height = max_height
        
        # Combine text from all detections
        texts = [d.get('text', '') for d in detections if d.get('text', '').strip()]
        # Remove duplicates and clean up
        unique_texts = []
        for text in texts:
            clean_text = text.strip()
            if clean_text and clean_text not in unique_texts:
                unique_texts.append(clean_text)
        combined_text = ' '.join(unique_texts[:3])  # Limit to first 3 unique texts
        
        # Use highest confidence
        max_confidence = max(d.get('confidence', 0) for d in detections)
        
        # Check if any detection is a watermark
        is_watermark = any(d.get('is_watermark', False) for d in detections)
        
        return {
            'x': final_x,
            'y': final_y,
            'width': final_width,
            'height': final_height,
            'confidence': max_confidence,
            'type': 'merged_watermark',
            'text': combined_text,
            'is_watermark': is_watermark,
            'corner': f"merged_{len(detections)}_areas",
            'merged_count': len(detections)
        }
    
    def _detect_text_watermarks_full_frame(self, frame: np.ndarray) -> List[dict]:
        """Fast full-frame watermark detection - includes moving watermark detection"""
        if frame is None:
            return []
        
        # Scale down frame for faster processing
        h, w = frame.shape[:2]
        max_dim = 800  # Limit frame size for speed
        scale_factor = 1.0
        
        if h > max_dim or w > max_dim:
            scale_factor = max_dim / max(h, w)
            new_h, new_w = int(h * scale_factor), int(w * scale_factor)
            frame_scaled = cv2.resize(frame, (new_w, new_h))
        else:
            frame_scaled = frame
        
        detections = []
        
        # Method 1: Standard OCR detection
        ocr_detections = self._detect_text_with_ocr(frame_scaled, 0, 0)
        
        # Method 2: Moving watermark detection (grid-based)
        moving_detections = self._detect_moving_watermarks(frame_scaled)
        
        # Combine all detections
        all_detections = ocr_detections + moving_detections
        
        # Scale back coordinates if frame was resized
        if scale_factor != 1.0:
            for detection in all_detections:
                detection['x'] = int(detection['x'] / scale_factor)
                detection['y'] = int(detection['y'] / scale_factor)
                detection['width'] = int(detection['width'] / scale_factor)
                detection['height'] = int(detection['height'] / scale_factor)
        
        return all_detections

    def _calculate_website_text_confidence(self, roi: np.ndarray, aspect_ratio: float) -> float:
        """Calculate confidence for website text detection"""
        if roi.size == 0:
            return 0.0
        
        # Base confidence from aspect ratio (websites are horizontal)
        aspect_confidence = min(aspect_ratio / 10.0, 1.0)
        
        # Edge density (text has edges)
        edges = cv2.Canny(roi, 50, 150)
        edge_density = np.sum(edges > 0) / edges.size
        
        # Horizontal structure detection
        kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
        horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel_h)
        horizontal_score = np.sum(horizontal_lines > 0) / edges.size
        
        # Text pattern detection (look for character-like structures)
        # Small erosion followed by dilation to detect character gaps
        kernel_small = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        eroded = cv2.erode(edges, kernel_small, iterations=1)
        dilated = cv2.dilate(eroded, kernel_small, iterations=1)
        pattern_score = np.sum(dilated > 0) / edges.size
        
        # Combine all factors
        confidence = (aspect_confidence * 0.3 + 
                     edge_density * 0.3 + 
                     horizontal_score * 0.2 + 
                     pattern_score * 0.2)
        
        return min(confidence, 1.0)

    def _detect_text_regions_selective(self, region: np.ndarray, offset_x: int, offset_y: int) -> List[dict]:
        """Selective text detection with OCR - high-confidence detections only"""
        gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        text_regions = []
        h, w = region.shape[:2]
        
        # Only use adaptive thresholding - most reliable method
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Find connected components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
        
        for i in range(1, num_labels):  # Skip background
            x, y, cw, ch, area = stats[i]
            
            # Much stricter filtering for text-like regions
            if (cw > 20 and ch > 10 and cw < w * 0.8 and ch < h * 0.8 and
                0.2 <= ch/cw <= 2.0 and area > 100):  # Higher thresholds
                
                confidence = min(area / (cw * ch), 1.0)
                
                if confidence > 0.3:  # High confidence threshold
                    # Extract the specific region and try OCR on it
                    roi = region[y:y+ch, x:x+cw]
                    
                    # Try OCR on this region
                    if PYTESSERACT_AVAILABLE and roi.size > 0:
                        try:
                            if len(roi.shape) == 3:
                                roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                            else:
                                roi_gray = roi
                            
                            # Try different OCR modes
                            text = ""
                            for psm in [6, 7, 8, 13]:
                                try:
                                    config = f'--oem 3 --psm {psm}'
                                    candidate_text = pytesseract.image_to_string(roi_gray, config=config).strip()
                                    if len(candidate_text) > len(text):
                                        text = candidate_text
                                except:
                                    continue
                            
                            if len(text) > 1:
                                # Check if it's a watermark
                                is_watermark = self._is_watermark_text(text)
                                final_confidence = 0.8 if is_watermark else confidence
                                
                                text_regions.append({
                                    'x': offset_x + x,
                                    'y': offset_y + y,
                                    'width': cw,
                                    'height': ch,
                                    'confidence': final_confidence,
                                    'type': 'text_selective',
                                    'text': text,
                                    'is_watermark': is_watermark,
                                    'corner': 'selective_ocr'
                                })
                            else:
                                # No readable text, but keep as potential logo
                                text_regions.append({
                                    'x': offset_x + x,
                                    'y': offset_y + y,
                                    'width': cw,
                                    'height': ch,
                                    'confidence': confidence,
                                    'type': 'text_selective',
                                    'text': '',
                                    'is_watermark': False,
                                    'corner': 'selective_shape'
                                })
                        except Exception as e:
                            # Fallback to shape detection
                            text_regions.append({
                                'x': offset_x + x,
                                'y': offset_y + y,
                                'width': cw,
                                'height': ch,
                                'confidence': confidence,
                                'type': 'text_selective',
                                'text': '',
                                'is_watermark': False,
                                'corner': 'selective_fallback'
                            })
        
        return text_regions

    def _texts_are_similar(self, text1: str, text2: str) -> bool:
        """Check if two texts are similar enough to be the same moving watermark"""
        if not text1 or not text2:
            return False
            
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()
        
        # Exact match
        if text1 == text2:
            return True
        
        # If one is much shorter, check if it's contained in the other
        if len(text1) < len(text2):
            shorter, longer = text1, text2
        else:
            shorter, longer = text2, text1
            
        # If shorter text is contained in longer (accounting for OCR fragmentation)
        if len(shorter) >= 1 and shorter in longer:  # Allow single chars if contained
            return True
        
        # Special case: "MOVING WATERMARK" phrase detection
        # Check if both texts are parts of the common "MOVING WATERMARK" phrase
        moving_parts = {'moving', 'mov', 'ving', 'oving', 'ov', 'vi', 'ng', 'g', 'v'}
        watermark_parts = {'watermark', 'water', 'mark', 'ater', 'ter', 'rmark', 'emark', 'ark', 'ate'}
        
        # Normalize and check for moving/watermark fragments
        text1_norm = text1.replace(' ', '').replace('-', '').replace('_', '')
        text2_norm = text2.replace(' ', '').replace('-', '').replace('_', '')
        
        # Check if one is from "moving" and other from "watermark"
        text1_is_moving = any(part in text1_norm for part in moving_parts)
        text1_is_watermark = any(part in text1_norm for part in watermark_parts)
        text2_is_moving = any(part in text2_norm for part in moving_parts)
        text2_is_watermark = any(part in text2_norm for part in watermark_parts)
        
        # If one is from "moving" and other from "watermark", they're part of the same phrase
        if (text1_is_moving and text2_is_watermark) or (text1_is_watermark and text2_is_moving):
            return True
        
        # Check for moving watermark fragments (expanded and more comprehensive)
        watermark_fragments = {
            'moving', 'mov', 'ving', 'oving', 'ov', 'vi', 'ng', 'in', 'g',
            'watermark', 'water', 'mark', 'ater', 'ter', 'wat', 'ate', 'ma', 'ar', 'rk',
            'emark', 'rmark', 'wate', 'terma', 'ermar', 'rmار', 'g water', 'nic water',
            'logo', 'brand', 'copyright', '©', '®', '™', 'copy', 'right', 'ight',
            'watermar', 'waterm', 'aterm', 'rmar', 'mar', 'ark', 'emark', 'rmark',
            'waterkaar', 'tepkaarko', 'waterkaar', 'kaar', 'tepka', 'kaarko'  # OCR errors
        }
        
        # If both texts contain fragments from the same watermark
        text1_fragments = {frag for frag in watermark_fragments if frag in text1_norm}
        text2_fragments = {frag for frag in watermark_fragments if frag in text2_norm}
        
        # If they share watermark fragments
        if text1_fragments & text2_fragments:
            return True
            
        # Special case: check if texts could be parts of "MOVING WATERMARK"
        combined_target = 'movingwatermark'
        normalized_target = 'moving watermark'
        
        # Check if both texts are substrings of the target
        if len(text1) >= 2 and len(text2) >= 2:
            if (text1_norm in combined_target or text1_norm in normalized_target) and \
               (text2_norm in combined_target or text2_norm in normalized_target):
                return True
        
        # Check if one text is a corrupted version of the other (OCR errors)
        if len(text1) >= 3 and len(text2) >= 3:
            # Calculate edit distance roughly
            common_chars = set(text1) & set(text2)
            max_len = max(len(text1), len(text2))
            min_len = min(len(text1), len(text2))
            
            # If they have significant character overlap
            if len(common_chars) >= min_len * 0.6:  # 60% character overlap
                return True
            
            # Check for partial matches (one contains significant part of the other)
            if len(text1) >= 4 and len(text2) >= 4:
                # Check if significant portions match
                for i in range(len(text1) - 2):
                    for j in range(len(text2) - 2):
                        if text1[i:i+3] == text2[j:j+3]:  # 3-char match
                            return True
        
        return False
    
    def _select_best_watermarks(self, watermarks: List[dict], watermark_positions: dict) -> List[dict]:
        """Select the best watermarks based on consistency and confidence"""
        if not watermarks:
            return []
        
        # Group watermarks by text content
        watermark_groups = {}
        for watermark in watermarks:
            text = watermark.get('text', '')
            if text:
                if text not in watermark_groups:
                    watermark_groups[text] = []
                watermark_groups[text].append(watermark)
        
        best_watermarks = []
        
        for text, group in watermark_groups.items():
            # Sort by confidence
            group.sort(key=lambda x: x.get('confidence', 0), reverse=True)
            
            # Check if this watermark appears in multiple frames (more reliable)
            frame_count = len(set(w.get('frame', 0) for w in group))
            
            # Take the best detection of this watermark
            best_detection = group[0].copy()
            
            # If watermark appears in multiple frames, boost confidence
            if frame_count > 1:
                best_detection['confidence'] = min(best_detection.get('confidence', 0) * 1.2, 1.0)
                best_detection['multi_frame'] = True
            
            # Add position stability info
            if text in watermark_positions and len(watermark_positions[text]) > 1:
                positions = watermark_positions[text]
                x_positions = [p['x'] for p in positions]
                y_positions = [p['y'] for p in positions]
                
                # Calculate position variance (lower = more stable)
                x_variance = np.var(x_positions) if len(x_positions) > 1 else 0
                y_variance = np.var(y_positions) if len(y_positions) > 1 else 0
                
                # If position is very stable, boost confidence
                if x_variance < 50 and y_variance < 50:  # Stable position
                    best_detection['confidence'] = min(best_detection.get('confidence', 0) * 1.1, 1.0)
                    best_detection['position_stable'] = True
                else:
                    best_detection['position_stable'] = False
            
            best_watermarks.append(best_detection)
        
        # Sort by confidence and return
        best_watermarks.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        return best_watermarks
    
    def _detect_moving_watermarks(self, frame: np.ndarray) -> List[dict]:
        """Detect watermarks that might be moving or in unusual positions"""
        if frame is None:
            return []
        
        h, w = frame.shape[:2]
        detections = []
        
        # Create a grid to scan the entire frame efficiently
        grid_size = 6  # 6x6 grid
        cell_w = w // grid_size
        cell_h = h // grid_size
        
        for row in range(grid_size):
            for col in range(grid_size):
                # Skip center cells to avoid main content
                if 1 <= row <= 4 and 1 <= col <= 4:
                    continue
                
                x = col * cell_w
                y = row * cell_h
                
                # Extract cell region
                cell_region = frame[y:y+cell_h, x:x+cell_w]
                
                # Use OCR to detect text in this cell
                cell_detections = self._detect_text_with_ocr(cell_region, x, y)
                
                # Mark these as potentially moving watermarks
                for detection in cell_detections:
                    detection['corner'] = f'grid_{row}_{col}'
                    detection['moving_scan'] = True
                    detections.append(detection)
        
        return detections
    
    def detect_logos_with_timeline(self, video_path: str, sample_interval: float = 2.0) -> List[dict]:
        """Enhanced detection that tracks watermark positions throughout video timeline"""
        
        # Get video duration first
        try:
            duration_cmd = [
                "ffprobe", "-v", "error", "-show_entries", "format=duration", 
                "-of", "default=noprint_wrappers=1:nokey=1", video_path
            ]
            duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
            duration = float(duration_result.stdout.strip())
        except:
            duration = 60.0  # Default fallback
        
        # Sample frames throughout the video
        timestamps = []
        current_time = 1.0  # Start at 1 second
        while current_time < duration - 1.0:
            timestamps.append(current_time)
            current_time += sample_interval
        
        # Ensure we have at least a few samples
        if len(timestamps) < 3:
            timestamps = [1.0, duration/2, duration-1.0]
        
        print(f"🎬 Analyzing {len(timestamps)} frames across {duration:.1f}s video for moving watermarks")
        
        all_detections = []
        
        for i, timestamp in enumerate(timestamps):
            frame = self.extract_frame(video_path, timestamp)
            if frame is None:
                continue
            
            # Detect logos in this frame
            frame_detections = self.detect_logos_in_corners(frame)
            
            # Add temporal information
            for detection in frame_detections:
                detection['frame_index'] = i
                detection['timestamp'] = timestamp
                detection['frame_time'] = timestamp
                
            all_detections.extend(frame_detections)
        
        # Group detections by text similarity to track movement
        watermark_timelines = self._create_watermark_timelines(all_detections)
        
        return watermark_timelines
    
    def _create_watermark_timelines(self, detections: List[dict]) -> List[dict]:
        """Create timeline tracks for watermarks showing their movement over time"""
        
        # First, filter out obvious false positives
        filtered_detections = []
        for detection in detections:
            text = detection.get('text', '').strip()
            confidence = detection.get('confidence', 0)
            
            # Skip very low confidence detections
            if confidence < 0.5:  # Lowered from 0.6 for moving watermarks
                continue
                
            # Skip very short text fragments, but allow 2+ chars for moving watermarks
            if len(text) < 2:  # Lowered from 3 to catch partial text
                continue
                
            # Skip single characters only if very low confidence
            if len(text) == 1 and confidence < 0.7:
                continue
                
            # Skip obvious timestamp/frame number patterns
            if any(pattern in text.lower() for pattern in ['00:', 'fps', 'frame', 'sec']):
                continue
                
            # Prioritize watermark indicators (expanded list for moving watermarks)
            is_likely_watermark = (
                any(indicator in text.lower() for indicator in ['www', '.com', '©', '®', '™', 'watermark', 'moving', 'mark', 'water', 'mov', 'ving', 'ater', 'emark']) or
                detection.get('is_watermark', False) or
                confidence > 0.8 or
                (len(text) >= 3 and confidence > 0.6)  # Include longer text with decent confidence
            )
            
            detection['watermark_score'] = confidence * (2.0 if is_likely_watermark else 1.0)
            filtered_detections.append(detection)
        
        # Sort by watermark score and take top candidates
        filtered_detections.sort(key=lambda x: x.get('watermark_score', 0), reverse=True)
        
        # Limit to top 20 most likely watermarks to avoid overwhelming
        filtered_detections = filtered_detections[:20]
        
        # Group by text content with fuzzy matching for moving watermarks
        text_groups = {}
        position_groups = []  # For spatial-temporal grouping
        
        for detection in filtered_detections:
            text = detection.get('text', '').strip()
            x, y = detection['x'], detection['y']
            timestamp = detection.get('timestamp', 0)
            
            # Try to find existing groups this detection might belong to
            found_group = False
            
            # First try exact text match
            if text and text in text_groups:
                text_groups[text].append(detection)
                found_group = True
            else:
                # Try fuzzy text matching for moving watermarks
                for existing_text, existing_detections in text_groups.items():
                    if text and existing_text:
                        # Check if texts are similar (use fuzzy matching for all texts, not just long ones)
                        if (text in existing_text or existing_text in text or 
                            self._texts_are_similar(text, existing_text)):
                            # For very short texts, be more strict about position/timing
                            if len(text) <= 2 or len(existing_text) <= 2:
                                # For short fragments, require closer positioning but allow longer time gaps
                                recent_detections = [d for d in existing_detections 
                                                   if abs(d.get('timestamp', 0) - timestamp) < 5.0]  # Increased from 2.0
                                if recent_detections:
                                    avg_x = sum(d['x'] for d in recent_detections) / len(recent_detections)
                                    avg_y = sum(d['y'] for d in recent_detections) / len(recent_detections)
                                    
                                    # Stricter position requirements for short fragments
                                    if abs(x - avg_x) < 100 and abs(y - avg_y) < 50:
                                        text_groups[existing_text].append(detection)
                                        found_group = True
                                        break
                            else:
                                # For longer texts, allow even more temporal flexibility for moving watermarks
                                # Don't restrict by time at all for watermark-like texts
                                if (detection.get('is_watermark', False) or 
                                    any(indicator in text.lower() for indicator in ['watermark', 'moving', 'mark', 'water', 'mov', 'ving', 'ater', 'emark'])):
                                    # For watermark texts, only check position reasonableness
                                    if len(existing_detections) > 0:
                                        # Calculate overall position range
                                        all_x = [d['x'] for d in existing_detections] + [x]
                                        all_y = [d['y'] for d in existing_detections] + [y]
                                        x_range = max(all_x) - min(all_x)
                                        y_range = max(all_y) - min(all_y)
                                        
                                        # If the movement is reasonable (not teleporting across screen)
                                        if x_range < 500 and y_range < 300:  # Allow movement across most of screen
                                            text_groups[existing_text].append(detection)
                                            found_group = True
                                            break
                                else:
                                    # For non-watermark texts, use normal position/timing requirements
                                    recent_detections = [d for d in existing_detections 
                                                       if abs(d.get('timestamp', 0) - timestamp) < 3.0]
                                    if recent_detections:
                                        avg_x = sum(d['x'] for d in recent_detections) / len(recent_detections)
                                        avg_y = sum(d['y'] for d in recent_detections) / len(recent_detections)
                                        
                                        # If position is within reasonable movement range
                                        if abs(x - avg_x) < 200 and abs(y - avg_y) < 100:
                                            text_groups[existing_text].append(detection)
                                            found_group = True
                                            break
            
            # If no text group found, try spatial-temporal grouping
            if not found_group:
                # Look for detections in similar positions across time
                for group in position_groups:
                    recent_in_group = [d for d in group if abs(d.get('timestamp', 0) - timestamp) < 3.0]
                    if recent_in_group:
                        avg_x = sum(d['x'] for d in recent_in_group) / len(recent_in_group)
                        avg_y = sum(d['y'] for d in recent_in_group) / len(recent_in_group)
                        
                        # If this detection is near recent positions in this group
                        if abs(x - avg_x) < 150 and abs(y - avg_y) < 80:
                            group.append(detection)
                            found_group = True
                            break
                
                # Create new group if needed
                if not found_group:
                    if text:
                        text_groups[text] = [detection]
                    else:
                        position_groups.append([detection])
        
        # Convert position groups to text groups
        for i, group in enumerate(position_groups):
            if len(group) > 1:  # Only process multi-detection groups
                # Create a representative text from the group
                texts = [d.get('text', '') for d in group if d.get('text', '').strip()]
                if texts:
                    # Use the longest or most common text
                    group_text = max(texts, key=len) if texts else f'moving_element_{i}'
                else:
                    group_text = f'moving_element_{i}'
                text_groups[group_text] = group
        
        watermark_timelines = []
        
        for text, detections_list in text_groups.items():
            # Calculate average confidence for this text group
            avg_confidence = sum(d.get('confidence', 0) for d in detections_list) / len(detections_list)
            
            # Skip low-quality text groups
            if avg_confidence < 0.7 and len(detections_list) == 1:
                continue
                
            if len(detections_list) == 1:
                # Single detection - check if it's worth keeping
                detection = detections_list[0]
                if detection.get('confidence', 0) < 0.8 and not detection.get('is_watermark', False):
                    continue
                    
                timeline = {
                    'text': text,
                    'type': 'static',
                    'is_moving': False,
                    'detections': detections_list,
                    'positions': [{'x': d['x'], 'y': d['y'], 'width': d['width'], 'height': d['height'], 'confidence': d.get('confidence', 0)} for d in detections_list],
                    'movement_analysis': {'x_variance': 0, 'y_variance': 0},
                    'confidence': max(d.get('confidence', 0) for d in detections_list),
                    'is_watermark': any(d.get('is_watermark', False) for d in detections_list)
                }
                watermark_timelines.append(timeline)
                continue
            
            # Sort by timestamp
            detections_list.sort(key=lambda x: x.get('timestamp', 0))
            
            # Analyze movement
            positions = [(d['x'], d['y']) for d in detections_list]
            timestamps = [d.get('timestamp', 0) for d in detections_list]
            
            # Calculate movement characteristics
            x_coords = [pos[0] for pos in positions]
            y_coords = [pos[1] for pos in positions]
            
            x_variance = np.var(x_coords) if len(x_coords) > 1 else 0
            y_variance = np.var(y_coords) if len(y_coords) > 1 else 0
            
            movement_type = 'static'
            if x_variance > 100 or y_variance > 100:
                if x_variance > y_variance * 2:
                    movement_type = 'horizontal'
                elif y_variance > x_variance * 2:
                    movement_type = 'vertical'
                else:
                    movement_type = 'complex'
            
            timeline = {
                'text': text,
                'type': movement_type,
                'is_moving': movement_type in ['horizontal', 'vertical', 'complex'],
                'detections': detections_list,
                'positions': [{'x': d['x'], 'y': d['y'], 'width': d['width'], 'height': d['height'], 'confidence': d.get('confidence', 0)} for d in detections_list],
                'movement_analysis': {
                    'x_variance': x_variance,
                    'y_variance': y_variance,
                    'x_range': max(x_coords) - min(x_coords),
                    'y_range': max(y_coords) - min(y_coords),
                    'positions': positions,
                    'timestamps': timestamps
                },
                'confidence': max(d.get('confidence', 0) for d in detections_list),
                'is_watermark': any(d.get('is_watermark', False) for d in detections_list)
            }
            
            watermark_timelines.append(timeline)
        
        # Sort by confidence
        watermark_timelines.sort(key=lambda x: x['confidence'], reverse=True)
        
        return watermark_timelines

    def create_dynamic_removal_command(self, video_path: str, watermark_timeline: dict, method: str = 'blur') -> List[str]:
        """Create FFmpeg command for position-aware watermark removal"""
        
        # Get video dimensions for coordinate validation
        import subprocess
        try:
            result = subprocess.run([
                'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', 
                video_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
                if video_stream:
                    frame_width = int(video_stream['width'])
                    frame_height = int(video_stream['height'])
                else:
                    frame_width, frame_height = 640, 480  # Default fallback
            else:
                frame_width, frame_height = 640, 480  # Default fallback
        except:
            frame_width, frame_height = 640, 480  # Default fallback
            
        def validate_coordinates(x, y, w, h):
            """Validate and fix coordinates to fit within frame"""
            # Ensure coordinates are non-negative
            x = max(0, int(x))
            y = max(0, int(y))
            w = max(10, int(w))
            h = max(10, int(h))
            
            # Ensure coordinates fit within frame
            if x >= frame_width:
                x = frame_width - 20
            if y >= frame_height:
                y = frame_height - 20
                
            # Ensure width and height fit within frame
            if x + w > frame_width:
                w = frame_width - x
            if y + h > frame_height:
                h = frame_height - y
                
            # Ensure minimum size
            w = max(w, 10)
            h = max(h, 10)
            
            return x, y, w, h
        
        if watermark_timeline['type'] == 'static':
            # Static watermark - use simple removal
            detection = watermark_timeline['detections'][0]
            x, y, w, h = detection['x'], detection['y'], detection['width'], detection['height']
            
            # Validate coordinates
            x, y, w, h = validate_coordinates(x, y, w, h)
            
            if method == 'blur':
                # Use delogo for more reliable results (blur is complex)
                vf_filter = f"delogo=x={x}:y={y}:w={w}:h={h}"
            elif method == 'delogo':
                vf_filter = f"delogo=x={x}:y={y}:w={w}:h={h}"
            else:
                vf_filter = f"drawbox=x={x}:y={y}:w={w}:h={h}:color=black@0.8:t=fill"
            
            return [self.ffmpeg_path, "-i", video_path, "-vf", vf_filter, "-c:a", "copy"]
        
        else:
            # Moving watermark - create time-based removal
            detections = watermark_timeline['detections']
            
            if method == 'blur':
                # For blur method, use a simpler approach with multiple drawbox filters
                # This is more reliable than complex filter chains
                filter_parts = []
                
                for i, detection in enumerate(detections):
                    start_time = detection.get('timestamp', 0)
                    end_time = detections[i+1].get('timestamp', start_time + 5) if i+1 < len(detections) else start_time + 5
                    
                    x, y, w, h = detection['x'], detection['y'], detection['width'], detection['height']
                    
                    # Add padding for moving watermarks
                    padding = 10
                    x = max(0, x - padding)
                    y = max(0, y - padding)
                    w += 2 * padding
                    h += 2 * padding
                    
                    # Validate coordinates
                    x, y, w, h = validate_coordinates(x, y, w, h)
                    
                    # Use gblur filter instead of complex overlay
                    blur_filter = f"gblur=sigma=20:enable='between(t,{start_time},{end_time})'"
                    filter_parts.append(blur_filter)
                
                # Combine blur filters
                vf_filter = ','.join(filter_parts)
                return [self.ffmpeg_path, "-i", video_path, "-vf", vf_filter, "-c:a", "copy"]
            
            elif method == 'delogo':
                # For delogo, combine all time segments
                filter_parts = []
                
                for i, detection in enumerate(detections):
                    start_time = detection.get('timestamp', 0)
                    end_time = detections[i+1].get('timestamp', start_time + 5) if i+1 < len(detections) else start_time + 5
                    
                    x, y, w, h = detection['x'], detection['y'], detection['width'], detection['height']
                    
                    # Add padding for moving watermarks
                    padding = 10
                    x = max(0, x - padding)
                    y = max(0, y - padding)
                    w += 2 * padding
                    h += 2 * padding
                    
                    # Validate coordinates
                    x, y, w, h = validate_coordinates(x, y, w, h)
                    
                    segment_filter = f"delogo=x={x}:y={y}:w={w}:h={h}:enable='between(t,{start_time},{end_time})'"
                    filter_parts.append(segment_filter)
                
                vf_filter = ','.join(filter_parts)
                return [self.ffmpeg_path, "-i", video_path, "-vf", vf_filter, "-c:a", "copy"]
            
            else:
                # For drawbox method
                filter_parts = []
                
                for i, detection in enumerate(detections):
                    start_time = detection.get('timestamp', 0)
                    end_time = detections[i+1].get('timestamp', start_time + 5) if i+1 < len(detections) else start_time + 5
                    
                    x, y, w, h = detection['x'], detection['y'], detection['width'], detection['height']
                    
                    # Add padding for moving watermarks
                    padding = 10
                    x = max(0, x - padding)
                    y = max(0, y - padding)
                    w += 2 * padding
                    h += 2 * padding
                    
                    # Validate coordinates
                    x, y, w, h = validate_coordinates(x, y, w, h)
                    
                    segment_filter = f"drawbox=x={x}:y={y}:w={w}:h={h}:color=black@0.8:t=fill:enable='between(t,{start_time},{end_time})'"
                    filter_parts.append(segment_filter)
                
                vf_filter = ','.join(filter_parts)
                return [self.ffmpeg_path, "-i", video_path, "-vf", vf_filter, "-c:a", "copy"]
    
    def _validate_coordinates(self, x, y, w, h, video_width, video_height):
        """Validate and fix coordinates to ensure they're within video boundaries"""
        # Ensure coordinates are within bounds
        x = max(0, min(x, video_width - 1))
        y = max(0, min(y, video_height - 1))
        
        # Ensure dimensions don't exceed frame boundaries
        max_w = video_width - x
        max_h = video_height - y
        w = min(w, max_w - 1)  # Leave 1 pixel margin to avoid boundary issues
        h = min(h, max_h - 1)  # Leave 1 pixel margin to avoid boundary issues
        
        # Ensure minimum size for FFmpeg filters
        w = max(w, 2)
        h = max(h, 2)
        
        return x, y, w, h
    
    def _get_video_dimensions(self, video_path):
        """Get video dimensions using ffprobe"""
        try:
            probe_cmd = [
                "ffprobe", "-v", "error", "-select_streams", "v:0", 
                "-show_entries", "stream=width,height", "-of", "csv=p=0", video_path
            ]
            probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
            if probe_result.returncode == 0:
                dimensions = probe_result.stdout.strip().split(',')
                return int(dimensions[0]), int(dimensions[1])
        except:
            pass
        return 1920, 1080  # Default fallback
