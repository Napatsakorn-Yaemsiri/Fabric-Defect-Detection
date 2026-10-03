# Fabric-Defect-Detection Yolo11s
  Images: {'train_images': 8946, 'val_images': 2566, 'test_images': 2287}  
  - Train: 65  
  - Test: 18.5  
  - Val: 16.5  
Reason: Every dataset except StitchingNet has its own Train/Test/Val set and has a different number of images. Supposedly, every class should be 60/20/20, but due to the different number of images and the removal of unusable classes, it ended up with 65/18.5/16.5

12 Classes:  
-   0 hole                 846  
-   1 stain                1124  
-   2 oil spot             608  
-   3 cut                  757  
-   4 tear                 554  
-   5 wrinkle              499  
-   6 broken stitch        1201  
-   7 skipped stitch       1239  
-   8 pinched fabric       1192  
-   9 crooked seam         1230  
-  10 thread sagging       1173  
-  11 overlapped stitch    1203  
Total images: 13799  
Total backgrounds: 3355  
Total objects: 11626  

## Train
Model: Yolo11s  
Epoch: 130  
Batch: 16  
Image Size: 640  
### Fine-tuning hyperparameters
    optimizer="AdamW",      
    lr0=0.001,
    lrf=0.01,              
    momentum=0.937,
    weight_decay=0.0005,
    mosaic=1.0,
    mixup=0.2,
    degrees=0.0,            
    fliplr=0.5,
    patience=30,            
    seed=42,
    
## Result
| Class | Images | Instances | Precision (P) | Recall (R) | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|---:|---:|
| **all** | 2566 | 2168 | 0.803 | 0.787 | 0.825 | 0.541 |
| hole | 128 | 169 | 0.700 | 0.609 | 0.653 | 0.371 |
| stain | 180 | 211 | 0.724 | 0.608 | 0.721 | 0.442 |
| oil spot | 64 | 73 | 0.752 | 0.916 | 0.914 | 0.637 |
| cut | 133 | 168 | 0.755 | 0.734 | 0.794 | 0.502 |
| tear | 49 | 55 | 0.780 | 0.707 | 0.746 | 0.426 |
| wrinkle | 32 | 44 | 0.602 | 0.309 | 0.403 | 0.208 |
| broken stitch | 240 | 240 | 0.953 | 0.971 | 0.980 | 0.790 |
| skipped stitch | 248 | 248 | 0.906 | 0.984 | 0.986 | 0.655 |
| pinched fabric | 238 | 238 | 0.875 | 0.914 | 0.937 | 0.580 |
| crooked seam | 246 | 246 | 0.909 | 0.935 | 0.963 | 0.673 |
| thread sagging | 235 | 235 | 0.726 | 0.762 | 0.803 | 0.500 |
| overlapped stitch | 241 | 241 | 0.950 | 0.992 | 0.994 | 0.708 |

## Performance
| Metric | Value |
|---|---:|
| Model | YOLO11s |
| Weights | `best.pt` |
| Dataset | Validation set |
| mAP@0.5 | 82.43% |
| mAP@0.50:0.95 | 54.22% |
| Precision | 80.28% |
| Recall | 78.58% |
| Average FPS | 108.38 |
| Model Size (Parameters) | 9,432,436 |
