# Image_Organizer

A python tool to organize and copy DNG/JPG images based on image type, mod time and containing directory.

## Usage:

```python3 Image_Organizer.py <Input Directory> <Output Director>```

## Example:
```python3 Image_Organizer.py </Path/To/Input> </Path/To/Output>```

Files and folders discovered in </Path/To/Input>.
```
├── 100US100
│   ├── L1000001.DNG
│   ├── L1000001.JPG
│   ├── L1000002.DNG
│   ├── L1000002.JPG
├── 100US101
│   ├── L1000003.DNG
│   ├── L1000004.DNG
│   └── L1000005.DNG
└── 100US102
    ├── L1000006.DNG
    ├── L1000007.DNG
    ├── L1000008.DNG
```

New folder structure created in </Path/To/Output>. Files are copied to appropriate path based on containing folder, file type and mod time.
```
├── 100US100
│   ├── DNG
│   │   ├── 2026-01-31
│   │   │   ├── L1000001.DNG
│   │   │   ├── L1000002.DNG
│   └── JPG
│       └── 2026-01-31
│           ├── L1000001.JPG
│           ├── L1000002.JPG
├── 100US101
│   └── DNG
│       └── 2026-02-01
│           ├── L1000003.DNG
│           ├── L1000004.DNG
│           └── L1000005.DNG
└── 100US102
    └── DNG
        ├── 2026-03-01
        │   └── L1000006.DNG
        ├── 2026-03-02
        │   └── L1000007.DNG
        ├── 2026-03-03
        │   └── L1000008.DNG
```
