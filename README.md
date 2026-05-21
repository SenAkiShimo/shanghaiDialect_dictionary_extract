# Shanghai Dialect Dictionary Parser (AI + OCR Pipeline)

An end-to-end automated document parser designed to extract lexical data from scanned dual-column dialect dictionaries (Shanghai-to-Mandarin) and convert them into structured `.csv` database files.

---

## Current Status & System Architecture

The pipeline utilizes a **Two-Stage Approach** to solve dense document parsing:
1. **Stage 1 (Object Detection):** A custom-trained **YOLOv8 nano** model acts as a layout parser to detect and segment structural components:
   - `Class 0 (Word)`: Shanghai dialect lemmas.
   - `Class 1 (Ignore)`: Phonetic/IPA notations and page elements.
   - `Class 2 (Meaning)`: Mandarin definitions (supporting multi-line text blocks).
   - `Class 3 (CenterLine)`: The vertical dividing line.
2. **Stage 2 (OCR & Extraction):** **PaddleOCR v5** runs target-specific text recognition strictly inside the predicted regions, bypassing structural noise.

---

## Current Challenges & Visual Blindspots

While the custom synthetic data generator has enabled the model to recognize multi-line text structures successfully, empirical debugging on real dictionary scans (`temp_page_8.png`) has revealed 4 critical edge cases that cause spatial drift:

### 1. Linguistic Boundary Merging (Overlapping Boxes)
- **Problem:** Part-of-speech tags (e.g., `〈名〉`, `〈动〉`) and dense phonetic brackets are occasionally merged into the `Word` bounding box instead of being assigned to the `Meaning` or `Ignore` classes. 
- **Root Cause:** In the real dictionary, text tokens are tightly packed horizontally with minimal character spacing.

### 2. Vertical Block Swallowing (Over-segmentation)
- **Problem:** Consecutive independent dictionary entries are grouped into a single massive `Meaning` box.
- **Root Cause:** The synthetic data generator over-represented exceptionally long definitions, causing the AI to overfit to giant clusters of Hanzi characters and ignore thin white-space margins between separate definitions.

### 3. Cross-Column Overlap ("Border Jumping")
- **Problem:** Bounding boxes on the bottom-left column occasionally bleed past the vertical dividing line and merge with entries on the right column.
- **Root Cause:** The AI has not yet fully conceptualized the `CenterLine` class as an absolute, non-traversable physical barrier.

### 4. Page Skew and Scanning Tilt
- **Problem:** Micro-rotations (0.5° to 3.0°) introduced during physical book scanning cause standard axis-aligned bounding boxes to capture fragments of adjacent lines.

---

## Solutions Currently Under Development

We are modifying the core pipeline and synthetic pipeline to address these issues without drastically bloating the training volume:

### A. Enhancing Synthetic Data Variance (`generate_one_page`)
- **Data Re-balancing:** Lowering the probability of long paragraphs to 25% and making short (1-2 lines) definitions the statistical majority (75%).
- **Margin Padding:** Enforcing a strict 10-20px absolute white-space buffer zone around the central vertical dividing line and expanding the vertical entry-to-entry margin.
- **Label Insulation:** Adding explicit structural offsets to separate `Word` bounding boxes from trailing brackets.

### B. Automated Active Image Deskewing (The Vertical Angle Fix)
We are implementing a pre-processing math routine leveraging the detected `CenterLine (Class 3)`:
1. **Detect Line:** Extrapolate the top and bottom endpoints of the vertical line box.
2. **Compute Theta:** Calculate the exact physical tilt angle using arc-tangent slope formula:  
   $$\theta = \arctan\left(\frac{y_2 - y_1}{x_2 - x_1}\right)$$
3. **Warp Matrix:** Automatically rotate the canvas back to a perfectly vertical axis using `cv2.warpAffine` *prior* to final OCR cropping.

---

## Roadmap / Next Steps

- [ ] Re-generate 1,500 high-fidelity synthetic dictionary sheets incorporating grey scanning noise, micro-tilts, and varied dictionary entry margins.
- [ ] Retrain YOLOv8 with AdamW optimizer for 120 epochs using the new dual-class mask anchors.
- [ ] Implement the automated canvas rotation module to stabilize Stage 2 text crops.
